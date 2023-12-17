
from flask_wtf import FlaskForm
from wtforms import BooleanField



class NotificationSettingsValidation(FlaskForm):
    adoption_status_update_web = BooleanField("Receive Adoption Status Updates")
    donation_status_update_web = BooleanField("Receive Donation Status Updates")
    event_invited_web = BooleanField("Receive Event Invitations")

    adoption_status_update_email = BooleanField("Receive Adoption Status Updates")
    donation_status_update_email = BooleanField("Receive Donation Status Updates")
    event_invited_email = BooleanField("Receive Event Invitations")

   