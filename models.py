"""
Student Management System - Models
Contains the Student class and related data models.
"""

from typing import Optional, Dict, Any
import re

class Student:
    """
    Student class representing a student with all their attributes.
    Implements encapsulation and validation.
    """
    
    def __init__(self, name: str, roll: str, department: str, email: str, phone: str = "", student_id: Optional[int] = None):
        """
        Initialize a Student object with validation.
        
        Args:
            name: Student's full name
            roll: Student's roll number (must be unique)
            department: Student's department
            email: Student's email address
            phone: Student's phone number (optional)
            student_id: Database ID (None for new students)
        """
        self._id = student_id
        self._name = self._validate_name(name)
        self._roll = self._validate_roll(roll)
        self._department = self._validate_department(department)
        self._email = self._validate_email(email)
        self._phone = self._validate_phone(phone)
    
    @property
    def id(self) -> Optional[int]:
        """Get student ID"""
        return self._id
    
    @property
    def name(self) -> str:
        """Get student name"""
        return self._name
    
    @property
    def roll(self) -> str:
        """Get student roll number"""
        return self._roll
    
    @property
    def department(self) -> str:
        """Get student department"""
        return self._department
    
    @property
    def email(self) -> str:
        """Get student email"""
        return self._email
    
    @property
    def phone(self) -> str:
        """Get student phone"""
        return self._phone
    
    def _validate_name(self, name: str) -> str:
        """Validate and clean student name"""
        if not name or not name.strip():
            raise ValueError("Name cannot be empty")
        return name.strip().title()
    
    def _validate_roll(self, roll: str) -> str:
        """Validate roll number format"""
        if not roll or not roll.strip():
            raise ValueError("Roll number cannot be empty")
        roll = roll.strip().upper()
        if not re.match(r'^[A-Z0-9\-_]+$', roll):
            raise ValueError("Roll number can only contain letters, numbers, hyphens, and underscores")
        return roll
    
    def _validate_department(self, department: str) -> str:
        """Validate department name"""
        if not department or not department.strip():
            raise ValueError("Department cannot be empty")
        return department.strip().title()
    
    def _validate_email(self, email: str) -> str:
        """Validate email format"""
        if not email or not email.strip():
            raise ValueError("Email cannot be empty")
        email = email.strip().lower()
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_pattern, email):
            raise ValueError("Invalid email format")
        return email
    
    def _validate_phone(self, phone: str) -> str:
        """Validate phone number format"""
        if not phone:
            return ""
        phone = phone.strip()
        # Allow various phone formats
        phone_pattern = r'^[\+]?[0-9\s\-\(\)]{7,15}$'
        if not re.match(phone_pattern, phone):
            raise ValueError("Invalid phone number format")
        return phone
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert student object to dictionary for database operations"""
        return {
            'id': self._id,
            'name': self._name,
            'roll': self._roll,
            'department': self._department,
            'email': self._email,
            'phone': self._phone
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Student':
        """Create Student object from dictionary (from database)"""
        return cls(
            name=data['name'],
            roll=data['roll'],
            department=data['department'],
            email=data['email'],
            phone=data.get('phone', ''),
            student_id=data['id']
        )
    
    def __str__(self) -> str:
        """String representation of Student"""
        return f"Student({self._roll}: {self._name}, {self._department})"
    
    def __repr__(self) -> str:
        """Detailed string representation of Student"""
        return f"Student(id={self._id}, name='{self._name}', roll='{self._roll}', department='{self._department}', email='{self._email}', phone='{self._phone}')"


class User:
    """
    User class for authentication.
    Simple user model for login functionality.
    """
    
    def __init__(self, username: str, password: str, user_id: Optional[int] = None):
        """
        Initialize a User object.
        
        Args:
            username: Username for login
            password: Password (will be hashed)
            user_id: Database ID (None for new users)
        """
        self._id = user_id
        self._username = self._validate_username(username)
        self._password = password  # In a real app, this should be hashed
    
    @property
    def id(self) -> Optional[int]:
        """Get user ID"""
        return self._id
    
    @property
    def username(self) -> str:
        """Get username"""
        return self._username
    
    @property
    def password(self) -> str:
        """Get password"""
        return self._password
    
    def _validate_username(self, username: str) -> str:
        """Validate username"""
        if not username or not username.strip():
            raise ValueError("Username cannot be empty")
        username = username.strip()
        if len(username) < 3:
            raise ValueError("Username must be at least 3 characters long")
        return username
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert user object to dictionary for database operations"""
        return {
            'id': self._id,
            'username': self._username,
            'password': self._password
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'User':
        """Create User object from dictionary (from database)"""
        return cls(
            username=data['username'],
            password=data['password'],
            user_id=data['id']
        )
