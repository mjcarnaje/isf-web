from flask import current_app, url_for, render_template
from flask_mail import Message
from ..mail import mail
from ..config import Config
import os

def send_verification_email(email: str, token: str, user):
    try:
        current_app.logger.info("Sending Verification Email")
        
        sender_name = "ISF Team"
        sender_email = "from@example.com"

        verification_link = url_for('landing.verify_account', token=token, _external=True)

        msg = Message("Verification Email",
                      sender=(sender_name, sender_email),
                      recipients=[email])
        msg.html = render_template('verify-account-template.html', user=user, verification_link=verification_link)
        mail.send(msg)
        current_app.logger.info("Verification Email sent!")

    except Exception as e:
        current_app.logger.error(f"Error sending verification email to {email}: {str(e)}")
        # Optionally, you can raise the exception again or handle it in a way that fits your application's requirements.
    finally:
        print("Send")