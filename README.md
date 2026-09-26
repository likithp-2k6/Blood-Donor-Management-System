# Blood Donor Management System

A simple web-based Blood Donor Management System developed as a BCA academic project. The website helps a small blood centre register donors, record donations, track blood inventory, and review basic summaries from a browser.

## 1. Project Description

This project adapts the structure and academic scope of a traditional management-system project to blood donor operations. It uses straightforward Flask routes and SQLite queries to connect donor records, donation history, and available blood units.

## 2. Features

- Donor registration, viewing, editing, deletion, search, and blood-group filtering
- Donor profile with donation history and calculated totals
- Completed and cancelled donation records
- 90-day donor eligibility rule
- Automatic stock updates for completed donations
- Eight blood groups initialized with zero units
- Manual inventory adjustments with protection against negative stock
- Dashboard cards, blood availability, and recent donations
- Donor, blood group, and donation summaries
- Responsive interface, status badges, and confirmation prompts
- SQLite data persists between application restarts

## 3. Technology Stack

- Frontend: HTML5, manually written CSS3, and vanilla JavaScript
- Backend: Python and Flask
- Database: SQLite using Python's built-in `sqlite3` module

No ORM, UI framework, external API, or JavaScript framework is used.

## 4. Project Structure

```text
Blood-Donor-Management-System/
├── app.py
├── requirements.txt
├── README.md
├── database.db          # Created and initialized automatically
├── static/
│   ├── style.css
│   └── script.js
└── templates/
    ├── base.html
    ├── index.html
    ├── donors.html
    ├── add_donor.html
    ├── donor_details.html
    ├── donations.html
    ├── add_donation.html
    ├── inventory.html
    ├── add_inventory.html
    └── reports.html
```

## 5. Database Tables

The database is initialized automatically when `app.py` starts.

### Donors

Stores the donor identifier, name, age, gender, blood group, phone, email, address, last donation date, eligibility status, and registration date.

### Donations

Stores each donation's identifier, related donor, date, blood group, units, status, and remarks. A donor can have multiple donations. Deleting a donor also removes their donation history.

### Blood Inventory

Stores one row for each of A+, A-, B+, B-, AB+, AB-, O+, and O-, with available units and the last update date. Completed donations increase stock; cancelled donations do not.

## 6. Application Workflow

1. Open the dashboard to review donor, donation, and inventory totals.
2. Register a donor with contact and blood group information.
3. Find the donor using search or the blood group filter and open the profile.
4. Record a completed or cancelled donation for a registered donor.
5. Completed donations update the donor's latest donation date, eligibility, and blood inventory.
6. Review the donation history, inventory status, and reports.

## 7. User Interface

The shared navigation bar links to Dashboard, Donors, Donations, Blood Inventory, and Reports. Pages use a light background, red accent color, compact cards, searchable tables, simple forms, and status badges. The layout adjusts for narrow screens.

## 8. Installation

Python 3.9 or later is recommended.

```bash
python -m venv venv
```

Activate the environment on Windows:

```powershell
venv\Scripts\activate
```

On macOS or Linux:

```bash
source venv/bin/activate
```

Install the sole application dependency:

```bash
pip install -r requirements.txt
```

## 9. Running the Website

From the project directory run:

```bash
python app.py
```

Open [http://127.0.0.1:5000/](http://127.0.0.1:5000/) in a normal web browser. The SQLite database and initial blood group rows are created automatically.

## 10. Screenshots

Screenshots can be added after launching the website. Suggested captures:

- Dashboard
- Donor directory and donor profile
- Donation records
- Blood inventory
- Reports

## 11. Future Enhancements

- Pagination for larger donor and donation tables
- Additional validation and audit history for manual stock adjustments
- Optional export of summaries for academic demonstration

These are possible future improvements and are not part of the current system.

## 12. Learning Outcomes

- Python programming and Flask route handling
- Server-rendered pages and template inheritance
- HTML forms, CSS layout, and vanilla JavaScript interactions
- Relational database design and parameterized SQLite queries
- CRUD operations, validation, and basic data consistency

## 13. Author

- Student Name: Your Name
- USN: Your USN
- Course: BCA
- Project: Blood Donor Management System
- Technologies: Python | Flask | SQLite | HTML5 | CSS3 | JavaScript

## 14. License

This project is developed for educational, academic, internship, and portfolio purposes.
