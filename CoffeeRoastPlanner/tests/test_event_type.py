from Events import EventType
from enum import Enum


class TestEventType:
    def test_event_type_numeration_returns_correct_value(self):
        assert EventType(1) == EventType.temperature, 'EventType temperature failed'
        assert EventType(2) == EventType.turning_point, 'EventType turning point failed'
        assert EventType(3) == EventType.charge_temperature, 'EventType charge temperature failed'
        assert EventType(4) == EventType.time, 'EventType time failed'

    def test_event_type_enumerations_are_unique(self):
        obj_to_test = EventType(1)
        assert Enum.unique(EventType, obj_to_test)
