from enum import Enum

class DonationFor(Enum):
  General = 'General'
  Event = 'Event'
  Animal = 'Animal'

class DonationType(Enum):
  Money = 'Money'
  InKind = 'In-Kind'

class DonationDeliveryType(Enum):
  PickUp = 'Pick-up'
  Deliver = 'Deliver'