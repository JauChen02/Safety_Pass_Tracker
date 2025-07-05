import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from datetime import datetime, timedelta
import threading
import os
from safety_pass_system import SafetyPassApp, EmailNotificationSystem

# Try to import configuration
try:
    from config import EMAIL_CONFIG
except ImportError:
    EMAIL_CONFIG = {
        'smtp_server': 'smtp.gmail.com',
        'smtp_port': 587,
        'email_username': 'your_email@company.com',
        'email_password': 'your_app_password'
    }


class SafetyPassGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Safety Pass Management System")
        self.root.geometry("1200x800")
        self.root.minsize(1000, 600)

        # Initialize the backend system
        self.app = SafetyPassApp()
        self.app.email_system = EmailNotificationSystem(**EMAIL_CONFIG)

        # Configure styles
        self.setup_styles()

        # Create main interface
        self.create_menu()
        self.create_main_interface()
        self.create_status_bar()

        # Load initial data
        self.refresh_all_data()

        # Setup auto-refresh
        self.setup_auto_refresh()

    def setup_styles(self):
        """Configure the application theme and styles"""
        style = ttk.Style()
        style.theme_use('clam')

        # Configure colors and fonts
        style.configure('Title.TLabel', font=('Arial', 16, 'bold'), foreground='#2c3e50')
        style.configure('Heading.TLabel', font=('Arial', 12, 'bold'), foreground='#34495e')
        style.configure('Success.TLabel', foreground='#27ae60')
        style.configure('Warning.TLabel', foreground='#e74c3c')

        # Configure treeview
        style.configure('Treeview.Heading', font=('Arial', 10, 'bold'))
        style.configure('Treeview', font=('Arial', 9))

    def create_menu(self):
        """Create the application menu bar"""
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)

        # File menu
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Setup Sample Data", command=self.setup_sample_data)
        file_menu.add_separator()
        file_menu.add_command(label="Open Data Folder", command=self.open_data_folder)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit)

        # Tools menu
        tools_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Tools", menu=tools_menu)
        tools_menu.add_command(label="Send Test Email", command=self.send_test_email)
        tools_menu.add_command(label="Check Expiring Passes", command=self.check_expiring_passes)
        tools_menu.add_command(label="Email Settings", command=self.show_email_settings)

        # Help menu
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="About", command=self.show_about)

    def create_main_interface(self):
        """Create the main tabbed interface"""
        # Create notebook for tabs
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill='both', expand=True, padx=10, pady=5)

        # Create tabs
        self.create_dashboard_tab()
        self.create_employees_tab()
        self.create_pass_types_tab()
        self.create_passes_tab()
        self.create_reports_tab()

    def create_dashboard_tab(self):
        """Create the dashboard overview tab"""
        dashboard_frame = ttk.Frame(self.notebook)
        self.notebook.add(dashboard_frame, text="🏠 Dashboard")

        # Title
        title_label = ttk.Label(dashboard_frame, text="Safety Pass Management Dashboard", style='Title.TLabel')
        title_label.pack(pady=20)

        # Statistics frame
        stats_frame = ttk.LabelFrame(dashboard_frame, text="System Overview", padding=20)
        stats_frame.pack(fill='x', padx=20, pady=10)

        # Create statistics grid
        stats_grid = ttk.Frame(stats_frame)
        stats_grid.pack(fill='x')

        # Statistics labels
        self.stats_labels = {}
        stats_info = [
            ("Total Employees", "employees_count"),
            ("Pass Types Available", "pass_types_count"),
            ("Active Passes", "active_passes_count"),
            ("Expiring Soon (15 days)", "expiring_soon_count"),
            ("Expired Passes", "expired_passes_count")
        ]

        for i, (label_text, key) in enumerate(stats_info):
            row = i // 3
            col = i % 3

            stat_frame = ttk.Frame(stats_grid)
            stat_frame.grid(row=row, column=col, padx=10, pady=5, sticky='w')

            ttk.Label(stat_frame, text=label_text, style='Heading.TLabel').pack()
            self.stats_labels[key] = ttk.Label(stat_frame, text="0", font=('Arial', 20, 'bold'))
            self.stats_labels[key].pack()

        # Quick actions frame
        actions_frame = ttk.LabelFrame(dashboard_frame, text="Quick Actions", padding=20)
        actions_frame.pack(fill='x', padx=20, pady=10)

        actions_grid = ttk.Frame(actions_frame)
        actions_grid.pack()

        # Quick action buttons
        ttk.Button(actions_grid, text="➕ Add New Employee",
                   command=self.show_add_employee_dialog, width=20).grid(row=0, column=0, padx=5, pady=5)
        ttk.Button(actions_grid, text="🎫 Issue New Pass",
                   command=self.show_issue_pass_dialog, width=20).grid(row=0, column=1, padx=5, pady=5)
        ttk.Button(actions_grid, text="📧 Check Notifications",
                   command=self.check_expiring_passes, width=20).grid(row=0, column=2, padx=5, pady=5)
        ttk.Button(actions_grid, text="📊 View Reports",
                   command=lambda: self.notebook.select(4), width=20).grid(row=1, column=0, padx=5, pady=5)
        ttk.Button(actions_grid, text="🔄 Refresh Data",
                   command=self.refresh_all_data, width=20).grid(row=1, column=1, padx=5, pady=5)
        ttk.Button(actions_grid, text="📂 Open Data Folder",
                   command=self.open_data_folder, width=20).grid(row=1, column=2, padx=5, pady=5)

    def create_employees_tab(self):
        """Create the employees management tab"""
        employees_frame = ttk.Frame(self.notebook)
        self.notebook.add(employees_frame, text="👥 Employees")

        # Title and controls
        title_frame = ttk.Frame(employees_frame)
        title_frame.pack(fill='x', padx=10, pady=5)

        ttk.Label(title_frame, text="Employee Management", style='Title.TLabel').pack(side='left')

        controls_frame = ttk.Frame(title_frame)
        controls_frame.pack(side='right')

        ttk.Button(controls_frame, text="➕ Add Employee",
                   command=self.show_add_employee_dialog).pack(side='right', padx=5)
        ttk.Button(controls_frame, text="✏️ Edit Selected",
                   command=self.edit_selected_employee).pack(side='right', padx=5)
        ttk.Button(controls_frame, text="🗑️ Remove Selected",
                   command=self.remove_selected_employee).pack(side='right', padx=5)

        # Employee list
        list_frame = ttk.LabelFrame(employees_frame, text="Employee List", padding=10)
        list_frame.pack(fill='both', expand=True, padx=10, pady=5)

        # Create treeview for employees
        columns = ('ID', 'Name', 'Email', 'Department', 'Manager', 'Active Passes')
        self.employees_tree = ttk.Treeview(list_frame, columns=columns, show='headings', height=15)

        # Configure columns
        self.employees_tree.heading('ID', text='Employee ID')
        self.employees_tree.heading('Name', text='Full Name')
        self.employees_tree.heading('Email', text='Email Address')
        self.employees_tree.heading('Department', text='Department')
        self.employees_tree.heading('Manager', text='Manager')
        self.employees_tree.heading('Active Passes', text='Active Passes')

        self.employees_tree.column('ID', width=100)
        self.employees_tree.column('Name', width=150)
        self.employees_tree.column('Email', width=200)
        self.employees_tree.column('Department', width=120)
        self.employees_tree.column('Manager', width=120)
        self.employees_tree.column('Active Passes', width=100)

        # Add scrollbar
        emp_scrollbar = ttk.Scrollbar(list_frame, orient='vertical', command=self.employees_tree.yview)
        self.employees_tree.configure(yscrollcommand=emp_scrollbar.set)

        self.employees_tree.pack(side='left', fill='both', expand=True)
        emp_scrollbar.pack(side='right', fill='y')

        # Bind double-click to edit
        self.employees_tree.bind('<Double-1>', lambda e: self.edit_selected_employee())

    def create_pass_types_tab(self):
        """Create the safety pass types management tab"""
        pass_types_frame = ttk.Frame(self.notebook)
        self.notebook.add(pass_types_frame, text="🏷️ Pass Types")

        # Title and controls
        title_frame = ttk.Frame(pass_types_frame)
        title_frame.pack(fill='x', padx=10, pady=5)

        ttk.Label(title_frame, text="Safety Pass Types Management", style='Title.TLabel').pack(side='left')

        controls_frame = ttk.Frame(title_frame)
        controls_frame.pack(side='right')

        ttk.Button(controls_frame, text="➕ Add Pass Type",
                   command=self.show_add_pass_type_dialog).pack(side='right', padx=5)
        ttk.Button(controls_frame, text="✏️ Edit Selected",
                   command=self.edit_selected_pass_type).pack(side='right', padx=5)
        ttk.Button(controls_frame, text="🗑️ Remove Selected",
                   command=self.remove_selected_pass_type).pack(side='right', padx=5)

        # Pass types list
        list_frame = ttk.LabelFrame(pass_types_frame, text="Available Pass Types", padding=10)
        list_frame.pack(fill='both', expand=True, padx=10, pady=5)

        # Create treeview for pass types
        columns = ('ID', 'Name', 'Category', 'Description', 'Validity (Days)', 'Issued Count')
        self.pass_types_tree = ttk.Treeview(list_frame, columns=columns, show='headings', height=15)

        # Configure columns
        for col in columns:
            self.pass_types_tree.heading(col, text=col)

        self.pass_types_tree.column('ID', width=100)
        self.pass_types_tree.column('Name', width=180)
        self.pass_types_tree.column('Category', width=120)
        self.pass_types_tree.column('Description', width=250)
        self.pass_types_tree.column('Validity (Days)', width=100)
        self.pass_types_tree.column('Issued Count', width=100)

        # Add scrollbar
        pt_scrollbar = ttk.Scrollbar(list_frame, orient='vertical', command=self.pass_types_tree.yview)
        self.pass_types_tree.configure(yscrollcommand=pt_scrollbar.set)

        self.pass_types_tree.pack(side='left', fill='both', expand=True)
        pt_scrollbar.pack(side='right', fill='y')

        # Bind double-click to edit
        self.pass_types_tree.bind('<Double-1>', lambda e: self.edit_selected_pass_type())

    def create_passes_tab(self):
        """Create the safety passes management tab"""
        passes_frame = ttk.Frame(self.notebook)
        self.notebook.add(passes_frame, text="🎫 Safety Passes")

        # Title and controls
        title_frame = ttk.Frame(passes_frame)
        title_frame.pack(fill='x', padx=10, pady=5)

        ttk.Label(title_frame, text="Safety Passes Management", style='Title.TLabel').pack(side='left')

        controls_frame = ttk.Frame(title_frame)
        controls_frame.pack(side='right')

        ttk.Button(controls_frame, text="🎫 Issue New Pass",
                   command=self.show_issue_pass_dialog).pack(side='right', padx=5)
        ttk.Button(controls_frame, text="❌ Revoke Selected",
                   command=self.revoke_selected_pass).pack(side='right', padx=5)

        # Filter frame
        filter_frame = ttk.LabelFrame(passes_frame, text="Filter Passes", padding=10)
        filter_frame.pack(fill='x', padx=10, pady=5)

        filter_controls = ttk.Frame(filter_frame)
        filter_controls.pack(fill='x')

        ttk.Label(filter_controls, text="Status:").grid(row=0, column=0, padx=5, sticky='w')
        self.pass_status_filter = ttk.Combobox(filter_controls, values=['All', 'Active', 'Expired', 'Revoked'],
                                               state='readonly', width=10)
        self.pass_status_filter.set('All')
        self.pass_status_filter.grid(row=0, column=1, padx=5)
        self.pass_status_filter.bind('<<ComboboxSelected>>', lambda e: self.refresh_passes_data())

        ttk.Label(filter_controls, text="Employee:").grid(row=0, column=2, padx=5, sticky='w')
        self.employee_filter = ttk.Combobox(filter_controls, state='readonly', width=20)
        self.employee_filter.grid(row=0, column=3, padx=5)
        self.employee_filter.bind('<<ComboboxSelected>>', lambda e: self.refresh_passes_data())

        ttk.Button(filter_controls, text="Clear Filters",
                   command=self.clear_pass_filters).grid(row=0, column=4, padx=20)

        # Passes list
        list_frame = ttk.LabelFrame(passes_frame, text="Issued Safety Passes", padding=10)
        list_frame.pack(fill='both', expand=True, padx=10, pady=5)

        # Create treeview for passes
        columns = ('Pass ID', 'Employee', 'Pass Type', 'Issue Date', 'Expiry Date', 'Days Left', 'Status')
        self.passes_tree = ttk.Treeview(list_frame, columns=columns, show='headings', height=12)

        # Configure columns
        for col in columns:
            self.passes_tree.heading(col, text=col)

        self.passes_tree.column('Pass ID', width=100)
        self.passes_tree.column('Employee', width=150)
        self.passes_tree.column('Pass Type', width=150)
        self.passes_tree.column('Issue Date', width=100)
        self.passes_tree.column('Expiry Date', width=100)
        self.passes_tree.column('Days Left', width=80)
        self.passes_tree.column('Status', width=80)

        # Add scrollbar
        passes_scrollbar = ttk.Scrollbar(list_frame, orient='vertical', command=self.passes_tree.yview)
        self.passes_tree.configure(yscrollcommand=passes_scrollbar.set)

        self.passes_tree.pack(side='left', fill='both', expand=True)
        passes_scrollbar.pack(side='right', fill='y')

    def create_reports_tab(self):
        """Create the reports and analytics tab"""
        reports_frame = ttk.Frame(self.notebook)
        self.notebook.add(reports_frame, text="📊 Reports")

        # Title
        ttk.Label(reports_frame, text="Reports and Analytics", style='Title.TLabel').pack(pady=10)

        # Report buttons frame
        buttons_frame = ttk.LabelFrame(reports_frame, text="Generate Reports", padding=20)
        buttons_frame.pack(fill='x', padx=10, pady=5)

        buttons_grid = ttk.Frame(buttons_frame)
        buttons_grid.pack()

        report_buttons = [
            ("⏰ Expiring Passes (Next 15 Days)", self.show_expiring_passes_report),
            ("❌ Expired Passes", self.show_expired_passes_report),
            ("✅ All Active Passes", self.show_active_passes_report),
            ("👤 Employee Pass Summary", self.show_employee_summary_report),
            ("📈 System Statistics", self.show_system_stats_report),
            ("📧 Email Notification Log", self.show_notification_log)
        ]

        for i, (text, command) in enumerate(report_buttons):
            row = i // 2
            col = i % 2
            ttk.Button(buttons_grid, text=text, command=command, width=30).grid(
                row=row, column=col, padx=10, pady=5)

        # Report display area
        self.report_frame = ttk.LabelFrame(reports_frame, text="Report Results", padding=10)
        self.report_frame.pack(fill='both', expand=True, padx=10, pady=5)

        # Create text widget for report display
        self.report_text = tk.Text(self.report_frame, wrap=tk.WORD, font=('Courier', 10))
        report_scrollbar = ttk.Scrollbar(self.report_frame, orient='vertical', command=self.report_text.yview)
        self.report_text.configure(yscrollcommand=report_scrollbar.set)

        self.report_text.pack(side='left', fill='both', expand=True)
        report_scrollbar.pack(side='right', fill='y')

    def create_status_bar(self):
        """Create the status bar at the bottom"""
        self.status_bar = ttk.Frame(self.root)
        self.status_bar.pack(side='bottom', fill='x')

        self.status_label = ttk.Label(self.status_bar, text="Ready", relief='sunken')
        self.status_label.pack(side='left', fill='x', expand=True, padx=5, pady=2)

        # Add current time
        self.time_label = ttk.Label(self.status_bar, text="", relief='sunken')
        self.time_label.pack(side='right', padx=5, pady=2)

        self.update_time()

    def update_time(self):
        """Update the time display"""
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.time_label.config(text=current_time)
        self.root.after(1000, self.update_time)

    def setup_auto_refresh(self):
        """Setup automatic data refresh"""
        self.refresh_all_data()
        # Refresh every 30 seconds
        self.root.after(30000, self.setup_auto_refresh)

    def update_status(self, message):
        """Update the status bar message"""
        self.status_label.config(text=message)
        self.root.update_idletasks()
        # Clear status after 5 seconds
        self.root.after(5000, lambda: self.status_label.config(text="Ready"))

    # Data refresh methods
    def refresh_all_data(self):
        """Refresh all data displays"""
        self.refresh_dashboard_stats()
        self.refresh_employees_data()
        self.refresh_pass_types_data()
        self.refresh_passes_data()
        self.update_filter_combos()
        self.update_status("Data refreshed")

    def refresh_dashboard_stats(self):
        """Update dashboard statistics"""
        # Calculate statistics
        total_employees = len(self.app.manager.employees)
        total_pass_types = len(self.app.manager.pass_types)
        active_passes = len([p for p in self.app.manager.safety_passes.values() if p.status == 'active'])
        expired_passes = len([p for p in self.app.manager.safety_passes.values() if p.status == 'expired'])
        expiring_soon = len(self.app.manager.get_expiring_passes(15))

        # Update labels
        self.stats_labels['employees_count'].config(text=str(total_employees))
        self.stats_labels['pass_types_count'].config(text=str(total_pass_types))
        self.stats_labels['active_passes_count'].config(text=str(active_passes))
        self.stats_labels['expired_passes_count'].config(text=str(expired_passes))
        self.stats_labels['expiring_soon_count'].config(text=str(expiring_soon))

        # Color code expiring soon
        if expiring_soon > 0:
            self.stats_labels['expiring_soon_count'].config(foreground='red')
        else:
            self.stats_labels['expiring_soon_count'].config(foreground='green')

    def refresh_employees_data(self):
        """Refresh the employees treeview"""
        # Clear existing data
        for item in self.employees_tree.get_children():
            self.employees_tree.delete(item)

        # Add employee data
        for emp in self.app.manager.employees.values():
            active_passes = len(self.app.manager.get_employee_passes(emp.employee_id))
            self.employees_tree.insert('', 'end', values=(
                emp.employee_id, emp.name, emp.email,
                emp.department, emp.manager, active_passes
            ))

    def refresh_pass_types_data(self):
        """Refresh the pass types treeview"""
        # Clear existing data
        for item in self.pass_types_tree.get_children():
            self.pass_types_tree.delete(item)

        # Add pass type data
        for pt in self.app.manager.pass_types.values():
            issued_count = len([p for p in self.app.manager.safety_passes.values()
                                if p.pass_type_id == pt.pass_type_id])
            self.pass_types_tree.insert('', 'end', values=(
                pt.pass_type_id, pt.name, pt.category,
                pt.description, pt.validity_period_days, issued_count
            ))

    def refresh_passes_data(self):
        """Refresh the passes treeview with filters"""
        # Clear existing data
        for item in self.passes_tree.get_children():
            self.passes_tree.delete(item)

        # Get filter values
        status_filter = self.pass_status_filter.get()
        employee_filter = self.employee_filter.get()

        # Add pass data with filters
        for safety_pass in self.app.manager.safety_passes.values():
            # Apply status filter
            if status_filter != 'All' and safety_pass.status.title() != status_filter:
                continue

            # Apply employee filter
            if employee_filter and employee_filter != 'All Employees':
                emp_name = self.app.manager.employees.get(safety_pass.employee_id, {}).name
                if emp_name != employee_filter:
                    continue

            # Get employee and pass type names
            employee = self.app.manager.employees.get(safety_pass.employee_id)
            pass_type = self.app.manager.pass_types.get(safety_pass.pass_type_id)

            employee_name = employee.name if employee else "Unknown"
            pass_type_name = pass_type.name if pass_type else "Unknown"

            # Calculate days left
            days_left = safety_pass.days_until_expiry() if safety_pass.status == 'active' else 'N/A'

            # Color code based on status and days left
            item = self.passes_tree.insert('', 'end', values=(
                safety_pass.pass_id, employee_name, pass_type_name,
                safety_pass.issue_date, safety_pass.expiry_date,
                days_left, safety_pass.status.title()
            ))

            # Color coding
            if safety_pass.status == 'expired':
                self.passes_tree.set(item, 'Status', '❌ Expired')
            elif safety_pass.status == 'revoked':
                self.passes_tree.set(item, 'Status', '🚫 Revoked')
            elif isinstance(days_left, int) and days_left <= 7:
                self.passes_tree.set(item, 'Days Left', f'⚠️ {days_left}')

    def update_filter_combos(self):
        """Update the filter combo boxes"""
        # Update employee filter
        employee_names = ['All Employees'] + [emp.name for emp in self.app.manager.employees.values()]
        self.employee_filter['values'] = employee_names
        if not self.employee_filter.get():
            self.employee_filter.set('All Employees')

    def clear_pass_filters(self):
        """Clear all pass filters"""
        self.pass_status_filter.set('All')
        self.employee_filter.set('All Employees')
        self.refresh_passes_data()

    # Dialog methods
    def show_add_employee_dialog(self):
        """Show dialog to add new employee"""
        dialog = EmployeeDialog(self.root, "Add New Employee")
        if dialog.result:
            emp_data = dialog.result
            self.app.manager.add_employee(
                emp_data['employee_id'], emp_data['name'],
                emp_data['email'], emp_data['department'], emp_data['manager']
            )
            self.refresh_all_data()
            self.update_status(f"Employee '{emp_data['name']}' added successfully")

    def edit_selected_employee(self):
        """Edit the selected employee"""
        selected = self.employees_tree.selection()
        if not selected:
            messagebox.showwarning("No Selection", "Please select an employee to edit.")
            return

        emp_id = self.employees_tree.item(selected[0])['values'][0]
        employee = self.app.manager.employees.get(emp_id)

        if employee:
            dialog = EmployeeDialog(self.root, "Edit Employee", employee)
            if dialog.result:
                emp_data = dialog.result
                self.app.manager.update_employee(emp_id, **emp_data)
                self.refresh_all_data()
                self.update_status(f"Employee '{emp_data['name']}' updated successfully")

    def remove_selected_employee(self):
        """Remove the selected employee"""
        selected = self.employees_tree.selection()
        if not selected:
            messagebox.showwarning("No Selection", "Please select an employee to remove.")
            return

        emp_id = self.employees_tree.item(selected[0])['values'][0]
        emp_name = self.employees_tree.item(selected[0])['values'][1]

        if messagebox.askyesno("Confirm Removal",
                               f"Are you sure you want to remove employee '{emp_name}'?\n\n"
                               "This action cannot be undone."):
            self.app.manager.remove_employee(emp_id)
            self.refresh_all_data()
            self.update_status(f"Employee '{emp_name}' removed successfully")

    def show_add_pass_type_dialog(self):
        """Show dialog to add new pass type"""
        dialog = PassTypeDialog(self.root, "Add New Pass Type")
        if dialog.result:
            pt_data = dialog.result
            self.app.manager.add_pass_type(
                pt_data['pass_type_id'], pt_data['name'],
                pt_data['description'], pt_data['category'],
                pt_data['validity_period_days']
            )
            self.refresh_all_data()
            self.update_status(f"Pass type '{pt_data['name']}' added successfully")

    def edit_selected_pass_type(self):
        """Edit the selected pass type"""
        selected = self.pass_types_tree.selection()
        if not selected:
            messagebox.showwarning("No Selection", "Please select a pass type to edit.")
            return

        pt_id = self.pass_types_tree.item(selected[0])['values'][0]
        pass_type = self.app.manager.pass_types.get(pt_id)

        if pass_type:
            dialog = PassTypeDialog(self.root, "Edit Pass Type", pass_type)
            if dialog.result:
                # Note: This would require an update_pass_type method in the backend
                self.update_status("Pass type editing not yet implemented")

    def remove_selected_pass_type(self):
        """Remove the selected pass type"""
        selected = self.pass_types_tree.selection()
        if not selected:
            messagebox.showwarning("No Selection", "Please select a pass type to remove.")
            return

        pt_id = self.pass_types_tree.item(selected[0])['values'][0]
        pt_name = self.pass_types_tree.item(selected[0])['values'][1]

        if messagebox.askyesno("Confirm Removal",
                               f"Are you sure you want to remove pass type '{pt_name}'?\n\n"
                               "This action cannot be undone."):
            self.app.manager.remove_pass_type(pt_id)
            self.refresh_all_data()
            self.update_status(f"Pass type '{pt_name}' removed successfully")

    def show_issue_pass_dialog(self):
        """Show dialog to issue new pass"""
        if not self.app.manager.employees:
            messagebox.showwarning("No Employees", "Please add employees before issuing passes.")
            return

        if not self.app.manager.pass_types:
            messagebox.showwarning("No Pass Types", "Please add pass types before issuing passes.")
            return

        dialog = IssuePassDialog(self.root, self.app.manager)
        if dialog.result:
            pass_data = dialog.result
            # Generate unique pass ID
            pass_id = f"PASS_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

            self.app.manager.issue_safety_pass(
                pass_id, pass_data['employee_id'],
                pass_data['pass_type_id'], pass_data['issue_date']
            )
            self.refresh_all_data()

            emp_name = self.app.manager.employees[pass_data['employee_id']].name
            pass_name = self.app.manager.pass_types[pass_data['pass_type_id']].name
            self.update_status(f"Pass '{pass_name}' issued to {emp_name}")

    def revoke_selected_pass(self):
        """Revoke the selected pass"""
        selected = self.passes_tree.selection()
        if not selected:
            messagebox.showwarning("No Selection", "Please select a pass to revoke.")
            return

        pass_id = self.passes_tree.item(selected[0])['values'][0]
        employee_name = self.passes_tree.item(selected[0])['values'][1]
        pass_type_name = self.passes_tree.item(selected[0])['values'][2]

        if messagebox.askyesno("Confirm Revocation",
                               f"Are you sure you want to revoke the pass:\n\n"
                               f"Employee: {employee_name}\n"
                               f"Pass Type: {pass_type_name}\n\n"
                               "This action cannot be undone."):
            self.app.manager.revoke_safety_pass(pass_id)
            self.refresh_all_data()
            self.update_status(f"Pass revoked for {employee_name}")

    # Report methods
    def show_expiring_passes_report(self):
        """Show report of expiring passes"""
        expiring_passes = self.app.manager.get_expiring_passes(15)

        report = "PASSES EXPIRING IN NEXT 15 DAYS\n"
        report += "=" * 50 + "\n\n"

        if not expiring_passes:
            report += "✅ No passes expiring in the next 15 days.\n"
        else:
            for safety_pass in sorted(expiring_passes, key=lambda p: p.days_until_expiry()):
                employee = self.app.manager.employees.get(safety_pass.employee_id)
                pass_type = self.app.manager.pass_types.get(safety_pass.pass_type_id)
                days_left = safety_pass.days_until_expiry()

                urgency = "🔴 URGENT" if days_left <= 3 else "🟡 WARNING" if days_left <= 7 else "🟢 NOTICE"

                report += f"{urgency} - {employee.name if employee else 'Unknown'}\n"
                report += f"   Pass: {pass_type.name if pass_type else 'Unknown'}\n"
                report += f"   Expires: {safety_pass.expiry_date} ({days_left} days)\n"
                report += f"   Email: {employee.email if employee else 'Unknown'}\n\n"

        self.display_report(report)

    def show_expired_passes_report(self):
        """Show report of expired passes"""
        expired_passes = [p for p in self.app.manager.safety_passes.values() if p.status == 'expired']

        report = "EXPIRED PASSES REPORT\n"
        report += "=" * 30 + "\n\n"

        if not expired_passes:
            report += "✅ No expired passes found.\n"
        else:
            for safety_pass in expired_passes:
                employee = self.app.manager.employees.get(safety_pass.employee_id)
                pass_type = self.app.manager.pass_types.get(safety_pass.pass_type_id)

                report += f"❌ {employee.name if employee else 'Unknown'}\n"
                report += f"   Pass: {pass_type.name if pass_type else 'Unknown'}\n"
                report += f"   Expired: {safety_pass.expiry_date}\n"
                report += f"   Email: {employee.email if employee else 'Unknown'}\n\n"

        self.display_report(report)

    def show_active_passes_report(self):
        """Show report of active passes"""
        active_passes = [p for p in self.app.manager.safety_passes.values() if p.status == 'active']

        report = "ACTIVE PASSES REPORT\n"
        report += "=" * 25 + "\n\n"

        if not active_passes:
            report += "No active passes found.\n"
        else:
            for safety_pass in active_passes:
                employee = self.app.manager.employees.get(safety_pass.employee_id)
                pass_type = self.app.manager.pass_types.get(safety_pass.pass_type_id)
                days_left = safety_pass.days_until_expiry()

                status_icon = "🔴" if days_left <= 7 else "🟢"

                report += f"{status_icon} {employee.name if employee else 'Unknown'}\n"
                report += f"   Pass: {pass_type.name if pass_type else 'Unknown'}\n"
                report += f"   Expires: {safety_pass.expiry_date} ({days_left} days)\n\n"

        self.display_report(report)

    def show_employee_summary_report(self):
        """Show employee summary report"""
        report = "EMPLOYEE SUMMARY REPORT\n"
        report += "=" * 30 + "\n\n"

        for employee in self.app.manager.employees.values():
            passes = self.app.manager.get_employee_passes(employee.employee_id)

            report += f"👤 {employee.name} ({employee.employee_id})\n"
            report += f"   Department: {employee.department}\n"
            report += f"   Manager: {employee.manager}\n"
            report += f"   Email: {employee.email}\n"
            report += f"   Active Passes: {len(passes)}\n"

            if passes:
                for safety_pass in passes:
                    pass_type = self.app.manager.pass_types.get(safety_pass.pass_type_id)
                    days_left = safety_pass.days_until_expiry()
                    report += f"     • {pass_type.name if pass_type else 'Unknown'} (expires in {days_left} days)\n"
            else:
                report += "     • No active passes\n"

            report += "\n"

        self.display_report(report)

    def show_system_stats_report(self):
        """Show system statistics report"""
        total_employees = len(self.app.manager.employees)
        total_pass_types = len(self.app.manager.pass_types)
        total_passes = len(self.app.manager.safety_passes)
        active_passes = len([p for p in self.app.manager.safety_passes.values() if p.status == 'active'])
        expired_passes = len([p for p in self.app.manager.safety_passes.values() if p.status == 'expired'])
        revoked_passes = len([p for p in self.app.manager.safety_passes.values() if p.status == 'revoked'])
        expiring_soon = len(self.app.manager.get_expiring_passes(15))

        report = "SYSTEM STATISTICS REPORT\n"
        report += "=" * 30 + "\n\n"

        report += f"📊 OVERVIEW\n"
        report += f"   Total Employees: {total_employees}\n"
        report += f"   Total Pass Types: {total_pass_types}\n"
        report += f"   Total Passes Issued: {total_passes}\n\n"

        report += f"🎫 PASS STATUS\n"
        report += f"   Active Passes: {active_passes}\n"
        report += f"   Expired Passes: {expired_passes}\n"
        report += f"   Revoked Passes: {revoked_passes}\n"
        report += f"   Expiring Soon (15 days): {expiring_soon}\n\n"

        if total_passes > 0:
            active_percent = (active_passes / total_passes) * 100
            expired_percent = (expired_passes / total_passes) * 100

            report += f"📈 PERCENTAGES\n"
            report += f"   Active: {active_percent:.1f}%\n"
            report += f"   Expired: {expired_percent:.1f}%\n\n"

        # Pass type usage
        report += f"🏷️ PASS TYPE USAGE\n"
        for pass_type in self.app.manager.pass_types.values():
            count = len([p for p in self.app.manager.safety_passes.values()
                         if p.pass_type_id == pass_type.pass_type_id])
            report += f"   {pass_type.name}: {count} issued\n"

        self.display_report(report)

    def show_notification_log(self):
        """Show notification log (placeholder)"""
        report = "EMAIL NOTIFICATION LOG\n"
        report += "=" * 25 + "\n\n"
        report += "📧 Feature coming soon!\n\n"
        report += "This will show:\n"
        report += "• Email notification history\n"
        report += "• Delivery status\n"
        report += "• Failed notifications\n"
        report += "• Notification statistics\n"

        self.display_report(report)

    def display_report(self, report_text):
        """Display report in the text widget"""
        self.report_text.delete(1.0, tk.END)
        self.report_text.insert(1.0, report_text)

        # Scroll to top
        self.report_text.see(1.0)

    # Menu action methods
    def setup_sample_data(self):
        """Setup sample data for testing"""
        if messagebox.askyesno("Setup Sample Data",
                               "This will add sample employees, pass types, and passes.\n\n"
                               "Continue?"):
            # Add sample employees
            self.app.manager.add_employee("EMP001", "John Smith", "john.smith@company.com", "Engineering",
                                          "Jane Manager")
            self.app.manager.add_employee("EMP002", "Alice Johnson", "alice.johnson@company.com", "Safety",
                                          "Bob Supervisor")
            self.app.manager.add_employee("EMP003", "Mike Brown", "mike.brown@company.com", "Operations",
                                          "Jane Manager")

            # Add sample pass types
            self.app.manager.add_pass_type("CONFINED_SPACE", "Confined Space Entry", "Entry permit for confined spaces",
                                           "Safety", 365)
            self.app.manager.add_pass_type("HEIGHTS", "Working at Heights", "Permit for working at elevated positions",
                                           "Safety", 180)
            self.app.manager.add_pass_type("HOT_WORK", "Hot Work Permit", "Permit for welding, cutting, and hot work",
                                           "Operations", 90)
            self.app.manager.add_pass_type("ELECTRICAL", "Electrical Work Permit",
                                           "Permit for electrical maintenance work", "Technical", 270)

            # Issue sample passes
            self.app.manager.issue_safety_pass("PASS001", "EMP001", "CONFINED_SPACE")
            self.app.manager.issue_safety_pass("PASS002", "EMP001", "HEIGHTS")
            self.app.manager.issue_safety_pass("PASS003", "EMP002", "HOT_WORK")
            self.app.manager.issue_safety_pass("PASS004", "EMP003", "ELECTRICAL")

            self.refresh_all_data()
            self.update_status("Sample data created successfully!")
            messagebox.showinfo("Success", "Sample data has been created successfully!")

    def open_data_folder(self):
        """Open the data folder in file explorer"""
        data_folder = self.app.manager.data_folder
        try:
            if os.name == 'nt':  # Windows
                os.startfile(data_folder)
            elif os.name == 'posix':  # macOS and Linux
                os.system(f'open "{data_folder}"')
            else:
                messagebox.showinfo("Data Folder", f"Data folder location:\n{data_folder}")

            self.update_status("Data folder opened")
        except Exception as e:
            messagebox.showerror("Error", f"Could not open data folder:\n{str(e)}")

    def send_test_email(self):
        """Send a test email"""
        dialog = TestEmailDialog(self.root)
        if dialog.result:
            email_address = dialog.result
            try:
                # Send test email using the email system
                self.app.email_system.send_expiry_notification(
                    email_address, "Test User", "Test Safety Pass", 5
                )
                self.update_status("Test email sent successfully!")
                messagebox.showinfo("Success", f"Test email sent to {email_address}")
            except Exception as e:
                messagebox.showerror("Email Error", f"Failed to send test email:\n{str(e)}")

    def check_expiring_passes(self):
        """Manually check and send expiring pass notifications"""
        try:
            # Run the notification check in a separate thread to avoid freezing UI
            def run_notifications():
                self.app.run_daily_notifications()
                self.root.after(0, lambda: self.update_status("Notification check completed"))
                self.root.after(0, lambda: messagebox.showinfo("Complete", "Expiring pass notifications sent!"))

            thread = threading.Thread(target=run_notifications)
            thread.daemon = True
            thread.start()

            self.update_status("Checking for expiring passes...")

        except Exception as e:
            messagebox.showerror("Error", f"Failed to check expiring passes:\n{str(e)}")

    def show_email_settings(self):
        """Show email configuration dialog"""
        dialog = EmailSettingsDialog(self.root, EMAIL_CONFIG)
        if dialog.result:
            # Update email configuration
            global EMAIL_CONFIG
            EMAIL_CONFIG = dialog.result
            self.app.email_system = EmailNotificationSystem(**EMAIL_CONFIG)
            self.update_status("Email settings updated")
            messagebox.showinfo("Success", "Email settings have been updated!")

    def show_about(self):
        """Show about dialog"""
        about_text = """Safety Pass Management System
Version 1.0

A comprehensive safety pass tracking system designed to automate 
the management of employee safety passes and their expiry dates.

Features:
• Employee and pass type management
• Automated pass issuance and tracking
• Email notifications for expiring passes
• Comprehensive reporting
• CSV data export/import

© 2025 Safety Pass Management System"""

        messagebox.showinfo("About", about_text)


# Dialog classes
class EmployeeDialog:
    def __init__(self, parent, title, employee=None):
        self.result = None

        # Create dialog window
        self.dialog = tk.Toplevel(parent)
        self.dialog.title(title)
        self.dialog.geometry("400x300")
        self.dialog.resizable(False, False)
        self.dialog.transient(parent)
        self.dialog.grab_set()

        # Center the dialog
        self.dialog.geometry("+%d+%d" % (parent.winfo_rootx() + 100, parent.winfo_rooty() + 100))

        # Create form
        main_frame = ttk.Frame(self.dialog, padding=20)
        main_frame.pack(fill='both', expand=True)

        # Form fields
        fields = [
            ("Employee ID:", "employee_id"),
            ("Full Name:", "name"),
            ("Email Address:", "email"),
            ("Department:", "department"),
            ("Manager:", "manager")
        ]

        self.entries = {}

        for i, (label_text, field_name) in enumerate(fields):
            ttk.Label(main_frame, text=label_text).grid(row=i, column=0, sticky='w', pady=5)

            entry = ttk.Entry(main_frame, width=30)
            entry.grid(row=i, column=1, pady=5, padx=(10, 0))
            self.entries[field_name] = entry

            # Fill with existing data if editing
            if employee:
                entry.insert(0, getattr(employee, field_name, ''))

        # Buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=len(fields), column=0, columnspan=2, pady=20)

        ttk.Button(button_frame, text="Save", command=self.save).pack(side='right', padx=5)
        ttk.Button(button_frame, text="Cancel", command=self.cancel).pack(side='right')

        # Focus on first field
        self.entries['employee_id'].focus()

        # Bind Enter key
        self.dialog.bind('<Return>', lambda e: self.save())
        self.dialog.bind('<Escape>', lambda e: self.cancel())

        # Wait for dialog to close
        self.dialog.wait_window()

    def save(self):
        # Validate fields
        data = {}
        for field_name, entry in self.entries.items():
            value = entry.get().strip()
            if not value:
                messagebox.showerror("Validation Error", f"Please enter {field_name.replace('_', ' ').title()}")
                entry.focus()
                return
            data[field_name] = value

        # Validate email format (basic)
        email = data['email']
        if '@' not in email or '.' not in email:
            messagebox.showerror("Validation Error", "Please enter a valid email address")
            self.entries['email'].focus()
            return

        self.result = data
        self.dialog.destroy()

    def cancel(self):
        self.dialog.destroy()


class PassTypeDialog:
    def __init__(self, parent, title, pass_type=None):
        self.result = None

        # Create dialog window
        self.dialog = tk.Toplevel(parent)
        self.dialog.title(title)
        self.dialog.geometry("450x350")
        self.dialog.resizable(False, False)
        self.dialog.transient(parent)
        self.dialog.grab_set()

        # Center the dialog
        self.dialog.geometry("+%d+%d" % (parent.winfo_rootx() + 100, parent.winfo_rooty() + 100))

        # Create form
        main_frame = ttk.Frame(self.dialog, padding=20)
        main_frame.pack(fill='both', expand=True)

        # Form fields
        row = 0

        # Pass Type ID
        ttk.Label(main_frame, text="Pass Type ID:").grid(row=row, column=0, sticky='w', pady=5)
        self.id_entry = ttk.Entry(main_frame, width=30)
        self.id_entry.grid(row=row, column=1, pady=5, padx=(10, 0))
        row += 1

        # Name
        ttk.Label(main_frame, text="Pass Name:").grid(row=row, column=0, sticky='w', pady=5)
        self.name_entry = ttk.Entry(main_frame, width=30)
        self.name_entry.grid(row=row, column=1, pady=5, padx=(10, 0))
        row += 1

        # Category
        ttk.Label(main_frame, text="Category:").grid(row=row, column=0, sticky='w', pady=5)
        self.category_combo = ttk.Combobox(main_frame, width=27,
                                           values=['Safety', 'Operations', 'Technical', 'Administrative', 'Emergency'])
        self.category_combo.grid(row=row, column=1, pady=5, padx=(10, 0))
        row += 1

        # Validity Period
        ttk.Label(main_frame, text="Validity (Days):").grid(row=row, column=0, sticky='w', pady=5)
        self.validity_entry = ttk.Entry(main_frame, width=30)
        self.validity_entry.grid(row=row, column=1, pady=5, padx=(10, 0))
        row += 1

        # Description
        ttk.Label(main_frame, text="Description:").grid(row=row, column=0, sticky='nw', pady=5)
        self.description_text = tk.Text(main_frame, width=30, height=5)
        self.description_text.grid(row=row, column=1, pady=5, padx=(10, 0))
        row += 1

        # Fill with existing data if editing
        if pass_type:
            self.id_entry.insert(0, pass_type.pass_type_id)
            self.name_entry.insert(0, pass_type.name)
            self.category_combo.set(pass_type.category)
            self.validity_entry.insert(0, str(pass_type.validity_period_days))
            self.description_text.insert(1.0, pass_type.description)

        # Buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=row, column=0, columnspan=2, pady=20)

        ttk.Button(button_frame, text="Save", command=self.save).pack(side='right', padx=5)
        ttk.Button(button_frame, text="Cancel", command=self.cancel).pack(side='right')

        # Focus on first field
        self.id_entry.focus()

        # Bind keys
        self.dialog.bind('<Escape>', lambda e: self.cancel())

        # Wait for dialog to close
        self.dialog.wait_window()

    def save(self):
        # Validate and collect data
        pass_type_id = self.id_entry.get().strip()
        name = self.name_entry.get().strip()
        category = self.category_combo.get().strip()
        validity_str = self.validity_entry.get().strip()
        description = self.description_text.get(1.0, tk.END).strip()

        # Validation
        if not all([pass_type_id, name, category, validity_str]):
            messagebox.showerror("Validation Error", "Please fill in all required fields")
            return

        try:
            validity_days = int(validity_str)
            if validity_days <= 0:
                raise ValueError()
        except ValueError:
            messagebox.showerror("Validation Error", "Validity period must be a positive number")
            self.validity_entry.focus()
            return

        self.result = {
            'pass_type_id': pass_type_id,
            'name': name,
            'category': category,
            'description': description,
            'validity_period_days': validity_days
        }
        self.dialog.destroy()

    def cancel(self):
        self.dialog.destroy()


class IssuePassDialog:
    def __init__(self, parent, manager):
        self.result = None
        self.manager = manager

        # Create dialog window
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("Issue New Safety Pass")
        self.dialog.geometry("400x250")
        self.dialog.resizable(False, False)
        self.dialog.transient(parent)
        self.dialog.grab_set()

        # Center the dialog
        self.dialog.geometry("+%d+%d" % (parent.winfo_rootx() + 100, parent.winfo_rooty() + 100))

        # Create form
        main_frame = ttk.Frame(self.dialog, padding=20)
        main_frame.pack(fill='both', expand=True)

        row = 0

        # Employee selection
        ttk.Label(main_frame, text="Employee:").grid(row=row, column=0, sticky='w', pady=5)
        employee_options = [f"{emp.name} ({emp.employee_id})" for emp in manager.employees.values()]
        self.employee_combo = ttk.Combobox(main_frame, width=35, values=employee_options, state='readonly')
        self.employee_combo.grid(row=row, column=1, pady=5, padx=(10, 0))
        row += 1

        # Pass type selection
        ttk.Label(main_frame, text="Pass Type:").grid(row=row, column=0, sticky='w', pady=5)
        pass_type_options = [f"{pt.name} ({pt.category})" for pt in manager.pass_types.values()]
        self.pass_type_combo = ttk.Combobox(main_frame, width=35, values=pass_type_options, state='readonly')
        self.pass_type_combo.grid(row=row, column=1, pady=5, padx=(10, 0))
        row += 1

        # Issue date
        ttk.Label(main_frame, text="Issue Date:").grid(row=row, column=0, sticky='w', pady=5)
        self.date_entry = ttk.Entry(main_frame, width=30)
        self.date_entry.insert(0, datetime.now().strftime('%Y-%m-%d'))
        self.date_entry.grid(row=row, column=1, pady=5, padx=(10, 0))
        row += 1

        # Help text
        help_label = ttk.Label(main_frame, text="Issue date format: YYYY-MM-DD", font=('Arial', 8))
        help_label.grid(row=row, column=1, sticky='w', padx=(10, 0))
        row += 1

        # Buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=row, column=0, columnspan=2, pady=20)

        ttk.Button(button_frame, text="Issue Pass", command=self.issue_pass).pack(side='right', padx=5)
        ttk.Button(button_frame, text="Cancel", command=self.cancel).pack(side='right')

        # Focus on employee combo
        self.employee_combo.focus()

        # Bind keys
        self.dialog.bind('<Escape>', lambda e: self.cancel())

        # Wait for dialog to close
        self.dialog.wait_window()

    def issue_pass(self):
        # Validate selections
        employee_selection = self.employee_combo.get()
        pass_type_selection = self.pass_type_combo.get()
        issue_date = self.date_entry.get().strip()

        if not employee_selection:
            messagebox.showerror("Validation Error", "Please select an employee")
            return

        if not pass_type_selection:
            messagebox.showerror("Validation Error", "Please select a pass type")
            return

        # Extract IDs from selections
        employee_id = employee_selection.split('(')[-1].rstrip(')')
        pass_type_id = None

        # Find pass type ID
        for pt in self.manager.pass_types.values():
            if f"{pt.name} ({pt.category})" == pass_type_selection:
                pass_type_id = pt.pass_type_id
                break

        # Validate date format
        try:
            datetime.strptime(issue_date, '%Y-%m-%d')
        except ValueError:
            messagebox.showerror("Validation Error", "Please enter date in YYYY-MM-DD format")
            self.date_entry.focus()
            return

        self.result = {
            'employee_id': employee_id,
            'pass_type_id': pass_type_id,
            'issue_date': issue_date
        }
        self.dialog.destroy()

    def cancel(self):
        self.dialog.destroy()


class TestEmailDialog:
    def __init__(self, parent):
        self.result = None

        # Create dialog window
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("Send Test Email")
        self.dialog.geometry("350x150")
        self.dialog.resizable(False, False)
        self.dialog.transient(parent)
        self.dialog.grab_set()

        # Center the dialog
        self.dialog.geometry("+%d+%d" % (parent.winfo_rootx() + 150, parent.winfo_rooty() + 150))

        # Create form
        main_frame = ttk.Frame(self.dialog, padding=20)
        main_frame.pack(fill='both', expand=True)

        ttk.Label(main_frame, text="Enter email address to send test notification:").pack(pady=5)

        self.email_entry = ttk.Entry(main_frame, width=40)
        self.email_entry.pack(pady=10)

        button_frame = ttk.Frame(main_frame)
        button_frame.pack(pady=10)

        ttk.Button(button_frame, text="Send Test", command=self.send_test).pack(side='right', padx=5)
        ttk.Button(button_frame, text="Cancel", command=self.cancel).pack(side='right')

        self.email_entry.focus()
        self.dialog.bind('<Return>', lambda e: self.send_test())
        self.dialog.bind('<Escape>', lambda e: self.cancel())

        self.dialog.wait_window()

    def send_test(self):
        email = self.email_entry.get().strip()
        if not email:
            messagebox.showerror("Validation Error", "Please enter an email address")
            return

        if '@' not in email or '.' not in email:
            messagebox.showerror("Validation Error", "Please enter a valid email address")
            return

        self.result = email
        self.dialog.destroy()

    def cancel(self):
        self.dialog.destroy()


class EmailSettingsDialog:
    def __init__(self, parent, current_config):
        self.result = None

        # Create dialog window
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("Email Settings")
        self.dialog.geometry("400x300")
        self.dialog.resizable(False, False)
        self.dialog.transient(parent)
        self.dialog.grab_set()

        # Center the dialog
        self.dialog.geometry("+%d+%d" % (parent.winfo_rootx() + 100, parent.winfo_rooty() + 100))

        # Create form
        main_frame = ttk.Frame(self.dialog, padding=20)
        main_frame.pack(fill='both', expand=True)

        # Form fields
        fields = [
            ("SMTP Server:", "smtp_server"),
            ("SMTP Port:", "smtp_port"),
            ("Email Username:", "email_username"),
            ("Email Password:", "email_password")
        ]

        self.entries = {}

        for i, (label_text, field_name) in enumerate(fields):
            ttk.Label(main_frame, text=label_text).grid(row=i, column=0, sticky='w', pady=5)

            if field_name == "email_password":
                entry = ttk.Entry(main_frame, width=30, show="*")
            else:
                entry = ttk.Entry(main_frame, width=30)

            entry.grid(row=i, column=1, pady=5, padx=(10, 0))
            self.entries[field_name] = entry

            # Fill with current config
            if field_name in current_config:
                entry.insert(0, str(current_config[field_name]))

        # Info label
        info_frame = ttk.LabelFrame(main_frame, text="Common Settings", padding=10)
        info_frame.grid(row=len(fields), column=0, columnspan=2, pady=20, sticky='ew')

        info_text = """Gmail: smtp.gmail.com, port 587
Outlook: smtp-mail.outlook.com, port 587
Yahoo: smtp.mail.yahoo.com, port 587

Note: For Gmail, use App Password instead of regular password."""

        ttk.Label(info_frame, text=info_text, font=('Arial', 8)).pack()

        # Buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=len(fields) + 1, column=0, columnspan=2, pady=10)

        ttk.Button(button_frame, text="Save", command=self.save).pack(side='right', padx=5)
        ttk.Button(button_frame, text="Cancel", command=self.cancel).pack(side='right')

        self.entries['smtp_server'].focus()
        self.dialog.bind('<Escape>', lambda e: self.cancel())

        self.dialog.wait_window()

    def save(self):
        # Validate and collect data
        config = {}

        smtp_server = self.entries['smtp_server'].get().strip()
        smtp_port_str = self.entries['smtp_port'].get().strip()
        email_username = self.entries['email_username'].get().strip()
        email_password = self.entries['email_password'].get().strip()

        # Validation
        if not all([smtp_server, smtp_port_str, email_username, email_password]):
            messagebox.showerror("Validation Error", "Please fill in all fields")
            return

        try:
            smtp_port = int(smtp_port_str)
            if smtp_port <= 0 or smtp_port > 65535:
                raise ValueError()
        except ValueError:
            messagebox.showerror("Validation Error", "Please enter a valid port number (1-65535)")
            return

        config = {
            'smtp_server': smtp_server,
            'smtp_port': smtp_port,
            'email_username': email_username,
            'email_password': email_password
        }

        self.result = config
        self.dialog.destroy()

    def cancel(self):
        self.dialog.destroy()


def main():
    """Main function to run the GUI application"""
    root = tk.Tk()
    app = SafetyPassGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()