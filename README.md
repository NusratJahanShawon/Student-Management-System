# Student Management System (SMS)

A comprehensive desktop application built with Python Tkinter, applying Object-Oriented Programming principles, and using SQLite for database storage.

## 🚀 Features

### Core Functionality
- **User Authentication**: Secure login system with username/password
- **Student CRUD Operations**: Create, Read, Update, Delete student records
- **Data Validation**: Comprehensive validation for all student fields
- **Search Functionality**: Search students by name, roll number, department, or email
- **Duplicate Prevention**: Prevents duplicate roll numbers and email addresses

### Advanced Features
- **CSV Import/Export**: Import student data from CSV files and export to CSV
- **Report Generation**: Generate department-wise and summary reports
- **Modern GUI**: Clean and intuitive Tkinter interface with Treeview tables
- **Error Handling**: Comprehensive error handling and user feedback
- **Data Persistence**: SQLite database for reliable data storage

### Technical Implementation
- **Object-Oriented Design**: Proper class structure with encapsulation
- **Database Operations**: Full CRUD operations with SQLite
- **File Handling**: CSV import/export with validation
- **Input Validation**: Real-time validation with user-friendly error messages

## 📂 Project Structure

```
student_management/
│
├── main.py              # Application entry point
├── models.py            # Student and User model classes
├── db.py               # Database operations class
├── gui.py              # Main GUI application
├── utils.py            # Utility functions (CSV, reports)
├── students.db         # SQLite database (created automatically)
└── README.md           # This file
```

## 🛠️ Installation & Setup

### Prerequisites
- Python 3.7 or higher
- tkinter (usually included with Python)
- sqlite3 (usually included with Python)


