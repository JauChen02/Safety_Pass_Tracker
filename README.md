# Safety Pass Management System

A comprehensive safety pass tracking system with both **Command Line** and **User-Friendly GUI** interfaces. Designed to automate the management of employee safety passes and their expiry dates with automated email notifications.

## 🎯 For Tech-Illiterate Managers

**Just want to use the app? Follow these simple steps:**

### **Windows Users (Easiest)**
1. Download all files to a folder on your computer
2. **Double-click `Start Safety Pass App.bat`**
3. The app will automatically install any missing components
4. The user-friendly interface will open automatically!

### **All Users (Easy)**
1. Download all files to a folder on your computer  
2. **Double-click `run_app.py`**
3. The graphical interface will start automatically

### **What You'll See**
- **Dashboard** - Overview of your safety passes and statistics
- **Employees Tab** - Add, edit, and manage employee information with simple forms
- **Pass Types Tab** - Create different types of safety passes with dropdown menus
- **Safety Passes Tab** - Issue passes to employees using easy dropdown selections
- **Reports Tab** - Generate reports with the click of a button

**No command line knowledge needed!** Everything is point-and-click with dropdown menus, forms, and buttons.

---

## 🚀 Features

### **For Managers (GUI Interface)**
- **Visual Dashboard** with real-time statistics
- **Easy Employee Management** - Add/edit employees with simple forms
- **Dropdown-Based Pass Issuance** - Select employee and pass type from lists
- **One-Click Reports** - Generate expiring passes, statistics, and summaries
- **Automated Email Notifications** - System sends reminders automatically
- **CSV Integration** - Edit data in Excel when needed
- **Built-in Help** - Tooltips and guidance throughout the interface

### **For Developers (Command Line Interface)**
- Object-oriented design with clean class structure
- CSV data storage for Excel compatibility
- Automated email notifications 15-1 days before expiry
- Comprehensive reporting and analytics
- Background scheduling for daily checks

---

## 📁 File Structure

After setup, your folder will contain:

```
safety-pass-management/
├── Start Safety Pass App.bat    # 🖱️ CLICK THIS (Windows users)
├── run_app.py                   # 🖱️ OR CLICK THIS (All users)
├── safety_pass_gui.py           # GUI application code
├── safety_pass_system.py        # Core system logic
├── main.py                      # Command line interface
├── config_example.py            # Email configuration template
├── requirements.txt             # Python dependencies
├── README.md                    # This file
└── safety_pass_data/            # Data folder (created automatically)
    ├── employees.csv            # Employee data
    ├── pass_types.csv           # Safety pass types
    └── safety_passes.csv        # Issued safety passes
```

---

## 🎮 Using the GUI Application

### **Starting the Application**
The easiest way is to double-click one of these files:
- **`Start Safety Pass App.bat`** (Windows - automatic setup)
- **`run_app.py`** (All platforms - automatic setup)

### **Main Interface Overview**

#### **🏠 Dashboard Tab**
- **System Statistics** - See total employees, passes, expiring passes at a glance
- **Quick Action Buttons** - Add employees, issue passes, check notifications
- **Color-coded Alerts** - Red numbers indicate urgent attention needed

#### **👥 Employees Tab**
- **Employee List** - View all employees in an organized table
- **Add Employee** - Simple form with dropdown menus
- **Edit/Remove** - Right-click or use buttons to modify employee data
- **Search & Filter** - Find employees quickly

#### **🏷️ Pass Types Tab**
- **Manage Pass Categories** - Create pass types like "Confined Space", "Heights", etc.
- **Set Validity Periods** - Define how long each pass type lasts
- **Categorize Passes** - Organize by Safety, Operations, Technical, etc.

#### **🎫 Safety Passes Tab**
- **Issue New Passes** - Select employee and pass type from dropdown menus
- **Filter Passes** - View active, expired, or specific employee passes
- **Automatic Expiry Calculation** - System calculates expiry dates automatically
- **Visual Status Indicators** - See pass status at a glance

#### **📊 Reports Tab**
- **One-Click Reports** - Generate various reports instantly
- **Expiring Passes Report** - See who needs renewal soon
- **Employee Summaries** - View all passes per employee
- **System Statistics** - Overall system health and usage

### **Common Tasks**

#### **Adding a New Employee**
1. Go to **👥 Employees** tab
2. Click **➕ Add Employee**
3. Fill in the simple form (all fields required)
4. Click **Save**

#### **Issuing a Safety Pass**
1. Go to **🎫 Safety Passes** tab
2. Click **🎫 Issue New Pass**
3. Select employee from dropdown
4. Select pass type from dropdown
5. Set issue date (defaults to today)
6. Click **Issue Pass**

#### **Checking Who Needs Renewal**
1. Go to **📊 Reports** tab
2. Click **⏰ Expiring Passes (Next 15 Days)**
3. View the report showing who needs renewal

#### **Sending Email Notifications**
1. Go to **Tools** menu → **Check Expiring Passes**
2. System automatically sends emails to employees
3. Or use **Tools** → **Send Test Email** to test your email setup

---

## ⚙️ Installation & Setup

### **For Managers (Simple Setup)**

**Step 1: Get the Files**
- Download all files to a folder on your computer

**Step 2: Run the Application**
- Windows: Double-click `Start Safety Pass App.bat`
- Other: Double-click `run_app.py`

**Step 3: First Time Setup**
- App will ask if you want sample data - click "Yes" for testing
- Use **Tools** → **Email Settings** to configure your company email

**That's it!** The application handles everything else automatically.

### **For Developers (Advanced Setup)**

**Prerequisites:**
- Python 3.7 or higher
- Internet connection for email notifications

**Installation:**
```bash
# Clone or download the repository
git clone https://github.com/yourusername/safety-pass-management.git
cd safety-pass-management

# Install dependencies
pip install -r requirements.txt

# Run GUI application
python safety_pass_gui.py

# OR run command line application
python main.py
```

---

## 📧 Email Configuration

### **Using the GUI**
1. Go to **Tools** → **Email Settings**
2. Enter your email server details:
   - **Gmail**: `smtp.gmail.com`, port `587`
   - **Outlook**: `smtp-mail.outlook.com`, port `587` 
   - **Yahoo**: `smtp.mail.yahoo.com`, port `587`
3. Use your email and app password
4. Click **Save**

### **Gmail Setup (Recommended)**
1. Enable 2-factor authentication on Gmail
2. Generate an app password: [Gmail App Passwords](https://support.google.com/accounts/answer/185833)
3. Use your Gmail address and the app password in settings

### **Test Your Email**
- Use **Tools** → **Send Test Email** to verify your configuration

---

## 📊 Data Management

### **Easy Excel Editing**
- Click **📂 Open Data Folder** in the GUI
- Edit CSV files directly in Excel for bulk changes
- Save the files and refresh the application

### **CSV Files Explained**
- **`employees.csv`** - Employee information and email addresses
- **`pass_types.csv`** - Different safety pass categories and validity periods
- **`safety_passes.csv`** - Issued passes with expiry dates

### **Backup Your Data**
- Use **File** → **Open Data Folder** to find your data
- Copy the entire `safety_pass_data` folder to backup

---

## 🔔 Automated Notifications

### **How It Works**
- System automatically emails employees 15-1 days before pass expiry
- Different message urgency based on days remaining
- Personalized emails with employee name and pass details

### **Sample Email**
```
Dear John Smith,

This is a reminder that your safety pass 'Confined Space Entry' 
will expire in 5 days.

Please plan to renew your pass in advance to ensure uninterrupted 
site access.

If you have any questions, please contact your manager.

Best regards,
Safety Pass Management System
```

### **Setting Up Daily Checks**
- **Manual**: Use **Tools** → **Check Expiring Passes**
- **Automatic**: Leave the application running - it checks daily at 9 AM

---

## 🎯 Quick Start Guide

### **For New Users**
1. **Double-click** `run_app.py` or `Start Safety Pass App.bat`
2. When prompted, choose **"Yes"** to create sample data
3. Explore the different tabs to familiarize yourself
4. Configure email settings in **Tools** → **Email Settings**
5. Start adding your real employees and pass types

### **Daily Workflow**
1. **Start app** (double-click launcher)
2. **Check Dashboard** for expiring passes alerts
3. **Add new employees** as needed
4. **Issue passes** to employees
5. **Run email check** before leaving for the day

---

## 🔧 Troubleshooting

### **Application Won't Start**
- Make sure Python is installed (application will guide you)
- Try running `run_app.py` instead of the batch file
- Check that all files are in the same folder

### **Email Issues**
- Use **Tools** → **Send Test Email** to test configuration
- For Gmail, ensure you're using an App Password, not your regular password
- Check firewall settings if corporate network blocks email

### **Data Issues**
- Use **File** → **Open Data Folder** to check CSV files
- Close Excel before running the application
- Use **🔄 Refresh Data** button if data seems outdated

### **Common Solutions**
- **Restart the application** - fixes most display issues
- **Check email configuration** - most issues are email-related
- **Verify CSV files** - ensure they're not corrupted or locked

---

## 🎨 Interface Features

### **User-Friendly Design**
- **Large, clear buttons** with icons
- **Color-coded status indicators** (red = urgent, green = good)
- **Tooltips and help text** throughout the interface
- **Familiar spreadsheet-style data display**

### **Accessibility Features**
- **Large fonts** for easy reading
- **High contrast colors** for visibility
- **Keyboard shortcuts** for common actions
- **Simple navigation** with clearly labeled tabs

### **Professional Appearance**
- **Clean, modern interface** suitable for business use
- **Consistent styling** throughout the application
- **Status bar** showing current time and system messages
- **Menu system** for advanced features

---

## 💡 Tips for Managers

### **Best Practices**
- **Daily Check**: Start each day by checking the Dashboard for urgent renewals
- **Bulk Updates**: Use Excel to edit CSV files for large employee list changes
- **Regular Backups**: Copy your data folder weekly to prevent data loss
- **Email Testing**: Send test emails monthly to ensure notifications work

### **Time-Saving Features**
- **Quick Actions** on Dashboard for common tasks
- **Filter options** to find specific employees or passes quickly
- **One-click reports** instead of manual tracking
- **Automatic expiry calculations** - no manual date math needed

### **Customization**
- **Pass Categories**: Create pass types that match your facility needs
- **Validity Periods**: Set different expiry periods for different pass types
- **Email Templates**: Messages automatically personalize with employee names

---

## 🆘 Support

### **Getting Help**
- **Built-in Help**: Use **Help** → **About** for system information
- **Sample Data**: Use **File** → **Setup Sample Data** for testing
- **Email Test**: Use **Tools** → **Send Test Email** to verify email setup

### **Technical Support**
- Check the troubleshooting section above
- Verify all files are in the same folder
- Ensure Python is properly installed
- Test with sample data first

### **Feature Requests**
This system is designed to be easily customizable. Common requests include:
- Additional pass categories
- Custom email templates  
- Integration with existing HR systems
- Advanced reporting features

---

## 📜 License

This software is provided as-is for internal company use. Modify as needed for your organization's requirements.

**Built for safety professionals who want automation without complexity.**

---

*For technical details and advanced configuration, see the developer documentation below.*

## Email Configuration

### For Gmail (Recommended)
1. Enable 2-factor authentication on your Gmail account
2. Generate an app password: [Gmail App Passwords](https://support.google.com/accounts/answer/185833)
3. Update `config.py` with your Gmail address and app password

### For Other Email Providers
- **Outlook**: `smtp-mail.outlook.com`, port 587
- **Yahoo**: `smtp.mail.yahoo.com`, port 587
- **Corporate Email**: Check with your IT department for SMTP settings

## File Structure

After running the application, the following structure will be created:

```
safety_pass_management/
├── safety_pass_system.py      # Main application code
├── main.py                    # Application entry point
├── config.py                  # Email configuration (create from config_example.py)
├── config_example.py          # Example configuration
├── requirements.txt           # Python dependencies
├── README.md                  # This file
└── safety_pass_data/          # Data folder (created automatically)
    ├── employees.csv          # Employee data
    ├── pass_types.csv         # Safety pass types
    └── safety_passes.csv      # Issued safety passes
```

## CSV Data Management

All data is stored in CSV format for easy management:

### employees.csv
- **employee_id**: Unique identifier for each employee
- **name**: Employee full name
- **email**: Employee email address for notifications
- **department**: Employee department
- **manager**: Employee's manager

### pass_types.csv
- **pass_type_id**: Unique identifier for pass type
- **name**: Display name of the pass
- **description**: Description of what the pass allows
- **category**: Category (e.g., Safety, Operations, Technical)
- **validity_period_days**: How many days the pass is valid

### safety_passes.csv
- **pass_id**: Unique identifier for each issued pass
- **employee_id**: Which employee has this pass
- **pass_type_id**: Type of safety pass
- **issue_date**: When the pass was issued
- **expiry_date**: When the pass expires
- **status**: active, expired, or revoked

**Manager Tip**: You can edit these CSV files directly in Excel to make bulk changes when needed!

## Usage Guide

### Starting the Application
Run `python main.py` and choose from the main menu:

1. **Admin Interface**: Full management capabilities
2. **Notification Check**: Manual check for expiring passes
3. **Daily Scheduler**: Automated daily notifications
4. **Sample Data**: Set up test data
5. **System Status**: View current system state

### Daily Operations

#### Adding New Employees
1. Use Admin Interface → Employee Management → Add Employee
2. Or edit `employees.csv` directly in Excel

#### Creating Safety Pass Types
1. Use Admin Interface → Safety Pass Type Management → Add Pass Type
2. Define the validity period (e.g., 365 days for annual passes)

#### Issuing Safety Passes
1. Use Admin Interface → Safety Pass Management → Issue Safety Pass
2. The system automatically calculates expiry dates based on pass type

#### Managing Expiring Passes
- The system automatically emails employees 15-1 days before expiration
- Run daily notification checks manually or set up automated scheduling
- View expiring passes in the Reports menu

### Automated Email Notifications

The system sends personalized emails to employees:
- **15-2 days before expiry**: Regular reminder
- **1 day before expiry**: Urgent reminder with different message

Sample email content:
```
Dear John Smith,

This is a reminder that your safety pass 'Confined Space Entry' 
will expire in 5 days.

Please plan to renew your pass in advance to ensure uninterrupted 
site access.

If you have any questions, please contact your manager.

Best regards,
Safety Pass Management System
```

## Setting Up Automated Daily Checks

### Option 1: Manual Daily Checks
Run the application daily and select "Run Notification Check"

### Option 2: Automated Scheduler
1. Run the application
2. Select "Start Daily Notification Scheduler"
3. The system will check for expiring passes daily at 9:00 AM
4. Keep the application running on a server or dedicated computer

### Option 3: System Scheduler (Advanced)
Set up your operating system to run the notification check:

**Windows Task Scheduler**:
- Create a task to run `python main.py` with argument for notification check
- Schedule it to run daily

**Linux/Mac Cron**:
```bash
# Edit crontab
crontab -e

# Add line to run daily at 9 AM
0 9 * * * cd /path/to/safety_pass_management && python main.py --notify
```

## Reports and Monitoring

The system provides several reports:
- **Expiring Passes**: Shows passes expiring in the next 15 days
- **Expired Passes**: Shows passes that have already expired
- **Active Passes**: Shows all currently valid passes
- **Employee Summary**: Shows pass status for specific employees
- **System Summary**: Overall statistics

## Troubleshooting

### Email Issues
- **Authentication Failed**: Check your email credentials in `config.py`
- **Gmail Issues**: Ensure 2-factor authentication is enabled and you're using an app password
- **Corporate Email**: Contact IT for SMTP settings and firewall permissions

### CSV File Issues
- **File Locked**: Close Excel before running the application
- **Data Corruption**: The application creates backups; check the data folder
- **Character Encoding**: Ensure CSV files are saved in UTF-8 format

### Common Problems
- **Employee Not Found**: Check that employee_id matches exactly (case-sensitive)
- **Pass Type Not Found**: Verify the pass_type_id exists in pass_types.csv
- **Date Format Issues**: Use YYYY-MM-DD format for all dates

## Security Considerations

- Store email passwords securely (consider using environment variables for production)
- Regularly backup the `safety_pass_data` folder
- Restrict access to the data folder to authorized personnel only
- Consider encrypting sensitive email configuration files

## Support and Maintenance

### Regular Maintenance Tasks
1. **Weekly**: Review expiring passes report
2. **Monthly**: Check for expired passes and update employee status
3. **Quarterly**: Review and update safety pass types and validity periods
4. **Annually**: Backup all data and review system performance

### Data Backup
Regularly backup the `safety_pass_data` folder to prevent data loss.

## Customization

The system is designed to be easily customizable:
- Modify notification email templates in `safety_pass_system.py`
- Adjust notification timing (currently 15-1 days before expiry)
- Add new fields to CSV files and corresponding data classes
- Customize the admin interface menus

## License

This software is provided as-is for internal company use. Modify as needed for your organization's requirements.

---

For technical support or feature requests, contact your system administrator.