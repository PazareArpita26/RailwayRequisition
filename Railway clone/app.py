from flask import Flask, request, jsonify, render_template, flash, redirect, url_for
from datetime import datetime, timedelta
import smtplib
from email.mime.text import MIMEText
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build


app = Flask(__name__)

app.config['SECRET_KEY'] = '8f0d5b9534f3019c8650bdabe576992b'

# Google Sheets configuration
SERVICE_ACCOUNT_FILE = 'railwayrcc-f37d05c51345.json'
SPREADSHEET_ID = '131qwmJtwo6Np7dHQziK7rZQWUHlcBZrpX7j7CgA7Qx8'
SHEET_NAME = 'Sheet1'

# Authenticate with Google Sheets API
credentials = Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=['https://www.googleapis.com/auth/spreadsheets'])
service = build('sheets', 'v4', credentials=credentials)

# Function to calculate the due date excluding weekends
def calculate_due_date(start_date, business_days_to_add):
    current_date = start_date
    days_added = 0
    while days_added < business_days_to_add:
        current_date += timedelta(days=1)
        if current_date.weekday() < 5:  # Weekdays are 0-4
            days_added += 1
    return current_date.strftime('%d/%m/%Y')

# Function to send email
def send_email(to_email, subject, body):
    try:
        smtp_server = 'smtp.gmail.com'
        smtp_port = 587
        sender_email = 'chanupazare5@gmail.com'
        sender_password = 'wjfz tnra bunh wymq'  # Make sure to use environment variables for real credentials
        
        msg = MIMEText(body)
        msg['Subject'] = subject
        msg['From'] = sender_email
        msg['To'] = to_email

        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, to_email, msg.as_string())
        server.quit()
    except Exception as e:
        print(f"Error sending email: {e}")

@app.route('/')
def home():
    return render_template('index.html') 

@app.route('/post', methods=['POST'])
def do_post():
    try:
        # Extracting parameters from the request
        form_data = request.form
        email = form_data.get('email')
        uid = form_data.get('uid')
        full_name = form_data.get('full-name')
        address = form_data.get('address')
        mobile = form_data.get('mobile')
        class_roll = form_data.get('class-roll')
        gender = form_data.get('gender')
        dob = form_data.get('dob')
        age = form_data.get('age')
        period = form_data.get('period')
        class_travel = form_data.get('class-travel')
        category = form_data.get('category')
        station = form_data.get('station')
        date = form_data.get('date')

        # Fetch existing data from the spreadsheet
        sheet = service.spreadsheets()
        result = sheet.values().get(spreadsheetId=SPREADSHEET_ID, range=SHEET_NAME).execute()
        rows = result.get('values', [])

        # Check if the student has already applied within the restricted period
        now = datetime.now()
        rcc_period_days = 30 if period == 'Monthly' else 90

        for row in rows[1:]:  # Skip header row
            submission_date = datetime.strptime(row[0], '%Y-%m-%d %H:%M:%S')  # Assuming date is in column 0
            existing_email = row[1]  # Assuming email is in column 1
            if existing_email == email:
                diff_in_days = (now - submission_date).days
                if diff_in_days < rcc_period_days:
                    remaining_days = rcc_period_days - diff_in_days
                    message = f"""Dear {full_name},

You have already submitted the Railway Requisition Form. You can reapply only after {remaining_days} days.

Thank you for your understanding.

Kindly Note, 
           In the instances of gennuine reason you can resubmit the form in the office managery for which you have to 
           visit personally to the staff of the Railway Concession.

Best regards,
Railway Requisition Team"""
                    send_email(email, 'Reapplication Restricted', message)
                    return jsonify({'message': 'You cannot reapply until the RCC period has expired. A notification has been sent to your email.'}), 400

        # Append the form data to the spreadsheet
        new_row = [now.strftime('%Y-%m-%d %H:%M:%S'), email, uid, full_name, address, mobile, class_roll, gender, dob, age, period, class_travel, category, station, date]
        sheet.values().append(
            spreadsheetId=SPREADSHEET_ID,
            range=SHEET_NAME,
            valueInputOption='RAW',
            insertDataOption='INSERT_ROWS',
            body={'values': [new_row]}
        ).execute()

        # Calculate the due date and send a success email
        due_date = calculate_due_date(now, 3)
        success_message = f"""Dear {full_name},

Thank you for submitting the Railway Requisition Form. Please collect your Railway Certificate by {due_date}.

Note: You will not be able to reapply until the selected RCC period ({period}) has expired. Your RCC period ends on {(now + timedelta(days=rcc_period_days)).strftime('%d/%m/%Y')}

Kindly Note, 
           In the instances of gennuine reason you can resubmit the form in the office managery for which you have to visit personally to the staff of the Railway Concession.

Best regards,
Railway Requisition Team"""
        send_email(email, 'Form Submission Confirmation', success_message)
        # flash('Form submitted successfully! You will receive a confirmation email shortly.', 'success')
        # return redirect(url_for('home'))

        return jsonify({'status':'success', 'message': 'Form submitted successfully! A confirmation email has been sent.'}), 200

    except Exception as e:
        print(f"Error: {e}")
        # flash(f"Error: {str(e)}", 'error')
        # return redirect(url_for('home'))
        return jsonify({'status':'error', 'message': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
