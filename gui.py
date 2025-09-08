"""
Student Management System - GUI Application
Main Tkinter GUI application with login, dashboard, and student management features.
"""

import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from typing import List, Optional, Dict, Any
import threading
from datetime import datetime

from models import Student
from db import Database
from utils import CSVHandler, ReportGenerator, ValidationHelper

class LoginWindow:
    """
    Login window for user authentication.
    """
    
    def __init__(self, parent, on_login_success):
        """
        Initialize login window.
        
        Args:
            parent: Parent window
            on_login_success: Callback function when login is successful
        """
        self.parent = parent
        self.on_login_success = on_login_success
        self.window = None
        self.db = Database()
        
    def show(self):
        """Show the login window"""
        self.window = tk.Toplevel(self.parent)
        self.window.title("Student Management System - Login")
        self.window.geometry("400x300")
        self.window.resizable(False, False)
        self.window.transient(self.parent)
        self.window.grab_set()
        
        # Center the window
        self.window.update_idletasks()
        x = (self.window.winfo_screenwidth() // 2) - (400 // 2)
        y = (self.window.winfo_screenheight() // 2) - (300 // 2)
        self.window.geometry(f"400x300+{x}+{y}")
        
        self._create_widgets()
        
    def _create_widgets(self):
        """Create login form widgets"""
        # Main frame
        main_frame = ttk.Frame(self.window, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Title
        title_label = ttk.Label(main_frame, text="Student Management System", 
                               font=("Arial", 16, "bold"))
        title_label.pack(pady=(0, 20))
        
        # Login form frame
        form_frame = ttk.LabelFrame(main_frame, text="Login", padding="15")
        form_frame.pack(fill=tk.X, pady=(0, 20))
        
        # Username
        ttk.Label(form_frame, text="Username:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.username_var = tk.StringVar()
        username_entry = ttk.Entry(form_frame, textvariable=self.username_var, width=25)
        username_entry.grid(row=0, column=1, pady=5, padx=(10, 0))
        
        # Password
        ttk.Label(form_frame, text="Password:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.password_var = tk.StringVar()
        password_entry = ttk.Entry(form_frame, textvariable=self.password_var, 
                                  show="*", width=25)
        password_entry.grid(row=1, column=1, pady=5, padx=(10, 0))
        
        # Buttons frame
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X)
        
        # Login button
        login_btn = ttk.Button(button_frame, text="Login", command=self._login)
        login_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        # Cancel button
        cancel_btn = ttk.Button(button_frame, text="Cancel", command=self._cancel)
        cancel_btn.pack(side=tk.LEFT)
        
        # Default credentials info
        info_label = ttk.Label(main_frame, 
                              text="Default credentials: admin / admin123",
                              font=("Arial", 9), foreground="gray")
        info_label.pack(pady=(10, 0))
        
        # Bind Enter key to login
        self.window.bind('<Return>', lambda e: self._login())
        
        # Focus on username entry
        username_entry.focus()
        
    def _login(self):
        """Handle login button click"""
        username = self.username_var.get().strip()
        password = self.password_var.get().strip()
        
        if not username or not password:
            messagebox.showerror("Error", "Please enter both username and password")
            return
        
        try:
            if self.db.authenticate_user(username, password):
                self.window.destroy()
                self.on_login_success()
            else:
                messagebox.showerror("Error", "Invalid username or password")
        except Exception as e:
            messagebox.showerror("Error", f"Login failed: {str(e)}")
    
    def _cancel(self):
        """Handle cancel button click"""
        self.window.destroy()
        self.parent.quit()


class StudentForm:
    """
    Student form dialog for adding/editing students.
    """
    
    def __init__(self, parent, student: Optional[Student] = None, on_save=None):
        """
        Initialize student form.
        
        Args:
            parent: Parent window
            student: Student object to edit (None for new student)
            on_save: Callback function when form is saved
        """
        self.parent = parent
        self.student = student
        self.on_save = on_save
        self.window = None
        self.is_edit = student is not None
        
    def show(self):
        """Show the student form"""
        self.window = tk.Toplevel(self.parent)
        self.window.title(f"{'Edit' if self.is_edit else 'Add'} Student")
        self.window.geometry("500x400")
        self.window.resizable(False, False)
        self.window.transient(self.parent)
        self.window.grab_set()
        
        # Center the window
        self.window.update_idletasks()
        x = (self.window.winfo_screenwidth() // 2) - (500 // 2)
        y = (self.window.winfo_screenheight() // 2) - (400 // 2)
        self.window.geometry(f"500x400+{x}+{y}")
        
        self._create_widgets()
        
    def _create_widgets(self):
        """Create form widgets"""
        # Main frame
        main_frame = ttk.Frame(self.window, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Form frame
        form_frame = ttk.LabelFrame(main_frame, text="Student Information", padding="15")
        form_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 20))
        
        # Variables
        self.name_var = tk.StringVar()
        self.roll_var = tk.StringVar()
        self.department_var = tk.StringVar()
        self.email_var = tk.StringVar()
        self.phone_var = tk.StringVar()
        
        # Populate fields if editing
        if self.is_edit:
            self.name_var.set(self.student.name)
            self.roll_var.set(self.student.roll)
            self.department_var.set(self.student.department)
            self.email_var.set(self.student.email)
            self.phone_var.set(self.student.phone)
        
        # Name
        ttk.Label(form_frame, text="Name *:").grid(row=0, column=0, sticky=tk.W, pady=5)
        name_entry = ttk.Entry(form_frame, textvariable=self.name_var, width=30)
        name_entry.grid(row=0, column=1, pady=5, padx=(10, 0), sticky=tk.W)
        
        # Roll Number
        ttk.Label(form_frame, text="Roll Number *:").grid(row=1, column=0, sticky=tk.W, pady=5)
        roll_entry = ttk.Entry(form_frame, textvariable=self.roll_var, width=30)
        roll_entry.grid(row=1, column=1, pady=5, padx=(10, 0), sticky=tk.W)
        
        # Department
        ttk.Label(form_frame, text="Department *:").grid(row=2, column=0, sticky=tk.W, pady=5)
        department_entry = ttk.Entry(form_frame, textvariable=self.department_var, width=30)
        department_entry.grid(row=2, column=1, pady=5, padx=(10, 0), sticky=tk.W)
        
        # Email
        ttk.Label(form_frame, text="Email *:").grid(row=3, column=0, sticky=tk.W, pady=5)
        email_entry = ttk.Entry(form_frame, textvariable=self.email_var, width=30)
        email_entry.grid(row=3, column=1, pady=5, padx=(10, 0), sticky=tk.W)
        
        # Phone
        ttk.Label(form_frame, text="Phone:").grid(row=4, column=0, sticky=tk.W, pady=5)
        phone_entry = ttk.Entry(form_frame, textvariable=self.phone_var, width=30)
        phone_entry.grid(row=4, column=1, pady=5, padx=(10, 0), sticky=tk.W)
        
        # Buttons frame
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X)
        
        # Save button
        save_btn = ttk.Button(button_frame, text="Save", command=self._save)
        save_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        # Cancel button
        cancel_btn = ttk.Button(button_frame, text="Cancel", command=self._cancel)
        cancel_btn.pack(side=tk.LEFT)
        
        # Required fields note
        note_label = ttk.Label(main_frame, text="* Required fields", 
                              font=("Arial", 9), foreground="gray")
        note_label.pack(pady=(10, 0))
        
        # Focus on first entry
        name_entry.focus()
        
    def _save(self):
        """Handle save button click"""
        try:
            # Get form data
            name = self.name_var.get().strip()
            roll = self.roll_var.get().strip()
            department = self.department_var.get().strip()
            email = self.email_var.get().strip()
            phone = self.phone_var.get().strip()
            
            # Validate required fields
            if not name:
                messagebox.showerror("Error", "Name is required")
                return
            if not roll:
                messagebox.showerror("Error", "Roll number is required")
                return
            if not department:
                messagebox.showerror("Error", "Department is required")
                return
            if not email:
                messagebox.showerror("Error", "Email is required")
                return
            
            # Create student object
            if self.is_edit:
                student = Student(name, roll, department, email, phone, self.student.id)
            else:
                student = Student(name, roll, department, email, phone)
            
            # Call save callback
            if self.on_save:
                self.on_save(student)
            
            self.window.destroy()
            
        except ValueError as e:
            messagebox.showerror("Validation Error", str(e))
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save student: {str(e)}")
    
    def _cancel(self):
        """Handle cancel button click"""
        self.window.destroy()


class StudentManagementApp:
    """
    Main application class for the Student Management System.
    """
    
    def __init__(self, root, db: Database):
        """
        Initialize the main application.
        
        Args:
            root: Tkinter root window
            db: Database instance
        """
        self.root = root
        self.db = db
        self.current_students = []
        self.selected_student = None
        
        # Configure root window
        self.root.title("Student Management System")
        self.root.geometry("1000x700")
        self.root.minsize(800, 600)
        
        # Create menu bar
        self._create_menu()
        
        # Create main interface
        self._create_widgets()
        
        # Load initial data
        self._load_students()
        
    def _create_menu(self):
        """Create application menu bar"""
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        # File menu
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Export to CSV...", command=self._export_csv)
        file_menu.add_command(label="Import from CSV...", command=self._import_csv)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit)
        
        # Reports menu
        reports_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Reports", menu=reports_menu)
        reports_menu.add_command(label="Department Report", command=self._show_department_report)
        reports_menu.add_command(label="Summary Report", command=self._show_summary_report)
        
        # Help menu
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="About", command=self._show_about)
    
    def _create_widgets(self):
        """Create main application widgets"""
        # Main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Title
        title_label = ttk.Label(main_frame, text="Student Management System", 
                               font=("Arial", 18, "bold"))
        title_label.pack(pady=(0, 20))
        
        # Control panel
        control_frame = ttk.Frame(main_frame)
        control_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Buttons
        ttk.Button(control_frame, text="Add Student", 
                  command=self._add_student).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(control_frame, text="Edit Student", 
                  command=self._edit_student).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(control_frame, text="Delete Student", 
                  command=self._delete_student).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(control_frame, text="Refresh", 
                  command=self._load_students).pack(side=tk.LEFT, padx=(0, 20))
        
        # Search frame
        search_frame = ttk.Frame(control_frame)
        search_frame.pack(side=tk.RIGHT)
        
        ttk.Label(search_frame, text="Search:").pack(side=tk.LEFT, padx=(0, 5))
        self.search_var = tk.StringVar()
        search_entry = ttk.Entry(search_frame, textvariable=self.search_var, width=20)
        search_entry.pack(side=tk.LEFT, padx=(0, 5))
        search_entry.bind('<KeyRelease>', self._on_search)
        
        ttk.Button(search_frame, text="Clear", 
                  command=self._clear_search).pack(side=tk.LEFT)
        
        # Students table
        table_frame = ttk.LabelFrame(main_frame, text="Students", padding="10")
        table_frame.pack(fill=tk.BOTH, expand=True)
        
        # Create Treeview
        columns = ('ID', 'Name', 'Roll', 'Department', 'Email', 'Phone')
        self.tree = ttk.Treeview(table_frame, columns=columns, show='headings', height=15)
        
        # Configure columns
        self.tree.heading('ID', text='ID')
        self.tree.heading('Name', text='Name')
        self.tree.heading('Roll', text='Roll Number')
        self.tree.heading('Department', text='Department')
        self.tree.heading('Email', text='Email')
        self.tree.heading('Phone', text='Phone')
        
        # Configure column widths
        self.tree.column('ID', width=50, minwidth=50)
        self.tree.column('Name', width=150, minwidth=100)
        self.tree.column('Roll', width=100, minwidth=80)
        self.tree.column('Department', width=120, minwidth=100)
        self.tree.column('Email', width=200, minwidth=150)
        self.tree.column('Phone', width=120, minwidth=100)
        
        # Scrollbars
        v_scrollbar = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=self.tree.yview)
        h_scrollbar = ttk.Scrollbar(table_frame, orient=tk.HORIZONTAL, command=self.tree.xview)
        self.tree.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)
        
        # Pack treeview and scrollbars
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        v_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        h_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)
        
        # Bind selection event
        self.tree.bind('<<TreeviewSelect>>', self._on_student_select)
        self.tree.bind('<Double-1>', lambda e: self._edit_student())
        
        # Status bar
        self.status_var = tk.StringVar()
        self.status_var.set("Ready")
        status_bar = ttk.Label(main_frame, textvariable=self.status_var, 
                              relief=tk.SUNKEN, anchor=tk.W)
        status_bar.pack(fill=tk.X, pady=(10, 0))
    
    def _load_students(self):
        """Load students from database and refresh the table"""
        try:
            self.status_var.set("Loading students...")
            self.root.update()
            
            # Get students from database
            self.current_students = self.db.get_all_students()
            
            # Clear existing items
            for item in self.tree.get_children():
                self.tree.delete(item)
            
            # Add students to treeview
            for student in self.current_students:
                self.tree.insert('', tk.END, values=(
                    student.id,
                    student.name,
                    student.roll,
                    student.department,
                    student.email,
                    student.phone
                ))
            
            self.status_var.set(f"Loaded {len(self.current_students)} students")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load students: {str(e)}")
            self.status_var.set("Error loading students")
    
    def _on_student_select(self, event):
        """Handle student selection in treeview"""
        selection = self.tree.selection()
        if selection:
            item = self.tree.item(selection[0])
            student_id = item['values'][0]
            self.selected_student = next(
                (s for s in self.current_students if s.id == student_id), None
            )
        else:
            self.selected_student = None
    
    def _add_student(self):
        """Show add student form"""
        form = StudentForm(self.root, on_save=self._save_student)
        form.show()
    
    def _edit_student(self):
        """Show edit student form"""
        if not self.selected_student:
            messagebox.showwarning("Warning", "Please select a student to edit")
            return
        
        form = StudentForm(self.root, self.selected_student, on_save=self._save_student)
        form.show()
    
    def _save_student(self, student: Student):
        """Save student (add or update)"""
        try:
            if student.id is None:
                # Add new student
                student_id = self.db.add_student(student)
                student = Student(student.name, student.roll, student.department, 
                                student.email, student.phone, student_id)
                messagebox.showinfo("Success", "Student added successfully")
            else:
                # Update existing student
                self.db.update_student(student)
                messagebox.showinfo("Success", "Student updated successfully")
            
            # Refresh the table
            self._load_students()
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save student: {str(e)}")
    
    def _delete_student(self):
        """Delete selected student"""
        if not self.selected_student:
            messagebox.showwarning("Warning", "Please select a student to delete")
            return
        
        # Confirm deletion
        result = messagebox.askyesno("Confirm Delete", 
                                   f"Are you sure you want to delete student '{self.selected_student.name}'?")
        if result:
            try:
                self.db.delete_student(self.selected_student.id)
                messagebox.showinfo("Success", "Student deleted successfully")
                self._load_students()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to delete student: {str(e)}")
    
    def _on_search(self, event):
        """Handle search input"""
        query = self.search_var.get().strip()
        if not query:
            self._load_students()
            return
        
        try:
            # Search students
            search_results = self.db.search_students(query)
            
            # Clear existing items
            for item in self.tree.get_children():
                self.tree.delete(item)
            
            # Add search results to treeview
            for student in search_results:
                self.tree.insert('', tk.END, values=(
                    student.id,
                    student.name,
                    student.roll,
                    student.department,
                    student.email,
                    student.phone
                ))
            
            self.status_var.set(f"Found {len(search_results)} students matching '{query}'")
            
        except Exception as e:
            messagebox.showerror("Error", f"Search failed: {str(e)}")
    
    def _clear_search(self):
        """Clear search and reload all students"""
        self.search_var.set("")
        self._load_students()
    
    def _export_csv(self):
        """Export students to CSV"""
        if not self.current_students:
            messagebox.showwarning("Warning", "No students to export")
            return
        
        try:
            filename = CSVHandler.export_students_to_csv(self.current_students)
            messagebox.showinfo("Success", f"Students exported to {filename}")
        except Exception as e:
            messagebox.showerror("Error", f"Export failed: {str(e)}")
    
    def _import_csv(self):
        """Import students from CSV"""
        try:
            # Import CSV data
            students_data = CSVHandler.import_students_from_csv()
            
            if not students_data:
                messagebox.showinfo("Info", "No data found in CSV file")
                return
            
            # Validate data
            errors = CSVHandler.validate_csv_data(students_data)
            if errors:
                error_msg = "Validation errors found:\n\n" + "\n".join(errors[:10])
                if len(errors) > 10:
                    error_msg += f"\n... and {len(errors) - 10} more errors"
                messagebox.showerror("Validation Error", error_msg)
                return
            
            # Confirm import
            result = messagebox.askyesno("Confirm Import", 
                                       f"Import {len(students_data)} students?")
            if result:
                imported_count = 0
                error_count = 0
                
                for student_data in students_data:
                    try:
                        student = Student(
                            name=student_data['name'],
                            roll=student_data['roll'],
                            department=student_data['department'],
                            email=student_data['email'],
                            phone=student_data.get('phone', '')
                        )
                        self.db.add_student(student)
                        imported_count += 1
                    except Exception as e:
                        error_count += 1
                        print(f"Failed to import student {student_data.get('name', 'Unknown')}: {str(e)}")
                
                messagebox.showinfo("Import Complete", 
                                  f"Imported {imported_count} students successfully.\n"
                                  f"Failed to import {error_count} students.")
                
                # Refresh the table
                self._load_students()
                
        except Exception as e:
            messagebox.showerror("Error", f"Import failed: {str(e)}")
    
    def _show_department_report(self):
        """Show department report"""
        if not self.current_students:
            messagebox.showwarning("Warning", "No students to generate report")
            return
        
        try:
            report = ReportGenerator.generate_department_report(self.current_students)
            self._show_report_dialog("Department Report", report)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to generate report: {str(e)}")
    
    def _show_summary_report(self):
        """Show summary report"""
        if not self.current_students:
            messagebox.showwarning("Warning", "No students to generate report")
            return
        
        try:
            report = ReportGenerator.generate_summary_report(self.current_students)
            self._show_report_dialog("Summary Report", report)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to generate report: {str(e)}")
    
    def _show_report_dialog(self, title: str, content: str):
        """Show report in a dialog window"""
        report_window = tk.Toplevel(self.root)
        report_window.title(title)
        report_window.geometry("600x500")
        
        # Text widget with scrollbar
        text_frame = ttk.Frame(report_window, padding="10")
        text_frame.pack(fill=tk.BOTH, expand=True)
        
        text_widget = tk.Text(text_frame, wrap=tk.WORD, font=("Courier", 10))
        scrollbar = ttk.Scrollbar(text_frame, orient=tk.VERTICAL, command=text_widget.yview)
        text_widget.configure(yscrollcommand=scrollbar.set)
        
        text_widget.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Insert content
        text_widget.insert(tk.END, content)
        text_widget.config(state=tk.DISABLED)
        
        # Close button
        ttk.Button(report_window, text="Close", 
                  command=report_window.destroy).pack(pady=10)
    
    def _show_about(self):
        """Show about dialog"""
        about_text = """Student Management System v1.0

A desktop application built with:
• Python Tkinter for GUI
• SQLite for database storage
• Object-Oriented Programming principles

Features:
• Student CRUD operations
• CSV import/export
• Search functionality
• Report generation
• Data validation

Developed as a learning project for OOP and GUI programming."""
        
        messagebox.showinfo("About", about_text)
