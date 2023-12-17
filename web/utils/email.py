import os

import requests
from celery import shared_task
from flask import current_app, render_template, url_for
from flask_mail import Message

from ..mail import mail

def send_verification_email(email: str, token: str, user):
    try:
        current_app.logger.info("Sending Verification Email")
        
        verification_link = url_for('landing.verify_account', token=token, _external=True)

        sender_name = "ISF Team"
        sender_email = "team@isf.com"


        msg = Message(
            "Verification Email",
            sender=(sender_name, sender_email),
            recipients=[email]
        )

        msg.html = render_template('verify-account-template.html', user=user, verification_link=verification_link)
        
        msg.attach('logo.png', 'image/png', open(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'static', 'images', 'email_template', 'logo.png'), 'rb').read(), 'inline', headers=[('Content-ID', '<Logo>')])
        msg.attach('banner.jpeg', 'image/jpeg', open(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'static', 'images', 'email_template', 'banner.jpeg'), 'rb').read(), 'inline', headers=[('Content-ID', '<Banner>')])
        msg.attach('facebook.png', 'image/png', open(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'static', 'images', 'email_template', 'facebook.png'), 'rb').read(), 'inline', headers=[('Content-ID', '<Facebook>')])

        mail.send(msg)
        current_app.logger.info("Verification Email sent!")

    except Exception as e:
        current_app.logger.error(f"Error sending verification email to {email}: {str(e)}")
    finally:
        print("Send")


@shared_task()
def send_notification_email(subject, recipient_email, title, first_name, message, preview_image_url, sender_name, sender_email):
    try:
        msg = Message(
            subject=subject,
            sender=(sender_name, sender_email),
            recipients=[recipient_email]
        )
        msg.html = render_template('common-notification.html', title=title, first_name=first_name, message=message)

        logo_data = get_attach_data('logo.png', 'image/png', 'Logo')
        banner_data = get_attach_data('banner.jpeg', 'image/jpeg', 'Banner', remote_url=preview_image_url)
        facebook_data = get_attach_data('facebook.png', 'image/png', 'Facebook')

        msg.attach(*logo_data)
        msg.attach(*banner_data)
        msg.attach(*facebook_data)

        mail.send(msg)
    except Exception as e:
        current_app.logger.error(f"Error sending verification email to {recipient_email}: {str(e)}")
    finally:
        print("Send")



def get_attach_data(file_name, content_type, content_id, remote_url=None):
    if remote_url:
        file_data = requests.get(remote_url).content
    else:
        file_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'static', 'images', 'email_template', file_name)
        file_data = open(file_path, 'rb').read()

    attachment_data = (file_name, content_type, file_data, 'inline', [('Content-ID', f'<{content_id}>')])
    return attachment_data