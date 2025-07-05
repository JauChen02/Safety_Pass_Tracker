import csv
import os
import smtplib
import schedule
import time
from datetime import datetime, timedelta
import email.mime.text
import email.mime.multipart
from typing import List, Dict
from dataclasses import dataclass, asdict


# Data Classes
@dataclass
class Employee:
    employee_id: str
    name: str
    email: str
    department: str
    manager: str

    def to_dict(self):
        return asdict(self)


@dataclass
class SafetyPassType:
    pass_type_id: str
    name: str
    description: str
    category: str
    validity_period_days: int

    def to_dict(self):
        return asdict(self)


@dataclass
class SafetyPass:
    pass_id: str
    employee_id: str
    pass_type_id: str
    issue_date: str
    expiry_date: str
    status: str  # 'active', 'expired', 'revoked'

    def to_dict(self):
        return asdict(self)

    def days_until_expiry(self) -> int:
        """Calculate days until expiry"""
        expiry = datetime.strptime(self.expiry_date, '%Y-%m-%d')
        today = datetime.now()
        return (expiry - today).days


# Core Management System
class SafetyPassManager:
    def __init__(self, data_folder: str = "safety_pass_data"):
        self.data_folder = data_folder
        self.employees_file = os.path.join(data_folder, "employees.csv")
        self.pass_types_file = os.path.join(data_folder, "pass_types.csv")
        self.passes_file = os.path.join(data_folder, "safety_passes.csv")

        # Create data folder if it doesn't exist
        os.makedirs(data_folder, exist_ok=True)

        # Initialize CSV files if they don't exist
        self._initialize_csv_files()

        # Load data
        self.employees = self._load_employees()
        self.pass_types = self._load_pass_types()
        self.safety_passes = self._load_safety_passes()

    def _initialize_csv_files(self):
        """Initialize CSV files with headers if they don't exist"""
        # Employees CSV
        if not os.path.exists(self.employees_file):
            with open(self.employees_file, 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(['employee_id', 'name', 'email', 'department', 'manager'])

        # Pass Types CSV
        if not os.path.exists(self.pass_types_file):
            with open(self.pass_types_file, 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(['pass_type_id', 'name', 'description', 'category', 'validity_period_days'])

        # Safety Passes CSV
        if not os.path.exists(self.passes_file):
            with open(self.passes_file, 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(['pass_id', 'employee_id', 'pass_type_id', 'issue_date', 'expiry_date', 'status'])

    def _load_employees(self) -> Dict[str, Employee]:
        """Load employees from CSV"""
        employees = {}
        try:
            with open(self.employees_file, 'r') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    emp = Employee(**row)
                    employees[emp.employee_id] = emp
        except FileNotFoundError:
            pass
        return employees

    def _load_pass_types(self) -> Dict[str, SafetyPassType]:
        """Load safety pass types from CSV"""
        pass_types = {}
        try:
            with open(self.pass_types_file, 'r') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    row['validity_period_days'] = int(row['validity_period_days'])
                    pass_type = SafetyPassType(**row)
                    pass_types[pass_type.pass_type_id] = pass_type
        except FileNotFoundError:
            pass
        return pass_types

    def _load_safety_passes(self) -> Dict[str, SafetyPass]:
        """Load safety passes from CSV"""
        passes = {}
        try:
            with open(self.passes_file, 'r') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    safety_pass = SafetyPass(**row)
                    passes[safety_pass.pass_id] = safety_pass
        except FileNotFoundError:
            pass
        return passes

    def _save_employees(self):
        """Save employees to CSV"""
        with open(self.employees_file, 'w', newline='') as f:
            if self.employees:
                fieldnames = ['employee_id', 'name', 'email', 'department', 'manager']
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                for emp in self.employees.values():
                    writer.writerow(emp.to_dict())

    def _save_pass_types(self):
        """Save pass types to CSV"""
        with open(self.pass_types_file, 'w', newline='') as f:
            if self.pass_types:
                fieldnames = ['pass_type_id', 'name', 'description', 'category', 'validity_period_days']
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                for pass_type in self.pass_types.values():
                    writer.writerow(pass_type.to_dict())

    def _save_safety_passes(self):
        """Save safety passes to CSV"""
        with open(self.passes_file, 'w', newline='') as f:
            if self.safety_passes:
                fieldnames = ['pass_id', 'employee_id', 'pass_type_id', 'issue_date', 'expiry_date', 'status']
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                for safety_pass in self.safety_passes.values():
                    writer.writerow(safety_pass.to_dict())

    # Employee Management
    def add_employee(self, employee_id: str, name: str, email: str, department: str, manager: str):
        """Add a new employee"""
        employee = Employee(employee_id, name, email, department, manager)
        self.employees[employee_id] = employee
        self._save_employees()
        print(f"Employee {name} added successfully!")

    def remove_employee(self, employee_id: str):
        """Remove an employee"""
        if employee_id in self.employees:
            name = self.employees[employee_id].name
            del self.employees[employee_id]
            self._save_employees()
            print(f"Employee {name} removed successfully!")
        else:
            print("Employee not found!")

    def update_employee(self, employee_id: str, **kwargs):
        """Update employee information"""
        if employee_id in self.employees:
            for key, value in kwargs.items():
                if hasattr(self.employees[employee_id], key):
                    setattr(self.employees[employee_id], key, value)
            self._save_employees()
            print("Employee updated successfully!")
        else:
            print("Employee not found!")

    # Safety Pass Type Management
    def add_pass_type(self, pass_type_id: str, name: str, description: str, category: str, validity_period_days: int):
        """Add a new safety pass type"""
        pass_type = SafetyPassType(pass_type_id, name, description, category, validity_period_days)
        self.pass_types[pass_type_id] = pass_type
        self._save_pass_types()
        print(f"Safety pass type '{name}' added successfully!")

    def remove_pass_type(self, pass_type_id: str):
        """Remove a safety pass type"""
        if pass_type_id in self.pass_types:
            name = self.pass_types[pass_type_id].name
            del self.pass_types[pass_type_id]
            self._save_pass_types()
            print(f"Safety pass type '{name}' removed successfully!")
        else:
            print("Safety pass type not found!")

    # Safety Pass Management
    def issue_safety_pass(self, pass_id: str, employee_id: str, pass_type_id: str, issue_date: str = None):
        """Issue a safety pass to an employee"""
        if employee_id not in self.employees:
            print("Employee not found!")
            return

        if pass_type_id not in self.pass_types:
            print("Safety pass type not found!")
            return

        if issue_date is None:
            issue_date = datetime.now().strftime('%Y-%m-%d')

        # Calculate expiry date
        issue_dt = datetime.strptime(issue_date, '%Y-%m-%d')
        validity_days = self.pass_types[pass_type_id].validity_period_days
        expiry_dt = issue_dt + timedelta(days=validity_days)
        expiry_date = expiry_dt.strftime('%Y-%m-%d')

        safety_pass = SafetyPass(pass_id, employee_id, pass_type_id, issue_date, expiry_date, 'active')
        self.safety_passes[pass_id] = safety_pass
        self._save_safety_passes()

        employee_name = self.employees[employee_id].name
        pass_name = self.pass_types[pass_type_id].name
        print(f"Safety pass '{pass_name}' issued to {employee_name}, expires on {expiry_date}")

    def revoke_safety_pass(self, pass_id: str):
        """Revoke a safety pass"""
        if pass_id in self.safety_passes:
            self.safety_passes[pass_id].status = 'revoked'
            self._save_safety_passes()
            print("Safety pass revoked successfully!")
        else:
            print("Safety pass not found!")

    def get_employee_passes(self, employee_id: str) -> List[SafetyPass]:
        """Get all passes for an employee"""
        return [pass_obj for pass_obj in self.safety_passes.values()
                if pass_obj.employee_id == employee_id and pass_obj.status == 'active']

    def get_expiring_passes(self, days_ahead: int = 15) -> List[SafetyPass]:
        """Get passes expiring within specified days"""
        expiring_passes = []
        for safety_pass in self.safety_passes.values():
            if safety_pass.status == 'active':
                days_until_expiry = safety_pass.days_until_expiry()
                if 1 <= days_until_expiry <= days_ahead:
                    expiring_passes.append(safety_pass)
        return expiring_passes

    def update_expired_passes(self):
        """Update status of expired passes"""
        today = datetime.now().strftime('%Y-%m-%d')
        for safety_pass in self.safety_passes.values():
            if safety_pass.status == 'active' and safety_pass.expiry_date < today:
                safety_pass.status = 'expired'
        self._save_safety_passes()

    # Reporting and Display
    def display_employees(self):
        """Display all employees"""
        if not self.employees:
            print("No employees found.")
            return

        print("\n=== EMPLOYEES ===")
        for emp in self.employees.values():
            print(f"ID: {emp.employee_id}, Name: {emp.name}, Email: {emp.email}, Dept: {emp.department}")

    def display_pass_types(self):
        """Display all safety pass types"""
        if not self.pass_types:
            print("No safety pass types found.")
            return

        print("\n=== SAFETY PASS TYPES ===")
        for pass_type in self.pass_types.values():
            print(
                f"ID: {pass_type.pass_type_id}, Name: {pass_type.name}, Category: {pass_type.category}, Valid for: {pass_type.validity_period_days} days")

    def display_employee_passes(self, employee_id: str):
        """Display all passes for an employee"""
        if employee_id not in self.employees:
            print("Employee not found!")
            return

        employee_name = self.employees[employee_id].name
        passes = self.get_employee_passes(employee_id)

        if not passes:
            print(f"No active passes found for {employee_name}.")
            return

        print(f"\n=== PASSES FOR {employee_name} ===")
        for safety_pass in passes:
            pass_name = self.pass_types[safety_pass.pass_type_id].name
            days_left = safety_pass.days_until_expiry()
            print(f"Pass: {pass_name}, Expires: {safety_pass.expiry_date}, Days left: {days_left}")


# Email Notification System
class EmailNotificationSystem:
    def __init__(self, smtp_server: str, smtp_port: int, email_username: str, email_password: str):
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
        self.email_username = email_username
        self.email_password = email_password

    def send_expiry_notification(self, employee_email: str, employee_name: str, pass_name: str, days_until_expiry: int):
        """Send expiry notification email"""
        try:
            # Create message
            msg = email.mime.multipart.MimeMultipart()
            msg['From'] = self.email_username
            msg['To'] = employee_email
            msg['Subject'] = f"Safety Pass Expiry Reminder - {pass_name}"

            # Email body
            if days_until_expiry == 1:
                body = f"""Dear {employee_name},

This is an urgent reminder that your safety pass '{pass_name}' will expire TOMORROW.

Please ensure you renew your pass before it expires to avoid any disruption to your site access.

If you have any questions, please contact your manager immediately.

Best regards,
Safety Pass Management System"""
            else:
                body = f"""Dear {employee_name},

This is a reminder that your safety pass '{pass_name}' will expire in {days_until_expiry} days.

Please plan to renew your pass in advance to ensure uninterrupted site access.

If you have any questions, please contact your manager.

Best regards,
Safety Pass Management System"""

            msg.attach(email.mime.text.MimeText(body, 'plain'))

            # Send email
            server = smtplib.SMTP(self.smtp_server, self.smtp_port)
            server.starttls()
            server.login(self.email_username, self.email_password)
            text = msg.as_string()
            server.sendmail(self.email_username, employee_email, text)
            server.quit()

            print(f"Expiry notification sent to {employee_name} ({employee_email}) for {pass_name}")

        except Exception as e:
            print(f"Failed to send email to {employee_email}: {str(e)}")


# Main Application Class
class SafetyPassApp:
    def __init__(self):
        self.manager = SafetyPassManager()
        # Initialize email system (you'll need to configure these)
        self.email_system = EmailNotificationSystem(
            smtp_server="smtp.gmail.com",  # Update with your SMTP server
            smtp_port=587,
            email_username="your_email@company.com",  # Update with your email
            email_password="your_app_password"  # Update with your app password
        )

    def run_daily_notifications(self):
        """Run daily notification check"""
        print("Running daily expiry check...")
        self.manager.update_expired_passes()

        # Check for passes expiring in 1-15 days
        for days in range(1, 16):
            expiring_passes = [p for p in self.manager.get_expiring_passes(15)
                               if p.days_until_expiry() == days]

            for safety_pass in expiring_passes:
                employee = self.manager.employees[safety_pass.employee_id]
                pass_type = self.manager.pass_types[safety_pass.pass_type_id]

                self.email_system.send_expiry_notification(
                    employee.email,
                    employee.name,
                    pass_type.name,
                    days
                )

    def schedule_daily_checks(self):
        """Schedule daily checks"""
        schedule.every().day.at("09:00").do(self.run_daily_notifications)

        print("Daily notification system started. Checks will run at 9:00 AM daily.")
        while True:
            schedule.run_pending()
            time.sleep(3600)  # Check every hour

    def admin_interface(self):
        """Simple command-line admin interface"""
        while True:
            print("\n" + "=" * 50)
            print("SAFETY PASS MANAGEMENT SYSTEM")
            print("=" * 50)
            print("1. Employee Management")
            print("2. Safety Pass Type Management")
            print("3. Safety Pass Management")
            print("4. Reports")
            print("5. Run Notification Check")
            print("6. Exit")

            choice = input("\nSelect an option: ").strip()

            if choice == '1':
                self._employee_menu()
            elif choice == '2':
                self._pass_type_menu()
            elif choice == '3':
                self._safety_pass_menu()
            elif choice == '4':
                self._reports_menu()
            elif choice == '5':
                self.run_daily_notifications()
            elif choice == '6':
                print("Goodbye!")
                break
            else:
                print("Invalid option. Please try again.")

    def _employee_menu(self):
        """Employee management menu"""
        while True:
            print("\n--- EMPLOYEE MANAGEMENT ---")
            print("1. Add Employee")
            print("2. Remove Employee")
            print("3. Update Employee")
            print("4. Display All Employees")
            print("5. Back to Main Menu")

            choice = input("\nSelect an option: ").strip()

            if choice == '1':
                emp_id = input("Employee ID: ")
                name = input("Name: ")
                email = input("Email: ")
                department = input("Department: ")
                manager = input("Manager: ")
                self.manager.add_employee(emp_id, name, email, department, manager)

            elif choice == '2':
                emp_id = input("Employee ID to remove: ")
                self.manager.remove_employee(emp_id)

            elif choice == '3':
                emp_id = input("Employee ID to update: ")
                if emp_id in self.manager.employees:
                    print("Leave blank to keep current value:")
                    name = input("Name: ").strip()
                    email = input("Email: ").strip()
                    department = input("Department: ").strip()
                    manager = input("Manager: ").strip()

                    updates = {}
                    if name: updates['name'] = name
                    if email: updates['email'] = email
                    if department: updates['department'] = department
                    if manager: updates['manager'] = manager

                    self.manager.update_employee(emp_id, **updates)
                else:
                    print("Employee not found!")

            elif choice == '4':
                self.manager.display_employees()

            elif choice == '5':
                break

            else:
                print("Invalid option. Please try again.")

    def _pass_type_menu(self):
        """Safety pass type management menu"""
        while True:
            print("\n--- SAFETY PASS TYPE MANAGEMENT ---")
            print("1. Add Pass Type")
            print("2. Remove Pass Type")
            print("3. Display All Pass Types")
            print("4. Back to Main Menu")

            choice = input("\nSelect an option: ").strip()

            if choice == '1':
                pass_type_id = input("Pass Type ID: ")
                name = input("Name: ")
                description = input("Description: ")
                category = input("Category: ")
                validity_days = int(input("Validity Period (days): "))
                self.manager.add_pass_type(pass_type_id, name, description, category, validity_days)

            elif choice == '2':
                pass_type_id = input("Pass Type ID to remove: ")
                self.manager.remove_pass_type(pass_type_id)

            elif choice == '3':
                self.manager.display_pass_types()

            elif choice == '4':
                break

            else:
                print("Invalid option. Please try again.")

    def _safety_pass_menu(self):
        """Safety pass management menu"""
        while True:
            print("\n--- SAFETY PASS MANAGEMENT ---")
            print("1. Issue Safety Pass")
            print("2. Revoke Safety Pass")
            print("3. View Employee Passes")
            print("4. Back to Main Menu")

            choice = input("\nSelect an option: ").strip()

            if choice == '1':
                pass_id = input("Pass ID: ")
                employee_id = input("Employee ID: ")
                pass_type_id = input("Pass Type ID: ")
                issue_date = input("Issue Date (YYYY-MM-DD, leave blank for today): ").strip()
                if not issue_date:
                    issue_date = None
                self.manager.issue_safety_pass(pass_id, employee_id, pass_type_id, issue_date)

            elif choice == '2':
                pass_id = input("Pass ID to revoke: ")
                self.manager.revoke_safety_pass(pass_id)

            elif choice == '3':
                employee_id = input("Employee ID: ")
                self.manager.display_employee_passes(employee_id)

            elif choice == '4':
                break

            else:
                print("Invalid option. Please try again.")

    def _reports_menu(self):
        """Reports menu"""
        while True:
            print("\n--- REPORTS ---")
            print("1. Expiring Passes (Next 15 Days)")
            print("2. Expired Passes")
            print("3. All Active Passes")
            print("4. Employee Summary")
            print("5. Back to Main Menu")

            choice = input("\nSelect an option: ").strip()

            if choice == '1':
                expiring = self.manager.get_expiring_passes(15)
                if expiring:
                    print("\n=== PASSES EXPIRING IN NEXT 15 DAYS ===")
                    for safety_pass in expiring:
                        employee = self.manager.employees[safety_pass.employee_id]
                        pass_type = self.manager.pass_types[safety_pass.pass_type_id]
                        days_left = safety_pass.days_until_expiry()
                        print(
                            f"{employee.name} - {pass_type.name} - Expires: {safety_pass.expiry_date} ({days_left} days)")
                else:
                    print("No passes expiring in the next 15 days.")

            elif choice == '2':
                expired = [p for p in self.manager.safety_passes.values() if p.status == 'expired']
                if expired:
                    print("\n=== EXPIRED PASSES ===")
                    for safety_pass in expired:
                        employee = self.manager.employees[safety_pass.employee_id]
                        pass_type = self.manager.pass_types[safety_pass.pass_type_id]
                        print(f"{employee.name} - {pass_type.name} - Expired: {safety_pass.expiry_date}")
                else:
                    print("No expired passes found.")

            elif choice == '3':
                active = [p for p in self.manager.safety_passes.values() if p.status == 'active']
                if active:
                    print("\n=== ALL ACTIVE PASSES ===")
                    for safety_pass in active:
                        employee = self.manager.employees[safety_pass.employee_id]
                        pass_type = self.manager.pass_types[safety_pass.pass_type_id]
                        days_left = safety_pass.days_until_expiry()
                        print(
                            f"{employee.name} - {pass_type.name} - Expires: {safety_pass.expiry_date} ({days_left} days)")
                else:
                    print("No active passes found.")

            elif choice == '4':
                print(f"\n=== SYSTEM SUMMARY ===")
                print(f"Total Employees: {len(self.manager.employees)}")
                print(f"Total Pass Types: {len(self.manager.pass_types)}")
                active_passes = len([p for p in self.manager.safety_passes.values() if p.status == 'active'])
                expired_passes = len([p for p in self.manager.safety_passes.values() if p.status == 'expired'])
                print(f"Active Passes: {active_passes}")
                print(f"Expired Passes: {expired_passes}")
                expiring_soon = len(self.manager.get_expiring_passes(15))
                print(f"Expiring in 15 Days: {expiring_soon}")

            elif choice == '5':
                break

            else:
                print("Invalid option. Please try again.")


# Example usage and setup
if __name__ == "__main__":
    app = SafetyPassApp()

    print("Safety Pass Management System initialized!")
    print(f"Data files are stored in: {app.manager.data_folder}")
    print("CSV files can be edited directly in Excel for bulk changes.")

    # You can run the admin interface
    # app.admin_interface()

    # Or run the daily notification scheduler
    # app.schedule_daily_checks()