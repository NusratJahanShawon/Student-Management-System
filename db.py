"""
Student Management System - Database Operations
Handles all SQLite database operations using OOP principles.
"""

import sqlite3
import os
from typing import List, Optional, Dict, Any, Tuple
from models import Student, User

class Database:
    """
    Database class to handle all SQLite operations.
    Implements CRUD operations for students and users.
    """
    
    def __init__(self, db_path: str = "students.db"):
        """
        Initialize database connection.
        
        Args:
            db_path: Path to SQLite database file
        """
        self.db_path = db_path
        self.connection = None
    
    def connect(self) -> sqlite3.Connection:
        """Establish database connection"""
        try:
            self.connection = sqlite3.connect(self.db_path)
            self.connection.row_factory = sqlite3.Row  # Enable column access by name
            return self.connection
        except sqlite3.Error as e:
            raise Exception(f"Database connection failed: {str(e)}")
    
    def disconnect(self):
        """Close database connection"""
        if self.connection:
            self.connection.close()
            self.connection = None
    
    def initialize_database(self):
        """Create database tables if they don't exist"""
        try:
            conn = self.connect()
            cursor = conn.cursor()
            
            # Create students table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS students (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    roll TEXT UNIQUE NOT NULL,
                    department TEXT NOT NULL,
                    email TEXT UNIQUE NOT NULL,
                    phone TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Create users table for authentication
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE NOT NULL,
                    password TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Create index for faster searches
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_students_roll ON students(roll)')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_students_department ON students(department)')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_students_email ON students(email)')
            
            conn.commit()
            
            # Insert default admin user if no users exist
            cursor.execute('SELECT COUNT(*) FROM users')
            if cursor.fetchone()[0] == 0:
                cursor.execute('''
                    INSERT INTO users (username, password) 
                    VALUES (?, ?)
                ''', ('admin', 'admin123'))
                conn.commit()
            
        except sqlite3.Error as e:
            raise Exception(f"Database initialization failed: {str(e)}")
        finally:
            self.disconnect()
    
    # Student CRUD Operations
    
    def add_student(self, student: Student) -> int:
        """
        Add a new student to the database.
        
        Args:
            student: Student object to add
            
        Returns:
            ID of the inserted student
            
        Raises:
            Exception: If student with same roll or email already exists
        """
        try:
            conn = self.connect()
            cursor = conn.cursor()
            
            # Check for duplicate roll number
            cursor.execute('SELECT id FROM students WHERE roll = ?', (student.roll,))
            if cursor.fetchone():
                raise Exception(f"Student with roll number '{student.roll}' already exists")
            
            # Check for duplicate email
            cursor.execute('SELECT id FROM students WHERE email = ?', (student.email,))
            if cursor.fetchone():
                raise Exception(f"Student with email '{student.email}' already exists")
            
            cursor.execute('''
                INSERT INTO students (name, roll, department, email, phone)
                VALUES (?, ?, ?, ?, ?)
            ''', (student.name, student.roll, student.department, student.email, student.phone))
            
            student_id = cursor.lastrowid
            conn.commit()
            return student_id
            
        except sqlite3.Error as e:
            raise Exception(f"Failed to add student: {str(e)}")
        finally:
            self.disconnect()
    
    def get_student(self, student_id: int) -> Optional[Student]:
        """
        Get a student by ID.
        
        Args:
            student_id: ID of the student to retrieve
            
        Returns:
            Student object or None if not found
        """
        try:
            conn = self.connect()
            cursor = conn.cursor()
            
            cursor.execute('SELECT * FROM students WHERE id = ?', (student_id,))
            row = cursor.fetchone()
            
            if row:
                return Student.from_dict(dict(row))
            return None
            
        except sqlite3.Error as e:
            raise Exception(f"Failed to get student: {str(e)}")
        finally:
            self.disconnect()
    
    def get_all_students(self) -> List[Student]:
        """
        Get all students from the database.
        
        Returns:
            List of Student objects
        """
        try:
            conn = self.connect()
            cursor = conn.cursor()
            
            cursor.execute('SELECT * FROM students ORDER BY name')
            rows = cursor.fetchall()
            
            return [Student.from_dict(dict(row)) for row in rows]
            
        except sqlite3.Error as e:
            raise Exception(f"Failed to get students: {str(e)}")
        finally:
            self.disconnect()
    
    def update_student(self, student: Student) -> bool:
        """
        Update an existing student.
        
        Args:
            student: Student object with updated information
            
        Returns:
            True if update was successful
            
        Raises:
            Exception: If student not found or duplicate roll/email
        """
        try:
            conn = self.connect()
            cursor = conn.cursor()
            
            # Check if student exists
            cursor.execute('SELECT id FROM students WHERE id = ?', (student.id,))
            if not cursor.fetchone():
                raise Exception("Student not found")
            
            # Check for duplicate roll number (excluding current student)
            cursor.execute('SELECT id FROM students WHERE roll = ? AND id != ?', (student.roll, student.id))
            if cursor.fetchone():
                raise Exception(f"Student with roll number '{student.roll}' already exists")
            
            # Check for duplicate email (excluding current student)
            cursor.execute('SELECT id FROM students WHERE email = ? AND id != ?', (student.email, student.id))
            if cursor.fetchone():
                raise Exception(f"Student with email '{student.email}' already exists")
            
            cursor.execute('''
                UPDATE students 
                SET name = ?, roll = ?, department = ?, email = ?, phone = ?, updated_at = CURRENT_TIMESTAMP
                WHERE id = ?
            ''', (student.name, student.roll, student.department, student.email, student.phone, student.id))
            
            conn.commit()
            return cursor.rowcount > 0
            
        except sqlite3.Error as e:
            raise Exception(f"Failed to update student: {str(e)}")
        finally:
            self.disconnect()
    
    def delete_student(self, student_id: int) -> bool:
        """
        Delete a student by ID.
        
        Args:
            student_id: ID of the student to delete
            
        Returns:
            True if deletion was successful
        """
        try:
            conn = self.connect()
            cursor = conn.cursor()
            
            cursor.execute('DELETE FROM students WHERE id = ?', (student_id,))
            conn.commit()
            
            return cursor.rowcount > 0
            
        except sqlite3.Error as e:
            raise Exception(f"Failed to delete student: {str(e)}")
        finally:
            self.disconnect()
    
    def search_students(self, query: str) -> List[Student]:
        """
        Search students by name, roll, department, or email.
        
        Args:
            query: Search query string
            
        Returns:
            List of matching Student objects
        """
        try:
            conn = self.connect()
            cursor = conn.cursor()
            
            search_pattern = f"%{query}%"
            cursor.execute('''
                SELECT * FROM students 
                WHERE name LIKE ? OR roll LIKE ? OR department LIKE ? OR email LIKE ?
                ORDER BY name
            ''', (search_pattern, search_pattern, search_pattern, search_pattern))
            
            rows = cursor.fetchall()
            return [Student.from_dict(dict(row)) for row in rows]
            
        except sqlite3.Error as e:
            raise Exception(f"Failed to search students: {str(e)}")
        finally:
            self.disconnect()
    
    def get_students_by_department(self, department: str) -> List[Student]:
        """
        Get all students from a specific department.
        
        Args:
            department: Department name
            
        Returns:
            List of Student objects from the department
        """
        try:
            conn = self.connect()
            cursor = conn.cursor()
            
            cursor.execute('SELECT * FROM students WHERE department = ? ORDER BY name', (department,))
            rows = cursor.fetchall()
            
            return [Student.from_dict(dict(row)) for row in rows]
            
        except sqlite3.Error as e:
            raise Exception(f"Failed to get students by department: {str(e)}")
        finally:
            self.disconnect()
    
    def get_departments(self) -> List[str]:
        """
        Get list of all departments.
        
        Returns:
            List of unique department names
        """
        try:
            conn = self.connect()
            cursor = conn.cursor()
            
            cursor.execute('SELECT DISTINCT department FROM students ORDER BY department')
            rows = cursor.fetchall()
            
            return [row[0] for row in rows]
            
        except sqlite3.Error as e:
            raise Exception(f"Failed to get departments: {str(e)}")
        finally:
            self.disconnect()
    
    def get_student_count_by_department(self) -> Dict[str, int]:
        """
        Get count of students per department.
        
        Returns:
            Dictionary with department names as keys and counts as values
        """
        try:
            conn = self.connect()
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT department, COUNT(*) as count 
                FROM students 
                GROUP BY department 
                ORDER BY department
            ''')
            rows = cursor.fetchall()
            
            return {row[0]: row[1] for row in rows}
            
        except sqlite3.Error as e:
            raise Exception(f"Failed to get student count by department: {str(e)}")
        finally:
            self.disconnect()
    
    # User Authentication Operations
    
    def authenticate_user(self, username: str, password: str) -> bool:
        """
        Authenticate user login.
        
        Args:
            username: Username
            password: Password
            
        Returns:
            True if authentication successful
        """
        try:
            conn = self.connect()
            cursor = conn.cursor()
            
            cursor.execute('SELECT id FROM users WHERE username = ? AND password = ?', (username, password))
            return cursor.fetchone() is not None
            
        except sqlite3.Error as e:
            raise Exception(f"Authentication failed: {str(e)}")
        finally:
            self.disconnect()
    
    def add_user(self, user: User) -> int:
        """
        Add a new user to the database.
        
        Args:
            user: User object to add
            
        Returns:
            ID of the inserted user
        """
        try:
            conn = self.connect()
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO users (username, password)
                VALUES (?, ?)
            ''', (user.username, user.password))
            
            user_id = cursor.lastrowid
            conn.commit()
            return user_id
            
        except sqlite3.Error as e:
            raise Exception(f"Failed to add user: {str(e)}")
        finally:
            self.disconnect()
    
    def get_user_count(self) -> int:
        """
        Get total number of users.
        
        Returns:
            Number of users in the database
        """
        try:
            conn = self.connect()
            cursor = conn.cursor()
            
            cursor.execute('SELECT COUNT(*) FROM users')
            return cursor.fetchone()[0]
            
        except sqlite3.Error as e:
            raise Exception(f"Failed to get user count: {str(e)}")
        finally:
            self.disconnect()
