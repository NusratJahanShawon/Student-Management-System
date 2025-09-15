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

### Installation Steps

1. **Clone or download the project files**
   ```bash
   # If using git
   git clone <repository-url>
   cd student-management-system
   ```

2. **Run the application**
   ```bash
   python main.py
   ```

3. **Default Login Credentials**
   - Username: `admin`
   - Password: `admin123`

## 📖 Usage Guide

### 1. Login
- Launch the application using `python main.py`
- Enter the default credentials or create new users
- Click "Login" to access the main dashboard

### 2. Managing Students

#### Adding a Student
1. Click "Add Student" button
2. Fill in the required fields:
   - **Name**: Student's full name
   - **Roll Number**: Unique identifier (letters, numbers, hyphens, underscores allowed)
   - **Department**: Student's department
   - **Email**: Valid email address
   - **Phone**: Phone number (optional)
3. Click "Save" to add the student

#### Editing a Student
1. Select a student from the table
2. Click "Edit Student" button
3. Modify the required fields
4. Click "Save" to update

#### Deleting a Student
1. Select a student from the table
2. Click "Delete Student" button
3. Confirm the deletion

### 3. Search Functionality
- Use the search box to find students by:
  - Name
  - Roll number
  - Department
  - Email address
- Search is performed in real-time as you type
- Click "Clear" to reset the search

### 4. CSV Operations

#### Exporting Data
1. Go to **File** → **Export to CSV**
2. Choose a location and filename
3. All student data will be exported to CSV format

#### Importing Data
1. Go to **File** → **Import from CSV**
2. Select a CSV file with the following columns:
   - Name (required)
   - Roll (required)
   - Department (required)
   - Email (required)
   - Phone (optional)
3. The system will validate the data before importing

### 5. Reports
- **Department Report**: Detailed report showing all students by department
- **Summary Report**: Statistical overview with department-wise counts

## 🏗️ Architecture & Design Patterns

### Object-Oriented Design
- **Student Class**: Encapsulates student data with validation
- **User Class**: Handles user authentication
- **Database Class**: Manages all database operations
- **GUI Classes**: Separate classes for different UI components

### Key Design Principles
- **Encapsulation**: Private attributes with public properties
- **Single Responsibility**: Each class has a specific purpose
- **Error Handling**: Comprehensive exception handling
- **Data Validation**: Input validation at multiple levels

### Database Schema
```sql
-- Students table
CREATE TABLE students (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    roll TEXT UNIQUE NOT NULL,
    department TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    phone TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Users table
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

## 🔧 Technical Features

### Data Validation
- **Name**: Non-empty, title case formatting
- **Roll Number**: Alphanumeric with hyphens/underscores, unique
- **Department**: Non-empty, title case formatting
- **Email**: Valid email format, unique
- **Phone**: Optional, various international formats

### Error Handling
- Database connection errors
- Validation errors with user-friendly messages
- File operation errors
- Network-related errors (if applicable)

### Performance Optimizations
- Database indexing for faster searches
- Efficient Treeview updates
- Lazy loading of data
- Memory-efficient data structures

## 🎯 Learning Outcomes

This project demonstrates:

1. **GUI Programming**: Tkinter widgets, layouts, event handling
2. **OOP Concepts**: Classes, inheritance, encapsulation, polymorphism
3. **Database Operations**: SQLite CRUD operations, transactions
4. **File Handling**: CSV import/export, data validation
5. **Error Handling**: Try-catch blocks, user feedback
6. **Software Architecture**: Modular design, separation of concerns

## 🚀 Future Enhancements

Potential improvements for advanced learning:

1. **Enhanced Security**: Password hashing, session management
2. **Advanced Reports**: PDF generation, charts and graphs
3. **Data Backup**: Automated backup functionality
4. **Multi-user Support**: Role-based access control
5. **API Integration**: REST API for web interface
6. **Advanced Search**: Filters, sorting options
7. **Data Visualization**: Charts and graphs for statistics

## 🐛 Troubleshooting

### Common Issues

1. **Database Connection Error**
   - Ensure SQLite is properly installed
   - Check file permissions in the project directory

2. **Import/Export Issues**
   - Verify CSV file format matches expected columns
   - Check file permissions for read/write access

3. **GUI Not Displaying**
   - Ensure tkinter is installed: `python -m tkinter`
   - Check Python version compatibility

### Getting Help
- Check the error messages in the application
- Verify all required fields are filled
- Ensure unique constraints (roll number, email) are not violated

## 📝 License

This project is created for educational purposes. Feel free to use, modify, and distribute for learning.

---

**Happy Coding! 🎓**
