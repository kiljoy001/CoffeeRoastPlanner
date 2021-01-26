# RoastPlan.py

class RoastPlan:
    """
    A plan contains the time series of in order events
    during the roast with corresponding actions to add fuel
    or to open or shut air flow in the roaster. It also contains
    the target roast temperature, and id number.
    he roasting plan information is a container that holds the
    current date & time of plan creation, name of the
    roaster, green coffee weight, and the final weight
    of the roast.
    It contains a read only plan id to tie it to a plan
    It also has a weight loss calculation.

    """
    def __init__(self, plan_id, target_charge_temp, date_time, roaster_name, green_coffee_weight, final_weight=0):
        self.plan_id = plan_id
        self.charge_temp = target_charge_temp
        self.plan_date = date_time
        self.name_of_roaster = roaster_name
        self.green_coffee_weight = green_coffee_weight
        self.final_weight = final_weight
        self.events = {}

    @property
    def weight_loss(self):
        """
        The weight loss property returns the calculated
        weight loss expressed as percentile to two
        decimal points in accuracy when weighed after
        roast.
        :return: float
        """
        pass

    def return_events_list(self):
        """
        Returns full list of events as a dictionary or None

        :return: dict
        """

    def return_event(self, event_id):
        """
        searches internal database to return an event by event_id if found
        returns false if not found
        :param event_id: string
        :return: Event, bool
        """

    def add_event(self, event_id, event_type):
        """
        Adds an event to the internal events dictionary, returns True on success, False on failure
        :param event_id: string
        :param event_type: Enum
        :return: bool
        """

    def remove_event(self, event_id):
        """
        Removes an event from event list. Returns true on success, and false on failure.
        :param event_id:
        :return: bool
        """