# test roast plan

import pytest
import datetime as dt
from RoastPlan import RoastPlan
from Events import Event, EventType


class TestRoastPlan:
    def test_weight_loss_property_returns_correct_calculation(self):
        plan = RoastPlan('plan_001', 390.5, dt.datetime.now(), 'Ambex', 100, 85.55)
        plan1 = RoastPlan('plan_abcd', 390.5, dt.datetime.now(), 'Ambex', 2334, 258)
        assert plan.weight_loss == 14.45
        assert plan1.weight_loss == 11.05

    def test_weight_lost_property_is_read_only(self):
        plan = RoastPlan('plan_001', 390.5, dt.datetime.now(), 'Ambex', 100, 85)
        with pytest.raises(SyntaxError):
            plan.weight_loss = 1

    def test_weight_lost_property_returns_none_if_final_weight_is_0(self):
        plan = RoastPlan('plan_001', 390.5, dt.datetime.now(), 'Ambex', 100, 0)
        assert plan.weight_loss is None

    def test_return_event_list_returns_dict_on_success(self):
        plan = RoastPlan('plan_001', 390.5, dt.datetime.now(), 'Ambex', 100, 85)
        event = Event()
        plan.events['event_001'] = event
        assert plan.return_events_list() == {'event_001': event}

    def test_return_event_list_returns_none_on_failure(self):
        plan = RoastPlan('plan_001', 390.5, dt.datetime.now(), 'Ambex', 100, 85)
        assert plan.return_events_list() is None

    def test_return_event_returns_event_on_success(self):
        plan = RoastPlan('plan_001', 390.5, dt.datetime.now(), 'Ambex', 100, 85)
        event = Event()
        plan.events['event_001'] = event
        result = plan.return_event('event_001')
        assert isinstance(result, Event)

    def test_return_event_returns_false_on_failure(self):
        plan = RoastPlan('plan_001', 390.5, dt.datetime.now(), 'Ambex', 100, 85)
        assert plan.return_event('a') is False

    def test_add_event_updates_events_attribute(self):
        plan = RoastPlan('plan_001', 390.5, dt.datetime.now(), 'Ambex', 100, 85)
        plan.add_event('event_001', EventType(1))
        assert len(plan.events) == 1

    def test_add_event_returns_true_on_success(self):
        plan = RoastPlan('plan_001', 390.5, dt.datetime.now(), 'Ambex', 100, 85)
        assert plan.add_event('event_001', EventType(2))

    def test_add_event_returns_false_on_failure(self):
        plan = RoastPlan('plan_001', 390.5, dt.datetime.now(), 'Ambex', 100, 85)
        assert plan.add_event('event_001', EventType(10)) is False

    def test_remove_event_removes_event_from_dict(self):
        plan = RoastPlan('plan_001', 390.5, dt.datetime.now(), 'Ambex', 100, 85)
        plan.add_event('event_001', EventType(1))
        plan.add_event('even_002', EventType(2))
        plan.remove_event('event_001')
        assert len(plan.events) == 1

    def test_remove_event_returns_true_on_success(self):
        plan = RoastPlan('plan_001', 390.5, dt.datetime.now(), 'Ambex', 100, 85)
        plan.add_event('event_001', EventType(1))
        plan.add_event('even_002', EventType(2))
        assert plan.remove_event('event_001')

    def test_remove_event_returns_false_on_failure(self):
        plan = RoastPlan('plan_001', 390.5, dt.datetime.now(), 'Ambex', 100, 85)
        plan.add_event('event_001', EventType(1))
        plan.add_event('even_002', EventType(2))
        assert plan.remove_event('event_003') is False

