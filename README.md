# BLOOD DONOR MANAGEMENT SYSTEM

**Project README / Reference Document**

## Blood Donor Management System

A web-based Blood Donor Management System developed using Python, Flask, SQLite, HTML5, CSS3, and JavaScript. The application helps manage blood donors, blood donations, blood inventory, donor eligibility, donor records, donation records, and reports through a professional web interface.

The system stores donor and donation information in SQLite and provides tools for searching donors, filtering records, recording donations, updating blood inventory, checking donor eligibility, and viewing reports.

---

## Features

- Donor Management
- Add New Donor
- View Donor Records
- Search and Filter Donors
- View Individual Donor Details
- Edit Donor Information
- Delete Donor Records
- Blood Group Management
- Donation Management
- Record Blood Donations
- View Donation Records
- Complete Donation Records
- Cancel Donation Records
- Donor Eligibility Checking
- Donation History
- Blood Inventory Management
- Add Blood Inventory
- Update Blood Stock
- Blood Group-wise Inventory Tracking
- Inventory Validation
- Reports and Summary Information
- Dashboard with System Statistics
- Persistent SQLite Database Storage
- Form Validation
- Dependency-Aware Record Handling
- Professional Dark-Themed Web Interface

---

## Tech Stack

### Frontend

- HTML5
- CSS3
- JavaScript
- Jinja2 Templates

### Backend

- Python
- Flask

### Database

- SQLite

---

## Project Structure

```text
Blood-Donor-Management-System/
│── app.py
│── requirements.txt
│── README.md
│── .gitignore
│── .gitattributes
│
├── database.db                  # SQLite database
│
├── static/
│   ├── script.js
│   └── style.css
│
└── templates/
    ├── add_donation.html
    ├── add_donor.html
    ├── add_inventory.html
    ├── base.html
    ├── donations.html
    ├── donor_details.html
    ├── donors.html
    ├── index.html
    ├── inventory.html
    └── reports.html
```

---

## Database Tables

The system uses SQLite to store donor information, donation records, blood inventory, and related application data.

### Donor Table

| Field | Description |
|---|---|
| Donor ID | Unique donor identifier |
| Name | Donor name |
| Blood Group | Donor's blood group |
| Age | Donor age |
| Gender | Donor gender |
| Phone | Donor contact number |
| Email | Donor email address |
| Address | Donor address |
| Eligibility | Current donation eligibility status |

### Donation Table

| Field | Description |
|---|---|
| Donation ID | Unique donation identifier |
| Donor ID | Donor associated with the donation |
| Donation Date | Date of donation |
| Blood Group | Blood group associated with the donation |
| Quantity | Quantity of blood donated |
| Status | Current donation status |

Each donation connects a donor with a blood donation record and stores the relevant donation information.

### Blood Inventory Table

| Field | Description |
|---|---|
| Inventory ID | Unique inventory identifier |
| Blood Group | Blood group stored in inventory |
| Quantity | Available blood quantity |
| Last Updated | Date/time of the latest inventory update |

The inventory records track the available quantity for each blood group.

### Blood Group Data

The system supports the standard eight blood groups:

- A+
- A-
- B+
- B-
- AB+
- AB-
- O+
- O-

---

## Blood Donation Rules

Before a donation is recorded, the system checks the available donor and donation information.

The system considers:

- Donor records must contain valid required information.
- Blood group information must be valid.
- Donation records must be associated with an existing donor.
- Donor eligibility must be checked before recording a donation.
- Donation quantity must be valid.
- Donation status must be maintained correctly.
- Completed donations affect the corresponding blood inventory.
- Cancelled donations do not remain counted as completed donations.
- Inventory quantities are updated according to completed donation records.
- Donor donation history is maintained for reference.

The application validates the donation workflow before updating related records.

---

## Application Workflow

1. Open the Blood Donor Management System
2. View the Dashboard
3. Add Donor Information
4. View Donor Records
5. Search or Filter Donors
6. Open Individual Donor Details
7. Check Donor Eligibility
8. Record a Blood Donation
9. Complete or Cancel the Donation
10. Update Blood Inventory
11. View Donation History
12. View Blood Inventory
13. View Reports
14. Review System Statistics
15. Edit or Delete Records When Required

---

## Working Flow

```text
Donor Registration
        ↓
Donor Information
        ↓
Blood Group and Eligibility Check
        ↓
Donation Record
        ↓
Donation Status
        ↓
Completed Donation
        ↓
Blood Inventory Update
        ↓
Donation History
        ↓
Reports and Dashboard Statistics
```

---

## Blood Donation Process

### 1. Register a Donor

The system stores the donor's required personal and blood group information.

The donor record can later be searched, viewed, edited, or deleted.

### 2. Check Donor Eligibility

The application checks the donor's available information before allowing the donation workflow to proceed.

Eligibility information is maintained with the donor record.

### 3. Create a Donation Record

A donation record is created with the donor, donation date, blood group, quantity, and current status.

### 4. Complete or Cancel the Donation

A donation can be completed or cancelled according to the application workflow.

Completed donations are treated as actual blood donations and are reflected in inventory-related records.

### 5. Update Blood Inventory

When a donation is completed, the corresponding blood group inventory is updated.

The inventory section provides a blood-group-wise view of available stock.

### 6. View Donation History

The donation records page provides a history of recorded donations and their current status.

### 7. Generate Reports

The reports section provides summary information from donor, donation, and inventory records.

---

## Donor Management

The donor management section provides tools for maintaining donor information.

It supports:

- Adding donors
- Viewing donors
- Searching donors
- Filtering donors
- Viewing donor details
- Editing donor information
- Deleting donor records
- Viewing donor donation history
- Checking donor eligibility

The individual donor details page provides a focused view of the donor's information and associated donation records.

---

## Donation Management

The donation management section is used to maintain blood donation records.

It supports:

- Creating donation records
- Viewing donation records
- Tracking donation status
- Completing donations
- Cancelling donations
- Maintaining donation history
- Updating related blood inventory

The system keeps donation records associated with the corresponding donor.

---

## Blood Inventory Management

The inventory section maintains blood stock information for the supported blood groups.

It provides:

- Blood group-wise inventory
- Available quantity tracking
- Adding inventory records
- Updating inventory information
- Inventory summary information
- Blood stock visibility through the web interface

The inventory data is stored persistently in SQLite.

---

## Reports

The reports section provides information derived from the system records.

Reports can be used to review:

- Total donors
- Donation information
- Blood group information
- Inventory information
- Donation status
- Blood stock information
- Overall system statistics

---

## Dashboard

The dashboard provides a summary of the Blood Donor Management System.

It presents important system information such as:

- Total number of donors
- Donation statistics
- Blood inventory information
- Blood group information
- System summaries

The dashboard acts as the main entry point for the application.

---

## User Interface

The application interface includes:

- Navigation Area
- Dashboard
- Summary Cards
- Donor Management Tables
- Add Donor Form
- Donor Details Page
- Donation Management Tables
- Add Donation Form
- Inventory Management
- Add Inventory Form
- Reports Page
- Search Controls
- Filter Controls
- Status Indicators
- Eligibility Information
- Validation Messages
- Donation History
- Blood Inventory Summary
- Professional Dark-Themed Layout

---

## Data Integrity

The application maintains consistency between donor, donation, and inventory information.

The system includes:

- SQLite persistent storage
- Form validation
- Donor-to-donation relationships
- Donation status tracking
- Inventory updates based on donation workflow
- Validation of required form values
- Database-backed record management
- Record editing and deletion
- Application-level handling of related records

---

## Installation

### 1. Clone the Project

```bash
git clone https://github.com/likithp-2k6/Blood-Donor-Management-System.git
cd Blood-Donor-Management-System
```

### 2. Create a Virtual Environment

```bash
python -m venv .venv
```

### 3. Activate the Virtual Environment

#### Windows

```bash
.venv\Scripts\activate
```

#### Linux / macOS

```bash
source .venv/bin/activate
```

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

The project uses Flask as its main Python web framework dependency.

### 5. Run the Application

```bash
python app.py
```

### 6. Open the Application

Open the local Flask address shown in the terminal, normally:

```text
http://127.0.0.1:5000/
```

The SQLite database is used by the application for persistent donor, donation, and inventory data.

---

## Screenshots

Add screenshots of the main application pages inside a `screenshots` folder and update the paths below if required.


![Dashboard](https://github.com/likithp-2k6/Blood-Donor-Management-System/blob/main/Screenshots/Dashboard.png)

![Donors](https://github.com/likithp-2k6/Blood-Donor-Management-System/blob/main/Screenshots/Donors.png)

![Donations](https://github.com/likithp-2k6/Blood-Donor-Management-System/blob/main/Screenshots/Donations.png)

![Inventory](https://github.com/likithp-2k6/Blood-Donor-Management-System/blob/main/Screenshots/Inventory.png)
---

## Future Enhancements

- User Login and Authentication
- Administrator and Staff Roles
- Donor Login
- Blood Request Management
- Blood Recipient Management
- Hospital / Blood Bank Management
- Blood Request Matching
- Donor Notifications
- Email Notifications
- SMS Notifications
- Appointment Scheduling
- Advanced Donor Eligibility Rules
- Blood Expiry Tracking
- Blood Stock Alerts
- Advanced Reports
- Report Export
- Excel Export
- PDF Report Generation
- REST API Support
- Cloud Database Deployment
- Online Deployment

---

## Learning Outcomes

- Python programming
- Flask web application development
- SQLite database design
- Relational database concepts
- HTML and CSS
- JavaScript
- Jinja2 templating
- CRUD operations
- Form handling
- Form validation
- Database operations
- Data relationship management
- Blood donation workflow implementation
- Inventory management
- Report generation
- Full-stack web application development

---

## Author

**Student Name:** [Your Name]  
**USN:** [Your USN]  
**Course:** BCA  
**Project:** Blood Donor Management System

**Technologies:**  
Python | Flask | SQLite | HTML | CSS | JavaScript | Jinja2

---

## GitHub

https://github.com/likithp-2k6/Blood-Donor-Management-System

---

## License

This project is developed for educational, academic, internship, and portfolio purposes.
