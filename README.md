# Library Management System (LMS)

## Overview

Library Management System (LMS) is a backend application built using FastAPI and SQLAlchemy for managing schools, libraries, books, inventory, stock requests, book issues, returns, reports, and notifications.

The system is designed with a modular and scalable architecture suitable for educational institutions.

---

## Features

### School Management

* Create Schools
* Update Schools
* Retrieve School Information

### Branch Management

* Create Branches
* Manage Multiple Branches per School

### Library Structure Management

* Libraries
* Floors
* Racks
* Shelves
* Rows

### Book Management

* Book Categories
* Book Creation
* Product IDs
* ISBN Management

### Book Copy Management

* Barcode Generation
* Accession Numbers
* Copy Tracking
* Location Assignment

### Inventory Management

* Available Copies
* Lost Copies
* Damaged Copies
* Reserved Copies
* Low Stock Alerts

### Book Issue & Return

* Issue Books to Students
* Issue Books to Employees
* Return Books
* Fine Tracking
* Overdue Tracking

### Stock Request Management

* Create Stock Requests
* Approve Requests
* Reject Requests
* Complete Requests
* Automatic Inventory Updates

### Reports

* Issue Reports
* Inventory Reports
* Overdue Reports
* Return Reports
* Fine Reports
* Dashboard Reports

### Notifications

* Stock Notifications
* System Notifications

---

## Technology Stack

* FastAPI
* SQLAlchemy
* Pydantic
* MySQL
* Uvicorn
* AWS S3
* Git & GitHub

---

## Project Structure

```text
app/
├── models/
├── schemas/
├── services/
├── routers/
├── database/
├── utilities/
└── uploads/

main.py
requirements.txt
README.md
```

---

## Installation

Clone the repository:

```bash
git clone https://github.com/Ananthbheemiredd/lms-backend.git
```

Move into the project folder:

```bash
cd lms-backend
```

Create virtual environment:

```bash
python -m venv venv
```

Activate virtual environment:

```bash
venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the application:

```bash
uvicorn main:app --reload
```

---

## API Documentation

Swagger UI:

```text
http://localhost:8000/docs
```

ReDoc:

```text
http://localhost:8000/redoc
```

---

## Future Enhancements

* Stock Transaction Management
* Fine Management Module
* JWT Authentication
* Role Based Access Control
* Docker Deployment
* Audit Logs
* Dashboard Analytics

---

## Author

Ananth

Backend Developer

Built using FastAPI and SQLAlchemy.
