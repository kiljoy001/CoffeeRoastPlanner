# test roast plan collection

from RoastPlanCollection import RoastPlanCollection
import datetime as dt
from RoastPlan import RoastPlan


class TestRoastPlanCollection:
    def test_roasting_plan_collection_search_returns_correct_obj(self):
        test_plan = RoastPlan('test_plan', 390, dt.datetime.now(), 'ambex', 100)
        test_collection = RoastPlanCollection()
        test_collection.database = {test_plan.plan_id: test_plan}
        obj_to_test = test_collection.search_roasting_plan('test_plan_0000')
        assert obj_to_test == test_plan

    def test_roasting_plan_collection_search_returns_false_on_failure(self):
        test_collection = RoastPlanCollection()
        assert test_collection.search_roasting_plan('test_plan_0000') is False

    def test_roasting_plan_collection_search_returns_true_on_success(self):
        test_plan = RoastPlan('test_plan', 390, dt.datetime.now(), 'ambex', 100)
        test_collection = RoastPlanCollection()
        test_collection.database = {test_plan.plan_id: test_plan}
        assert test_collection.search_roasting_plan('test_plan')

    def test_roasting_plan_change_plan_updates_plan_data(self):
        test_collection = RoastPlanCollection()
        test_collection.add_plan('plan_001', 390.0, dt.datetime.now(), 'Ambex', 20.5)
        test_collection.change_plan_data('plan_001', 390.0, dt.datetime.now(), 'probat', 13.5)
        assert list(test_collection.database.values())[0].name_of_roaster == 'probat'

    def test_roasting_plan_change_plan_returns_true_on_success(self):
        test_collection = RoastPlanCollection()
        test_collection.add_plan('plan_001', 390.0, dt.datetime.now(), 'Ambex', 20.5)
        assert test_collection.change_plan_data('plan_001', 390.0, dt.datetime.now(), 'probat', 13.5)

    def test_roasting_plan_change_plan_returns_false_on_failure(self):
        test_collection = RoastPlanCollection()
        test_collection.add_plan('plan_001', 390.0, dt.datetime.now(), 'Ambex', 20.5)
        assert test_collection.change_plan_data('plan_002', 390.0, dt.datetime.now(), 'probat', 13.5) is False

    def test_roasting_plan_add_plan_updates_collection(self):
        test_collection = RoastPlanCollection()
        test_collection.add_plan('plan_001', 390.0, dt.datetime.now(), 'Ambex', 20.5)
        assert len(test_collection.database) == 1

    def test_roasting_plan_add_plan_returns_true_on_success(self):
        test_collection = RoastPlanCollection()
        assert test_collection.add_plan('plan_001', 390.0, dt.datetime.now(), 'Ambex', 20.5)

    def test_roasting_plan_add_plan_returns_false_on_failure(self):
        test_collection = RoastPlanCollection()
        test_collection.add_plan('plan_001', 390.0, dt.datetime.now(), 'Ambex', 20.5)
        assert test_collection.add_plan('plan_001', 390.0, dt.datetime.now(), 'Ambex', 20.5) is False

    def test_roasting_plan_delete_plan_removes_plan(self):
        test_collection = RoastPlanCollection()
        test_collection.add_plan('plan_001', 390.0, dt.datetime.now(), 'Ambex', 20.5)
        test_collection.add_plan('plan_002', 390.0, dt.datetime.now(), 'Ambex', 20.5)
        test_collection.delete_plan('plan_001')
        assert len(test_collection.database) == 1

    def test_roasting_plan_delete_plan_returns_true_on_success(self):
        test_collection = RoastPlanCollection()
        test_collection.add_plan('plan_001', 390.0, dt.datetime.now(), 'Ambex', 20.5)
        assert test_collection.delete_plan('plan_001')

    def test_roasting_plan_delete_plan_returns_false_on_failure(self):
        test_collection = RoastPlanCollection()
        assert test_collection.delete_plan('plan_001')
