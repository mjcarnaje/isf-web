from enum import Enum

class NotificationType(Enum):
    ADOPTION_REQUEST = 'ADOPTION_REQUEST'
    ADOPTION_STATUS_UPDATE = 'ADOPTION_STATUS_UPDATE'
    ADD_DONATION_MONEY = 'ADD_DONATION_MONEY'
    ADD_DONATION_IN_KIND = 'ADD_DONATION_IN_KIND'
    DONATION_STATUS_UPDATE = 'DONATION_STATUS_UPDATE'
    EVENT_INVITED = 'EVENT_INVITED'

    def get_email_subject(self):
        if self == NotificationType.ADOPTION_REQUEST:
            return "Adoption Request Notification"
        elif self == NotificationType.ADOPTION_STATUS_UPDATE:
            return "Adoption Status Update Notification"
        elif self == NotificationType.ADD_DONATION_MONEY:
            return "Donation Money Notification"
        elif self == NotificationType.ADD_DONATION_IN_KIND:
            return "Donation In Kind Notification"
        elif self == NotificationType.DONATION_STATUS_UPDATE:
            return "Donation Status Update Notification"
        elif self == NotificationType.EVENT_INVITED:
            return "Event Invitation Notification"

    def get_email_title(self):
        if self == NotificationType.ADOPTION_REQUEST:
            return "New Adoption Request"
        elif self == NotificationType.ADOPTION_STATUS_UPDATE:
            return "Adoption Status Updated"
        elif self == NotificationType.ADD_DONATION_MONEY:
            return "New Donation Received"
        elif self == NotificationType.ADD_DONATION_IN_KIND:
            return "New In-Kind Donation Received"
        elif self == NotificationType.DONATION_STATUS_UPDATE:
            return "Donation Status Updated"
        elif self == NotificationType.EVENT_INVITED:
            return "You're Invited to an Event"
