# Email Configuration Example
# Copy this file to config.py and update with your actual settings

EMAIL_CONFIG = {
    'smtp_server': 'smtp.gmail.com',  # Gmail SMTP server
    'smtp_port': 587,
    'email_username': 'your_company_email@gmail.com',  # Your email
    'email_password': 'your_app_password',  # Gmail app password (not your regular password)
}

# For Gmail:
# 1. Enable 2-factor authentication
# 2. Generate an app password: https://support.google.com/accounts/answer/185833
# 3. Use the app password here, not your regular Gmail password

# For other email providers:
# Outlook/Hotmail: smtp-mail.outlook.com, port 587
# Yahoo: smtp.mail.yahoo.com, port 587
# Custom SMTP: Check with your IT department

# Alternative email providers configuration examples:
OUTLOOK_CONFIG = {
    'smtp_server': 'smtp-mail.outlook.com',
    'smtp_port': 587,
    'email_username': 'your_email@outlook.com',
    'email_password': 'your_password',
}

YAHOO_CONFIG = {
    'smtp_server': 'smtp.mail.yahoo.com',
    'smtp_port': 587,
    'email_username': 'your_email@yahoo.com',
    'email_password': 'your_app_password',
}