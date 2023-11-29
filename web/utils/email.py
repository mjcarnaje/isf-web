import os

from flask import current_app, render_template, url_for
from flask_mail import Message

from ..config import Config
from ..mail import mail


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
        
        msg.attach('logo.png', 'image/png', open(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'static', 'images', 'email_template', 'logo.png'), 'rb').read(), 'inline', headers=[('Content-ID', '<Logo>')])
        msg.attach('banner.jpeg', 'image/jpeg', open(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'static', 'images', 'email_template', 'banner.jpeg'), 'rb').read(), 'inline', headers=[('Content-ID', '<Banner>')])
        msg.attach('facebook.png', 'image/png', open(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'static', 'images', 'email_template', 'facebook.png'), 'rb').read(), 'inline', headers=[('Content-ID', '<Facebook>')])

        mail.send(msg)
        current_app.logger.info("Verification Email sent!")

    except Exception as e:
        current_app.logger.error(f"Error sending verification email to {email}: {str(e)}")
        # Optionally, you can raise the exception again or handle it in a way that fits your application's requirements.
    finally:
        print("Send")