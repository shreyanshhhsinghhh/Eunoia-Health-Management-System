# Eunoia Health Management System

A desktop-based clinic management system built with Python, CustomTkinter, and MySQL. Eunoia brings patient records, appointments, inventory, billing, and basic analytics into one application designed for small clinics.

## Features

- **Dashboard:** Revenue summaries, patient statistics, appointment counts, and payment analytics.
- **Patient Management:** Add, view, update, and delete patient records.
- **Doctor Management:** Maintain doctor profiles, specializations, contact details, and availability.
- **Appointment Management:** Manage patient appointments, dates, times, and statuses.
- **Inventory Management:** Track medical supplies and highlight low-stock items.
- **Billing:** Record consultation fees, medicine costs, totals, and payment status.
- **PDF Generation:** Generate PDF bills for individual records.
- **Visual Analytics:** Charts for revenue, patients, appointments, and payment status.

## Technology Stack

- Python 3.12
- CustomTkinter
- MySQL
- Matplotlib
- ReportLab
- Pillow

## Project Structure

- `test.py` — Application entry point
- `db.py` — Database connection
- `patient.py` — Patient operations
- `doctor.py` — Doctor operations
- `appointments.py` — Appointment operations
- `inventory.py` — Inventory operations
- `billing.py` — Billing operations
- `database_schema.sql` — Database table definitions
- `logo.png` and `logo.ico` — Application assets

## Prerequisites

- Python 3.12
- MySQL Server

## Setup

1. Clone or download this repository.
2. Create a Python virtual environment:

   ```bash
   python -m venv .venv
   ```

3. Activate the environment on Windows:

   ```powershell
   .\.venv\Scripts\Activate.ps1
   ```

4. Install the dependencies:

   ```bash
   pip install -r requirements.txt
   ```

5. Create the database and tables using `database_schema.sql`.
6. Configure your local MySQL connection in `db.py` without committing credentials.
7. Launch the application:

   ```bash
   python test.py
   ```

## Security and Privacy

This project is intended for demonstration and educational purposes. Do not commit database passwords, application credentials, real patient records, or generated bills. Use fictional data when demonstrating the application.

## Future Improvements

Potential improvements include stronger authentication, input validation, automated tests, and improved database relationship constraints.

## Author

Developed as a personal Python and database project.