"""Beginner-friendly Flask application for a small blood donor centre."""
from datetime import date, datetime
import sqlite3
from pathlib import Path

from flask import Flask, flash, redirect, render_template, request, url_for

app = Flask(__name__)
app.secret_key = "blood-donor-academic-project"
BASE_DIR = Path(__file__).resolve().parent
DATABASE = BASE_DIR / "database.db"
BLOOD_GROUPS = ("A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-")
GENDERS = ("Male", "Female", "Other")


def connect_db():
    connection = sqlite3.connect(DATABASE)
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA foreign_keys = ON")
    return connection


def init_db():
    with connect_db() as db:
        db.executescript("""
            CREATE TABLE IF NOT EXISTS donors (
                donor_id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL, age INTEGER NOT NULL CHECK(age BETWEEN 18 AND 65),
                gender TEXT NOT NULL, blood_group TEXT NOT NULL,
                phone TEXT NOT NULL, email TEXT, address TEXT NOT NULL,
                last_donation_date TEXT, eligibility_status TEXT NOT NULL DEFAULT 'Eligible',
                created_date TEXT NOT NULL
            );
            CREATE TABLE IF NOT EXISTS donations (
                donation_id INTEGER PRIMARY KEY AUTOINCREMENT,
                donor_id INTEGER NOT NULL REFERENCES donors(donor_id) ON DELETE CASCADE,
                donation_date TEXT NOT NULL, blood_group TEXT NOT NULL,
                units INTEGER NOT NULL CHECK(units > 0),
                donation_status TEXT NOT NULL CHECK(donation_status IN ('Completed','Cancelled')),
                remarks TEXT DEFAULT ''
            );
            CREATE TABLE IF NOT EXISTS blood_inventory (
                inventory_id INTEGER PRIMARY KEY AUTOINCREMENT,
                blood_group TEXT NOT NULL UNIQUE,
                units_available INTEGER NOT NULL DEFAULT 0 CHECK(units_available >= 0),
                last_updated TEXT NOT NULL
            );
        """)
        today = date.today().isoformat()
        db.executemany("INSERT OR IGNORE INTO blood_inventory (blood_group,units_available,last_updated) VALUES (?,0,?)",
                       [(group, today) for group in BLOOD_GROUPS])


def eligible(last_date):
    if not last_date:
        return "Eligible"
    try:
        return "Eligible" if (date.today() - date.fromisoformat(last_date)).days >= 90 else "Not Eligible"
    except ValueError:
        return "Eligible"


def refresh_eligibility(db, donor_id):
    latest = db.execute("SELECT MAX(donation_date) FROM donations WHERE donor_id=? AND donation_status='Completed'", (donor_id,)).fetchone()[0]
    db.execute("UPDATE donors SET last_donation_date=?, eligibility_status=? WHERE donor_id=?", (latest, eligible(latest), donor_id))


def donor_form_data(form):
    data = {key: form.get(key, "").strip() for key in ("name", "age", "gender", "blood_group", "phone", "email", "address", "last_donation_date")}
    errors = []
    if not all(data[k] for k in ("name", "age", "gender", "blood_group", "phone", "address")):
        errors.append("Please complete all required fields.")
    try:
        age = int(data["age"])
        if age < 18 or age > 65:
            errors.append("Donor age must be between 18 and 65.")
    except ValueError:
        age = 0
        errors.append("Enter a valid age.")
    if data["gender"] not in GENDERS:
        errors.append("Choose a valid gender.")
    if data["blood_group"] not in BLOOD_GROUPS:
        errors.append("Choose a valid blood group.")
    if data["last_donation_date"]:
        try:
            if date.fromisoformat(data["last_donation_date"]) > date.today():
                errors.append("Last donation date cannot be in the future.")
        except ValueError:
            errors.append("Enter a valid last donation date.")
    data["age"] = age
    return data, errors


@app.route("/")
def index():
    with connect_db() as db:
        db.execute("UPDATE donors SET eligibility_status=CASE WHEN last_donation_date IS NULL OR date(last_donation_date)<=date('now','-90 days') THEN 'Eligible' ELSE 'Not Eligible' END")
        stats = {
            "donors": db.execute("SELECT COUNT(*) FROM donors").fetchone()[0],
            "eligible": db.execute("SELECT COUNT(*) FROM donors WHERE eligibility_status='Eligible'").fetchone()[0],
            "donations": db.execute("SELECT COUNT(*) FROM donations").fetchone()[0],
            "units": db.execute("SELECT COALESCE(SUM(units_available),0) FROM blood_inventory").fetchone()[0],
        }
        inventory = db.execute("SELECT * FROM blood_inventory ORDER BY inventory_id").fetchall()
        recent = db.execute("SELECT d.*,p.name AS donor_name FROM donations d JOIN donors p ON p.donor_id=d.donor_id ORDER BY d.donation_date DESC,d.donation_id DESC LIMIT 5").fetchall()
    return render_template("index.html", stats=stats, inventory=inventory, recent=recent)


@app.route("/donors")
def donors():
    query = request.args.get("q", "").strip()
    group = request.args.get("blood_group", "")
    sql = "SELECT * FROM donors WHERE 1=1"
    params = []
    if query:
        sql += " AND (CAST(donor_id AS TEXT) LIKE ? OR name LIKE ? OR phone LIKE ?)"
        params.extend([f"%{query}%"] * 3)
    if group in BLOOD_GROUPS:
        sql += " AND blood_group=?"
        params.append(group)
    sql += " ORDER BY donor_id DESC"
    with connect_db() as db:
        db.execute("UPDATE donors SET eligibility_status=CASE WHEN last_donation_date IS NULL OR date(last_donation_date)<=date('now','-90 days') THEN 'Eligible' ELSE 'Not Eligible' END")
        rows = db.execute(sql, params).fetchall()
    return render_template("donors.html", donors=rows, query=query, selected_group=group, groups=BLOOD_GROUPS)


@app.route("/add_donor", methods=["GET", "POST"])
def add_donor():
    data = {}
    if request.method == "POST":
        data, errors = donor_form_data(request.form)
        if not errors:
            last = data["last_donation_date"] or None
            with connect_db() as db:
                cursor = db.execute("INSERT INTO donors (name,age,gender,blood_group,phone,email,address,last_donation_date,eligibility_status,created_date) VALUES (?,?,?,?,?,?,?,?,?,?)",
                    (data["name"], data["age"], data["gender"], data["blood_group"], data["phone"], data["email"], data["address"], last, eligible(last), date.today().isoformat()))
                # Registration may include a historical last date, but cannot infer historic stock.
                donor_id = cursor.lastrowid
            flash("Donor registered successfully.", "success")
            return redirect(url_for("donor_details", donor_id=donor_id))
        for error in errors:
            flash(error, "error")
    return render_template("add_donor.html", donor=data, groups=BLOOD_GROUPS, genders=GENDERS, title="Register Donor", today=date.today().isoformat())


@app.route("/edit_donor/<int:donor_id>", methods=["GET", "POST"])
def edit_donor(donor_id):
    with connect_db() as db:
        donor = db.execute("SELECT * FROM donors WHERE donor_id=?", (donor_id,)).fetchone()
        if donor is None:
            flash("Donor record was not found.", "error")
            return redirect(url_for("donors"))
        if request.method == "POST":
            data, errors = donor_form_data(request.form)
            if not errors:
                # Completed donation history is authoritative for last donation date.
                latest = db.execute("SELECT MAX(donation_date) FROM donations WHERE donor_id=? AND donation_status='Completed'", (donor_id,)).fetchone()[0]
                last = latest or data["last_donation_date"] or None
                db.execute("UPDATE donors SET name=?,age=?,gender=?,blood_group=?,phone=?,email=?,address=?,last_donation_date=?,eligibility_status=? WHERE donor_id=?",
                           (data["name"],data["age"],data["gender"],data["blood_group"],data["phone"],data["email"],data["address"],last,eligible(last),donor_id))
                flash("Donor updated successfully.", "success")
                return redirect(url_for("donor_details", donor_id=donor_id))
            for error in errors:
                flash(error, "error")
            donor = data
    return render_template("add_donor.html", donor=donor, groups=BLOOD_GROUPS, genders=GENDERS, title="Edit Donor", today=date.today().isoformat())


@app.route("/delete_donor/<int:donor_id>", methods=["POST"])
def delete_donor(donor_id):
    with connect_db() as db:
        cursor = db.execute("DELETE FROM donors WHERE donor_id=?", (donor_id,))
        if cursor.rowcount:
            flash("Donor and related donation records deleted successfully.", "success")
        else:
            flash("Donor record was not found.", "error")
    return redirect(url_for("donors"))


@app.route("/donor/<int:donor_id>")
def donor_details(donor_id):
    with connect_db() as db:
        donor = db.execute("SELECT * FROM donors WHERE donor_id=?", (donor_id,)).fetchone()
        if donor is None:
            flash("Donor record was not found.", "error")
            return redirect(url_for("donors"))
        db.execute("UPDATE donors SET eligibility_status=? WHERE donor_id=?", (eligible(donor["last_donation_date"]), donor_id))
        donor = db.execute("SELECT * FROM donors WHERE donor_id=?", (donor_id,)).fetchone()
        history = db.execute("SELECT * FROM donations WHERE donor_id=? ORDER BY donation_date DESC,donation_id DESC", (donor_id,)).fetchall()
        totals = db.execute("SELECT COUNT(*) AS count,COALESCE(SUM(CASE WHEN donation_status='Completed' THEN units ELSE 0 END),0) AS units FROM donations WHERE donor_id=?", (donor_id,)).fetchone()
    return render_template("donor_details.html", donor=donor, history=history, totals=totals)


@app.route("/donations")
def donations():
    with connect_db() as db:
        rows = db.execute("SELECT d.*,p.name AS donor_name FROM donations d JOIN donors p ON p.donor_id=d.donor_id ORDER BY d.donation_date DESC,d.donation_id DESC").fetchall()
    return render_template("donations.html", donations=rows)


@app.route("/add_donation", methods=["GET", "POST"])
def add_donation():
    with connect_db() as db:
        donor_rows = db.execute("SELECT donor_id,name,blood_group FROM donors ORDER BY name").fetchall()
        if request.method == "POST":
            donor_id = request.form.get("donor_id", "")
            donation_date = request.form.get("donation_date", "").strip()
            status = request.form.get("donation_status", "")
            remarks = request.form.get("remarks", "").strip()
            try:
                units = int(request.form.get("units", ""))
                if units <= 0: raise ValueError
            except ValueError:
                units = 0
            donor = db.execute("SELECT * FROM donors WHERE donor_id=?", (donor_id,)).fetchone()
            errors = []
            if donor is None: errors.append("Select a registered donor.")
            try:
                parsed = date.fromisoformat(donation_date)
                if parsed > date.today(): errors.append("Donation date cannot be in the future.")
            except ValueError:
                errors.append("Enter a valid donation date.")
            if units <= 0: errors.append("Units must be a positive whole number.")
            if status not in ("Completed", "Cancelled"): errors.append("Choose a valid donation status.")
            if not errors and status == "Completed" and eligible(donor["last_donation_date"]) != "Eligible":
                errors.append("This donor is not yet eligible under the 90-day rule.")
            if not errors:
                try:
                    db.execute("INSERT INTO donations (donor_id,donation_date,blood_group,units,donation_status,remarks) VALUES (?,?,?,?,?,?)",
                               (donor["donor_id"], donation_date, donor["blood_group"], units, status, remarks))
                    if status == "Completed":
                        db.execute("UPDATE blood_inventory SET units_available=units_available+?,last_updated=? WHERE blood_group=?", (units, donation_date, donor["blood_group"]))
                        refresh_eligibility(db, donor["donor_id"])
                    flash("Donation recorded successfully.", "success")
                    return redirect(url_for("donations"))
                except sqlite3.Error:
                    flash("The donation could not be saved. Please review the details and try again.", "error")
            for error in errors: flash(error, "error")
    return render_template("add_donation.html", donors=donor_rows, today=date.today().isoformat())


@app.route("/delete_donation/<int:donation_id>", methods=["POST"])
def delete_donation(donation_id):
    with connect_db() as db:
        donation = db.execute("SELECT * FROM donations WHERE donation_id=?", (donation_id,)).fetchone()
        if donation is None:
            flash("Donation record was not found.", "error")
        elif donation["donation_status"] == "Completed":
            current = db.execute("SELECT units_available FROM blood_inventory WHERE blood_group=?", (donation["blood_group"],)).fetchone()[0]
            if current < donation["units"]:
                flash("This donation cannot be deleted because its units have since been used in an inventory adjustment.", "error")
            else:
                db.execute("UPDATE blood_inventory SET units_available=units_available-?,last_updated=? WHERE blood_group=?", (donation["units"], date.today().isoformat(), donation["blood_group"]))
                db.execute("DELETE FROM donations WHERE donation_id=?", (donation_id,))
                refresh_eligibility(db, donation["donor_id"])
                flash("Donation deleted and inventory adjusted successfully.", "success")
        else:
            db.execute("DELETE FROM donations WHERE donation_id=?", (donation_id,))
            flash("Cancelled donation deleted successfully.", "success")
    return redirect(url_for("donations"))


@app.route("/inventory")
def inventory():
    with connect_db() as db: rows = db.execute("SELECT * FROM blood_inventory ORDER BY inventory_id").fetchall()
    return render_template("inventory.html", inventory=rows)


@app.route("/add_inventory", methods=["GET", "POST"])
def add_inventory():
    if request.method == "POST":
        group = request.form.get("blood_group", "")
        try: delta = int(request.form.get("units", ""))
        except ValueError: delta = None
        if group not in BLOOD_GROUPS:
            flash("Choose a valid blood group.", "error")
        elif delta is None or delta == 0:
            flash("Enter a non-zero whole number of units to add or remove.", "error")
        else:
            with connect_db() as db:
                current = db.execute("SELECT units_available FROM blood_inventory WHERE blood_group=?", (group,)).fetchone()[0]
                if current + delta < 0:
                    flash("Inventory cannot be reduced below zero.", "error")
                else:
                    db.execute("UPDATE blood_inventory SET units_available=?,last_updated=? WHERE blood_group=?", (current + delta, date.today().isoformat(), group))
                    flash("Inventory updated successfully.", "success")
                    return redirect(url_for("inventory"))
    return render_template("add_inventory.html", groups=BLOOD_GROUPS)


@app.route("/reports")
def reports():
    with connect_db() as db:
        db.execute("UPDATE donors SET eligibility_status=CASE WHEN last_donation_date IS NULL OR date(last_donation_date)<=date('now','-90 days') THEN 'Eligible' ELSE 'Not Eligible' END")
        summary = db.execute("SELECT COUNT(*) total, SUM(CASE WHEN eligibility_status='Eligible' THEN 1 ELSE 0 END) eligible, SUM(CASE WHEN eligibility_status='Not Eligible' THEN 1 ELSE 0 END) not_eligible FROM donors").fetchone()
        groups = db.execute("SELECT i.blood_group,i.units_available,COUNT(d.donor_id) donor_count FROM blood_inventory i LEFT JOIN donors d ON d.blood_group=i.blood_group GROUP BY i.blood_group ORDER BY i.inventory_id").fetchall()
        totals = db.execute("SELECT COUNT(*) count,COALESCE(SUM(CASE WHEN donation_status='Completed' THEN units ELSE 0 END),0) units FROM donations").fetchone()
        recent = db.execute("SELECT d.*,p.name donor_name FROM donations d JOIN donors p ON p.donor_id=d.donor_id ORDER BY donation_date DESC,donation_id DESC LIMIT 10").fetchall()
    return render_template("reports.html", summary=summary, groups=groups, totals=totals, recent=recent)


init_db()

if __name__ == "__main__":
    app.run(debug=False)
