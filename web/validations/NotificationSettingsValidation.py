from flask_wtf import FlaskForm
from wtforms import BooleanField

class NotificationSettingsValidation(FlaskForm):
    adoption_status_update_web = BooleanField("Receive Adoption Status Updates")
    donation_status_update_web = BooleanField("Receive Donation Status Updates")
    event_invited_web = BooleanField("Receive Event Invitations")
    confirm_join_org_request_web = BooleanField("Confirm Join Organization Requests")
    reject_join_org_request_web = BooleanField("Reject Join Organization Requests")

    adoption_status_update_email = BooleanField("Receive Adoption Status Updates via Email")
    donation_status_update_email = BooleanField("Receive Donation Status Updates via Email")
    event_invited_email = BooleanField("Receive Event Invitations via Email")
    confirm_join_org_request_email = BooleanField("Confirm Join Organization Requests via Email")
    reject_join_org_request_email = BooleanField("Reject Join Organization Requests via Email")
