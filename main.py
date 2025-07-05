#!/usr/bin/env python3
"""
Safety Pass Management System - Main Application
Run this file to start the application
"""

from datetime import datetime

# Import the main application
from safety_pass_system import SafetyPassApp, EmailNotificationSystem

# Try to import configuration
try:
    from config_example import EMAIL_CONFIG  # noqa: F401 (config module created by user)
except ImportError:
    print("Warning: config.py not found. Using default email configuration.")
    print("Copy config_example.py to config.py and update with your email settings.")
    EMAIL_CONFIG = {
        'smtp_server': 'smtp.gmail.com',
        'smtp_port': 587,
        'email_username': 'your_email@company.com',
        'email_password': 'your_app_password'
    }


class SafetyPassAppWithConfig(SafetyPassApp):
    """Extended app with configuration"""

    def __init__(self):
        super().__init__()
        # Override email system with configuration
        self.email_system = EmailNotificationSystem(**EMAIL_CONFIG)

    def setup_sample_data(self):
        """Set up sample data for testing"""
        print("Setting up sample data...")

        # Add sample employees
        self.manager.add_employee("EMP001", "John Smith", "john.smith@company.com", "Engineering", "Jane Manager")
        self.manager.add_employee("EMP002", "Alice Johnson", "alice.johnson@company.com", "Safety", "Bob Supervisor")
        self.manager.add_employee("EMP003", "Mike Brown", "mike.brown@company.com", "Operations", "Jane Manager")

        # Add sample pass types
        self.manager.add_pass_type("CONFINED_SPACE", "Confined Space Entry", "Entry permit for confined spaces",
                                   "Safety", 365)
        self.manager.add_pass_type("HEIGHTS", "Working at Heights", "Permit for working at elevated positions",
                                   "Safety", 180)
        self.manager.add_pass_type("HOT_WORK", "Hot Work Permit", "Permit for welding, cutting, and hot work",
                                   "Operations", 90)
        self.manager.add_pass_type("ELECTRICAL", "Electrical Work Permit", "Permit for electrical maintenance work",
                                   "Technical", 270)

        # Issue sample passes
        self.manager.issue_safety_pass("PASS001", "EMP001", "CONFINED_SPACE")
        self.manager.issue_safety_pass("PASS002", "EMP001", "HEIGHTS")
        self.manager.issue_safety_pass("PASS003", "EMP002", "HOT_WORK")
        self.manager.issue_safety_pass("PASS004", "EMP003", "ELECTRICAL")

        print("Sample data created successfully!")
        print("\nYou can now:")
        print("1. View the CSV files in the 'safety_pass_data' folder")
        print("2. Edit them directly in Excel if needed")
        print("3. Use the admin interface to manage the system")


def main():
    """Main application entry point"""
    print("=" * 60)
    print("SAFETY PASS MANAGEMENT SYSTEM")
    print("=" * 60)
    print(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()

    # Initialize the application
    app = SafetyPassAppWithConfig()

    print("Application initialized successfully!")
    print(f"Data folder: {app.manager.data_folder}")
    print()

    # Check if data exists
    if not app.manager.employees and not app.manager.pass_types:
        print("No data found. Would you like to set up sample data? (y/n): ", end="")
        if input().lower().startswith('y'):
            app.setup_sample_data()
            print()

    # Main menu
    while True:
        print("\nWhat would you like to do?")
        print("1. Run Admin Interface (Manage employees, passes, etc.)")
        print("2. Run Notification Check (Check for expiring passes)")
        print("3. Start Daily Notification Scheduler (Runs continuously)")
        print("4. Setup Sample Data")
        print("5. View System Status")
        print("6. Exit")

        choice = input("\nSelect an option: ").strip()

        if choice == '1':
            app.admin_interface()

        elif choice == '2':
            print("\nRunning notification check...")
            app.run_daily_notifications()
            print("Notification check completed.")

        elif choice == '3':
            print("\nStarting daily notification scheduler...")
            print("This will run continuously and check for expiring passes daily at 9:00 AM.")
            print("Press Ctrl+C to stop.")
            try:
                app.schedule_daily_checks()
            except KeyboardInterrupt:
                print("\nScheduler stopped.")

        elif choice == '4':
            app.setup_sample_data()

        elif choice == '5':
            print(f"\n=== SYSTEM STATUS ===")
            print(f"Data Folder: {app.manager.data_folder}")
            print(f"Employees: {len(app.manager.employees)}")
            print(f"Pass Types: {len(app.manager.pass_types)}")
            print(f"Total Passes: {len(app.manager.safety_passes)}")

            active_passes = len([p for p in app.manager.safety_passes.values() if p.status == 'active'])
            expired_passes = len([p for p in app.manager.safety_passes.values() if p.status == 'expired'])
            expiring_soon = len(app.manager.get_expiring_passes(15))

            print(f"Active Passes: {active_passes}")
            print(f"Expired Passes: {expired_passes}")
            print(f"Expiring Soon (15 days): {expiring_soon}")

            print(f"\nEmail Configuration:")
            print(f"SMTP Server: {EMAIL_CONFIG['smtp_server']}")
            print(f"Email Username: {EMAIL_CONFIG['email_username']}")
            if EMAIL_CONFIG['email_password'] == 'your_app_password':
                print("⚠️  Email not configured! Update config.py with your email settings.")

        elif choice == '6':
            print("\nThank you for using Safety Pass Management System!")
            print("Have a safe day!")
            break

        else:
            print("Invalid option. Please try again.")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nApplication terminated by user.")
    except Exception as e:
        print(f"\n\nUnexpected error: {e}")
        print("Please contact your system administrator.")
