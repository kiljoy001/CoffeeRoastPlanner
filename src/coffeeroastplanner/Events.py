# Events.py
from enum import Enum, unique


@unique
class EventType(Enum):
    """
    Contains an enumeration for each type of event:
    temperature, turning point, charge temperature, time, fuel
    """
    temperature = 1
    turning_point = 2
    charge_temperature = 3
    time = 4
    fuel = 5


class Event:
    """
    Describes an event and has an event_id.
    returns an event as event_id paired with a list
    that contains the event type and data value
    """
    pass
