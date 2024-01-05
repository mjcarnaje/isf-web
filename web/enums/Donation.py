from enum import Enum

class DonationFor(Enum):
  General = 'General'
  AnimalHelp = 'Animal Help'

class DonationType(Enum):
  Money = 'Money'
  InKind = 'In-Kind'

class DonationDeliveryType(Enum):
  PickUp = 'Pick-up'
  Deliver = 'Deliver'