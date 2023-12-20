from enum import Enum

class EventStatus(Enum):
  SCHEDULED = 'Scheduled'
  IN_PROGRESS = 'In Progress'
  COMPLETED = 'Completed'
  CANCELLED = 'Cancelled'

class WhoCanJoinEvent(Enum):
  ANYONE = 'Anyone'
  VERIFIED_USERS = 'Verified Users'
  MEMBER_ONLY = 'Member-Only'