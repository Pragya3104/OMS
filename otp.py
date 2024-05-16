import json
import pyotp 
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from auth import load_users

# Generate OTP
def generate_otp():
    totp = pyotp.TOTP(pyotp.random_base32())
    return totp.now()

# Send OTP via email
def send_otp(username):
    users = load_users()
    email = users[username]['email']
    otp = generate_otp()

    # Save OTP temporarily in user data (for demonstration purposes; ideally use a secure method)
    users[username]['otp'] = otp
    with open('data.json', 'w') as file:
        json.dump(users, file, indent=2)

    # Email setup
    sender_email = "pragyjha870@gmail.com"
    sender_password = "czdy qore tnop fadf"
    subject = "Your OTP Code"
    body = f"Your OTP code is {otp}"

    # Email message
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    # Send email
    try:
        server = smtplib.SMTP('smtp.example.com', 587)
        server.starttls()
        server.login(sender_email, sender_password)
        text = msg.as_string()
        server.sendmail(sender_email, email, text)
        server.quit()
        print("OTP sent successfully")
    except Exception as e:
        print(f"Failed to send OTP: {e}")

# Verify OTP
def verify_otp(username, otp_code):
    users = load_users()
    if username in users and users[username]['otp'] == otp_code:
        return True
    return False
