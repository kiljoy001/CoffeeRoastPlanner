# RoastPlanCollection.py

class RoastPlanCollection:
    """
    The RoastPlanCollection is a collection of
    roasting plans. You can change, add, read,
    or delete a roasting plan in the collection
    It stores the plans in a dictionary with the plan_id
    and plan object as a value
    """
    def __init__(self):
        self.database = {}

    def search_roasting_plan(self, plan_id):
        """
        this method searches for a plan by it's id
        and returns the plan if found. Otherwise it
        returns false
        :return: plan, bool
        """
        pass

    def change_plan_data(self, plan_id, target_charge_temp, date_time, roaster_name, green_coffee_weight):
        """
        Updates plan data. Returns true on success,
        returns false on failure
        :return: tuple
        """
        pass

    def delete_plan(self, plan_id):
        """
        Removes plan and returns true on success, returns false on failure
        :return: bool
        """
        pass

    def add_plan(self, plan_id, target_charge_temp, date_time, roaster_name, green_coffee_weight):
        """
        Add plan to the collection. Returns true on success, false on failure
        :param green_coffee_weight: float
        :param roaster_name: string
        :param date_time: datetime
        :param target_charge_temp: float
        :param plan_id: string
        :return: bool
        """
        pass
