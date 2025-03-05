import smtplib, ssl
from email.mime.text import MIMEText


# extraxt emails from the 
def send_email(email, msg):
    # Define the email parameters
    smtp_server = "smtp.gmail.com"
    smtp_port = 465
    context = ssl.create_default_context()

    from_email = "calendarappautomation@gmail.com"
    to_email = email
    password = "izhx upxp uxyx lgya"

    # Define the email content
    subject = "Test Email from Python"
    body = msg

    # Create a text message
    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = from_email
    msg["To"] = to_email

    with smtplib.SMTP_SSL(smtp_server, smtp_port, context=context) as server:
        # Send the email
        server.ehlo()
        server.login(from_email, password)
        server.sendmail(from_email, to_email, msg.as_string())
        server.quit()

    print("Email sent successfully!")

#email
# calendarappautomation@gmail.com
#ppaww
# calpassword