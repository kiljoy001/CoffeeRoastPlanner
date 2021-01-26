# Events.py
from enum import Enum, unique


@unique
class EventType(Enum):
    """
    Contains an enumeration for each type of event:
    temperature, turning point, charge temperature, time
    """
    pass


class Event:
    """
    Describes and event and has an event_id.
    returns an event as event_id paired with a list
    that contains the event type and data value
    """
    pass
