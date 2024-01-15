"""Emails module"""

from flask import url_for, render_template, current_app
from flask_mail import Message
from recipeapp import mail
import threading

def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)
        print('email sent')

def send_email(email, subject, template, template_data):
    try:
        with current_app.app_context():
                msg_title = subject
                sender = "muazuidrisyakub@yahoo.com"
                msg = Message(msg_title, sender=sender, recipients=[email])
                msg.html = render_template(template, data=template_data)
                thr = threading.Thread(
                    target=send_async_email,
                    args=(current_app._get_current_object(), msg))
                thr.start()
    except Exception as e:
        return {'msg': 'Email not sent', 'error': str(e)}

# Sending password reset email
def reset_password_otp(name, email, otp):
    try:
        subject = 'Verification Code'
        template = 'password-reset.html'
        template_data = {
            'app_name': 'Recipe Book',
            'title': 'Password Reset OTP - Recipe Book',
            'body':
                'Please use this verification code to reset your password',
            'name': name,
            'otp': otp
        }
        print('sending email')
        send_email(email, subject, template, template_data)
    except Exception as e:
        print(f"Error sending email: {e}")

# Sending OTP for registration or password reset
def send_otp_email(name, email, otp):
    subject = 'Verification Code'
    template = 'email_otp.html'
    template_data = {
        'app_name': 'Recipe Book',
        'title': 'Registration Confirmation - Recipe Book',
        'body':
            'Please use this verification code to confirm your registration',
        'name': name,
        'otp': otp
    }
    send_email(email, subject, template, template_data)

# Sending welcome email
def welcome_email(name, email):
    subject = 'Welcome to Foodie'
    template = 'welcome_email.html'
    template_data = {
        'app_name': 'Recipe Book',
        'title': 'Welcome to Foodie - Recipe Book',
        'body':
            'Thank you for joining us on this delicious journey!\ Explore our\
                app and discover amazing recipes to satisfy your cravings.',
        'name': name
    }
    send_email(email, subject, template, template_data)

# Sending promotion to admin email
def promotion_email(name, email):
    subject = 'Promotion to Admin'
    template = 'to_admin.html'
    template_data = {
        'app_name': 'Recipe Book',
        'title': 'Welcome to Admins Team - Recipe Book',
        'body':
            'Your dedication and hard work have paid off. Welcome to the\
                admin team! Your new responsibilities and privileges await.',
        'name': name
    }
    send_email(email, subject, template, template_data)