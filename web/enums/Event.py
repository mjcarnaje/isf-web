from enum import Enum

class EventStatus(Enum):
  SCHEDULED = 'Scheduled'
  IN_PROGRESS = 'In Progress'
  COMPLETED = 'Completed'
  CANCELLED = 'Cancelled'