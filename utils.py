"""
Student Management System - Utility Functions
Handles CSV import/export and other helper functions.
"""

import csv
import os
from typing import List, Dict, Any, Optional
from tkinter import filedialog, messagebox
from models import Student

class CSVHandler:
    """
    Handles CSV import and export operations for student data.
    """
    
    @staticmethod
    def export_students_to_csv(students: List[Student], filename: Optional[str] = None) -> str:
        """
        Export students to CSV file.
        
        Args:
            students: List of Student objects to export
            filename: Optional filename, if None will show save dialog
            
        Returns:
            Path to the exported file
            
        Raises:
            Exception: If export fails
        """
        try:
            if filename is None:
                filename = filedialog.asksaveasfilename(
                    defaultextension=".csv",
                    filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
                    title="Export Students to CSV"
                )
                
                if not filename:
                    raise Exception("No file selected for export")
            
            with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
                fieldnames = ['ID', 'Name', 'Roll', 'Department', 'Email', 'Phone']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                
                writer.writeheader()
                for student in students:
                    writer.writerow({
                        'ID': student.id,
                        'Name': student.name,
                        'Roll': student.roll,
                        'Department': student.department,
                        'Email': student.email,
                        'Phone': student.phone
                    })
            
            return filename
            
        except Exception as e:
            raise Exception(f"Failed to export CSV: {str(e)}")
    
    @staticmethod
    def import_students_from_csv(filename: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Import students from CSV file.
        
        Args:
            filename: Optional filename, if None will show open dialog
            
        Returns:
            List of dictionaries containing student data
            
        Raises:
            Exception: If import fails
        """
        try:
            if filename is None:
                filename = filedialog.askopenfilename(
                    filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
                    title="Import Students from CSV"
                )
                
                if not filename:
                    raise Exception("No file selected for import")
            
            if not os.path.exists(filename):
                raise Exception("File does not exist")
            
            students_data = []
            with open(filename, 'r', newline='', encoding='utf-8') as csvfile:
                # Try to detect delimiter
                sample = csvfile.read(1024)
                csvfile.seek(0)
                sniffer = csv.Sniffer()
                delimiter = sniffer.sniff(sample).delimiter
                
                reader = csv.DictReader(csvfile, delimiter=delimiter)
                
                # Check if required columns exist
                required_columns = ['Name', 'Roll', 'Department', 'Email']
                if not all(col in reader.fieldnames for col in required_columns):
                    missing_cols = [col for col in required_columns if col not in reader.fieldnames]
                    raise Exception(f"Missing required columns: {', '.join(missing_cols)}")
                
                for row_num, row in enumerate(reader, start=2):  # Start at 2 because header is row 1
                    try:
                        # Clean and validate data
                        student_data = {
                            'name': row.get('Name', '').strip(),
                            'roll': row.get('Roll', '').strip(),
                            'department': row.get('Department', '').strip(),
                            'email': row.get('Email', '').strip(),
                            'phone': row.get('Phone', '').strip()
                        }
                        
                        # Validate required fields
                        if not student_data['name']:
                            raise ValueError(f"Row {row_num}: Name is required")
                        if not student_data['roll']:
                            raise ValueError(f"Row {row_num}: Roll is required")
                        if not student_data['department']:
                            raise ValueError(f"Row {row_num}: Department is required")
                        if not student_data['email']:
                            raise ValueError(f"Row {row_num}: Email is required")
                        
                        students_data.append(student_data)
                        
                    except Exception as e:
                        raise Exception(f"Error in row {row_num}: {str(e)}")
            
            return students_data
            
        except Exception as e:
            raise Exception(f"Failed to import CSV: {str(e)}")
    
    @staticmethod
    def validate_csv_data(students_data: List[Dict[str, Any]]) -> List[str]:
        """
        Validate imported CSV data and return list of validation errors.
        
        Args:
            students_data: List of student data dictionaries
            
        Returns:
            List of validation error messages
        """
        errors = []
        seen_rolls = set()
        seen_emails = set()
        
        for i, student_data in enumerate(students_data, start=1):
            try:
                # Create temporary Student object to validate
                student = Student(
                    name=student_data['name'],
                    roll=student_data['roll'],
                    department=student_data['department'],
                    email=student_data['email'],
                    phone=student_data.get('phone', '')
                )
                
                # Check for duplicate roll numbers in the import data
                if student.roll in seen_rolls:
                    errors.append(f"Row {i}: Duplicate roll number '{student.roll}' in import data")
                else:
                    seen_rolls.add(student.roll)
                
                # Check for duplicate emails in the import data
                if student.email in seen_emails:
                    errors.append(f"Row {i}: Duplicate email '{student.email}' in import data")
                else:
                    seen_emails.add(student.email)
                    
            except ValueError as e:
                errors.append(f"Row {i}: {str(e)}")
        
        return errors


class ReportGenerator:
    """
    Generates various reports for the student management system.
    """
    
    @staticmethod
    def generate_department_report(students: List[Student]) -> str:
        """
        Generate a text report showing students by department.
        
        Args:
            students: List of Student objects
            
        Returns:
            Formatted report string
        """
        if not students:
            return "No students found."
        
        # Group students by department
        departments = {}
        for student in students:
            if student.department not in departments:
                departments[student.department] = []
            departments[student.department].append(student)
        
        # Generate report
        report = []
        report.append("=" * 60)
        report.append("STUDENT MANAGEMENT SYSTEM - DEPARTMENT REPORT")
        report.append("=" * 60)
        report.append(f"Generated on: {__import__('datetime').datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report.append(f"Total Students: {len(students)}")
        report.append(f"Total Departments: {len(departments)}")
        report.append("")
        
        for department in sorted(departments.keys()):
            dept_students = departments[department]
            report.append(f"DEPARTMENT: {department}")
            report.append("-" * 40)
            report.append(f"Number of Students: {len(dept_students)}")
            report.append("")
            
            for student in sorted(dept_students, key=lambda s: s.name):
                report.append(f"  • {student.name} ({student.roll})")
                report.append(f"    Email: {student.email}")
                if student.phone:
                    report.append(f"    Phone: {student.phone}")
                report.append("")
        
        return "\n".join(report)
    
    @staticmethod
    def generate_summary_report(students: List[Student]) -> str:
        """
        Generate a summary report with statistics.
        
        Args:
            students: List of Student objects
            
        Returns:
            Formatted summary report string
        """
        if not students:
            return "No students found."
        
        # Calculate statistics
        total_students = len(students)
        departments = {}
        for student in students:
            departments[student.department] = departments.get(student.department, 0) + 1
        
        # Generate report
        report = []
        report.append("=" * 50)
        report.append("STUDENT MANAGEMENT SYSTEM - SUMMARY REPORT")
        report.append("=" * 50)
        report.append(f"Generated on: {__import__('datetime').datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report.append("")
        report.append("OVERVIEW:")
        report.append(f"  Total Students: {total_students}")
        report.append(f"  Total Departments: {len(departments)}")
        report.append("")
        report.append("STUDENTS BY DEPARTMENT:")
        report.append("-" * 30)
        
        for department in sorted(departments.keys()):
            count = departments[department]
            percentage = (count / total_students) * 100
            report.append(f"  {department}: {count} students ({percentage:.1f}%)")
        
        return "\n".join(report)


class ValidationHelper:
    """
    Helper class for various validation operations.
    """
    
    @staticmethod
    def validate_roll_number(roll: str, existing_rolls: List[str], exclude_roll: Optional[str] = None) -> bool:
        """
        Validate if roll number is unique.
        
        Args:
            roll: Roll number to validate
            existing_rolls: List of existing roll numbers
            exclude_roll: Roll number to exclude from check (for updates)
            
        Returns:
            True if roll number is valid (unique)
        """
        if exclude_roll and roll == exclude_roll:
            return True
        return roll not in existing_rolls
    
    @staticmethod
    def validate_email(email: str, existing_emails: List[str], exclude_email: Optional[str] = None) -> bool:
        """
        Validate if email is unique.
        
        Args:
            email: Email to validate
            existing_emails: List of existing emails
            exclude_email: Email to exclude from check (for updates)
            
        Returns:
            True if email is valid (unique)
        """
        if exclude_email and email == exclude_email:
            return True
        return email not in existing_emails
