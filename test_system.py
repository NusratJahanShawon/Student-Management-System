"""
Test script for Student Management System
Tests core functionality without GUI.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from models import Student, User
from db import Database
from utils import CSVHandler, ReportGenerator

def test_models():
    """Test Student and User model classes"""
    print("Testing Models...")
    
    # Test Student creation
    try:
        student = Student("John Doe", "CS001", "Computer Science", "john@example.com", "123-456-7890")
        print(f"✓ Student created: {student}")
        
        # Test validation
        try:
            invalid_student = Student("", "CS002", "CS", "invalid-email", "")
            print("✗ Validation should have failed")
        except ValueError as e:
            print(f"✓ Validation working: {e}")
        
        # Test to_dict and from_dict
        student_dict = student.to_dict()
        student_from_dict = Student.from_dict(student_dict)
        print(f"✓ Serialization working: {student_from_dict}")
        
    except Exception as e:
        print(f"✗ Model test failed: {e}")
    
    print()

def test_database():
    """Test database operations"""
    print("Testing Database...")
    
    try:
        # Initialize database
        db = Database("test_students.db")
        db.initialize_database()
        print("✓ Database initialized")
        
        # Test user authentication
        auth_result = db.authenticate_user("admin", "admin123")
        print(f"✓ Authentication test: {auth_result}")
        
        # Test student operations
        student = Student("Test Student", "TEST001", "Test Department", "test@example.com", "123-456-7890")
        
        # Add student
        student_id = db.add_student(student)
        print(f"✓ Student added with ID: {student_id}")
        
        # Get student
        retrieved_student = db.get_student(student_id)
        print(f"✓ Student retrieved: {retrieved_student}")
        
        # Update student
        updated_student = Student("Updated Student", "TEST001", "Updated Department", "updated@example.com", "987-654-3210", student_id)
        db.update_student(updated_student)
        print("✓ Student updated")
        
        # Search students
        search_results = db.search_students("Test")
        print(f"✓ Search results: {len(search_results)} students found")
        
        # Get all students
        all_students = db.get_all_students()
        print(f"✓ All students retrieved: {len(all_students)} students")
        
        # Delete student
        db.delete_student(student_id)
        print("✓ Student deleted")
        
        # Clean up test database
        os.remove("test_students.db")
        print("✓ Test database cleaned up")
        
    except Exception as e:
        print(f"✗ Database test failed: {e}")
    
    print()

def test_utils():
    """Test utility functions"""
    print("Testing Utils...")
    
    try:
        # Test report generation
        students = [
            Student("Alice", "CS001", "Computer Science", "alice@example.com"),
            Student("Bob", "CS002", "Computer Science", "bob@example.com"),
            Student("Charlie", "EE001", "Electrical Engineering", "charlie@example.com")
        ]
        
        # Test department report
        dept_report = ReportGenerator.generate_department_report(students)
        print("✓ Department report generated")
        
        # Test summary report
        summary_report = ReportGenerator.generate_summary_report(students)
        print("✓ Summary report generated")
        
        # Test CSV validation
        csv_data = [
            {"name": "Test Student", "roll": "TEST001", "department": "Test Dept", "email": "test@example.com", "phone": "123-456-7890"}
        ]
        
        errors = CSVHandler.validate_csv_data(csv_data)
        print(f"✓ CSV validation working: {len(errors)} errors found")
        
    except Exception as e:
        print(f"✗ Utils test failed: {e}")
    
    print()

def main():
    """Run all tests"""
    print("=" * 50)
    print("STUDENT MANAGEMENT SYSTEM - TEST SUITE")
    print("=" * 50)
    print()
    
    test_models()
    test_database()
    test_utils()
    
    print("=" * 50)
    print("TEST SUITE COMPLETED")
    print("=" * 50)

if __name__ == "__main__":
    main()
