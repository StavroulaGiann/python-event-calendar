"""
This class is responsible for creating the events_list,
deleting events, adding events, and calls to save_system to 
save the list
"""
from datetime import datetime as _datetime


class Controller:
    def __init__(self, datetime=None) -> None:
        self.event_list = []
        if datetime != None:
            self.datetime = datetime
        else:
            self.datetime = _datetime.now()

    # Append given event to list
    # if event is new, then after adding it, sort the list
    def add(self, event):
        """
        >>> controller = Controller()
        >>> from event import Event
        >>> event = Event('2022-11-29', '9:30', 15, 'Coffee Break')
        >>> controller.add(event)
        >>> for event in controller.event_list:
        ...     print(event.save_format())
        2022-11-29,9:30,15,Coffee Break
        >>> event_2 = Event('2022-11-4', '15:20', 30, 'Lunch')
        >>> controller.add(event_2)
        >>> for event in controller.event_list:
        ...     print(event.save_format())
        2022-11-4,15:20,30,Lunch
        2022-11-29,9:30,15,Coffee Break
        """

        self.event_list.append(event)
        self.sort()

    # Remove given event from list
    def delete(self, event):
        """
        >>> controller = Controller()
        >>> from event import Event
        >>> event = Event('2022-11-29', '9:30', 15, 'Coffee Break')
        >>> controller.add(event)
        >>> event_2 = Event('2022-11-4', '15:20', 30, 'Lunch')
        >>> controller.add(event_2)
        >>> for event in controller.event_list:
        ...     print(event.save_format())
        2022-11-4,15:20,30,Lunch
        2022-11-29,9:30,15,Coffee Break
        >>> controller.delete(event_2)
        >>> for event in controller.event_list:
        ...     print(event.save_format())
        2022-11-29,9:30,15,Coffee Break
        """

        self.event_list.remove(event)

    # Sort event_list based on each event's datetime
    # This way, the events will appear in chronological order
    # to the user
    def sort(self):
        """
        >>> from event import Event
        >>> data = [Event("2023-1-11", "9:05", 20, "Event 1"), Event("2023-1-11", "11:32", 99, "Event 3"), Event("2023-1-11", "10:40", 18, "Event 2")]
        >>> controller = Controller()
        >>> for event in data:
        ...     controller.add(event)
        >>> for event in controller.event_list:
        ...     print(event.text_format())
        [Event 1] -> Ημερομηνία: 2023-1-11, Ώρα: 9:05, Διάρκεια: 20
        [Event 2] -> Ημερομηνία: 2023-1-11, Ώρα: 10:40, Διάρκεια: 18
        [Event 3] -> Ημερομηνία: 2023-1-11, Ώρα: 11:32, Διάρκεια: 99
        """

        def get_datetime(event):
            return event.datetime
        self.event_list.sort(key=get_datetime)


    # * --- Event List Getters ------------------------------------------
    # Create list of each event in controller.event_list that is scheduled for current month.
    def eventsInMonth(self, year=None, month=None):
        """
        >>> from datetime import datetime
        >>> from event import Event
        >>> data = [Event("2022-12-11", "9:05", 20, "Event 1"), Event("2023-1-11", "11:32", 99, "Event 3"), Event("2023-1-11", "10:40", 18, "Event 2")]
        >>> controller = Controller(datetime(2023,1,11))
        >>> for event in data:
        ...     controller.add(event)
        >>> for event in controller.eventsInMonth(year=2023, month=1):
        ...     print(event.text_format())
        [Event 2] -> Ημερομηνία: 2023-1-11, Ώρα: 10:40, Διάρκεια: 18
        [Event 3] -> Ημερομηνία: 2023-1-11, Ώρα: 11:32, Διάρκεια: 99
        """

        if year != None and month != None:
            return list(filter(lambda x: x.inMonth(year, month), self.event_list))
        else:
            return list(filter(lambda x: x.inMonth(self.datetime.year, self.datetime.month), self.event_list))

    # Get all the days of the events that are in selected month
    def daysContainingEvents(self):
        """
        >>> from event import Event
        >>> data = [Event("2022-12-11", "9:05", 20, "Event 1"), Event("2023-1-11", "11:32", 99, "Event 3"), Event("2023-1-23", "10:40", 18, "Event 2")]
        >>> controller = Controller()
        >>> for event in data:
        ...     controller.add(event)
        >>> controller.daysContainingEvents()
        [11, 23]
        """

        ls = []
        for event in self.eventsInMonth():
            day = event.datetime.day
            if day in ls:
                continue
            ls.append(day)

        return ls

    # Create list of each event in controller.event_list that is scheduled the given day.
    def getEventsInDay(self, datetime):
        """
        >>> from datetime import datetime
        >>> from event import Event
        >>> data = [Event("2022-12-11", "9:05", 20, "Event 1"), Event("2023-1-11", "11:32", 99, "Event 3"), Event("2023-1-23", "10:40", 18, "Event 2")]
        >>> controller = Controller()
        >>> for event in data:
        ...     controller.add(event)
        >>> for event in controller.getEventsInDay(datetime(2023, 1, 11)):
        ...     print(event.text_format())
        [Event 3] -> Ημερομηνία: 2023-1-11, Ώρα: 11:32, Διάρκεια: 99
        """

        return list(filter(lambda x: x.inDay(datetime), self.event_list))

    # Create list of each event in controller.event_list that is scheduled for later in day.
    def getEventsLaterInDay(self, datetime):
        return list(filter(lambda x: x.laterInDay(datetime), self.event_list))


    # * --- Month Operations --------------------------------------------
    def get_previous(self):
        """
        >>> from datetime import datetime
        >>> controller = Controller(datetime(2023, 1, 1))
        >>> controller.get_previous()
        (2022, 12)
        """

        if self.datetime.month == 1:
            return self.datetime.year - 1, 12
        
        return self.datetime.year, self.datetime.month - 1

    def get_next(self):
        """
        >>> from datetime import datetime
        >>> controller = Controller(datetime(2022, 12, 1))
        >>> controller.get_next()
        (2023, 1)
        """

        if self.datetime.month == 12:
            return self.datetime.year + 1, 1
        
        return self.datetime.year, self.datetime.month + 1

    def toNext(self):
        """
        >>> from datetime import datetime
        >>> controller = Controller(datetime(2022, 12, 1))
        >>> controller.toNext()
        >>> controller.datetime.year, controller.datetime.month
        (2023, 1)
        """

        year, month = self.get_next()
        self.datetime = _datetime(year, month, 1)

    def toPrevious(self):
        """
        >>> from datetime import datetime
        >>> controller = Controller(datetime(2023, 1, 1))
        >>> controller.toPrevious()
        >>> controller.datetime.year, controller.datetime.month
        (2022, 12)
        """

        year, month = self.get_previous()
        self.datetime = _datetime(year, month, 1)


    # * --- Event Operations --------------------------------------------
    # For two given events (chronological order does not matter)
    # check it there is time overlap between them
    def are_overlaping(self, previous_event, current_event):
        """
        >>> from event import Event
        >>> controller = Controller()
        >>> event_1 = Event('2023-1-23', '15:25', 15, 'Event 1')
        >>> event_2 = Event('2023-1-23', '16:00', 30, 'Event 2')
        >>> controller.are_overlaping(event_1, event_2)
        False
        >>> event_1 = Event('2023-1-23', '16:00', 15, 'Event 1')
        >>> event_2 = Event('2023-1-23', '15:25', 30, 'Event 2')
        >>> controller.are_overlaping(event_1, event_2)
        False
        >>> controller = Controller()
        >>> event_1 = Event('2023-1-23', '15:25', 60, 'Event 1')
        >>> event_2 = Event('2023-1-23', '16:00', 30, 'Event 2')
        >>> controller.are_overlaping(event_1, event_2)
        True
        >>> event_1 = Event('2023-1-23', '16:00', 15, 'Event 1')
        >>> event_2 = Event('2023-1-23', '15:25', 60, 'Event 2')
        >>> controller.are_overlaping(event_1, event_2)
        True
        """

        if previous_event.datetime > current_event.datetime:
            prev_end = current_event.get_end_time_total_minutes()
            curr_start = previous_event.get_total_minutes()

        else:
            prev_end = previous_event.get_end_time_total_minutes()
            curr_start = current_event.get_total_minutes()

        return curr_start - prev_end < 0

    # For a given event, checks if there is time overlap between
    # all the other events in a day
    # If there is, return True, else False
    def overlaps(self, event):
        """
        >>> from datetime import datetime
        >>> from event import Event
        >>> data = [Event("2023-1-11", "9:05", 20, "Event 1"), Event("2023-1-11", "11:32", 99, "Event 3"), Event("2023-1-23", "10:40", 18, "Event 2")]
        >>> controller = Controller()
        >>> for event in data:
        ...     controller.add(event)
        >>> new_event = Event("2023-1-11", "11:00", 10, "Event 4")
        >>> controller.overlaps(new_event)
        False
        >>> new_event = Event("2023-1-11", "11:30", 60, "Event 4")
        >>> controller.overlaps(new_event)
        True
        >>> new_event = Event("2023-1-11", "12:00", 20, "Event 4")
        >>> controller.overlaps(new_event)
        True
        >>> new_event = Event("2023-1-11", "14:00", 20, "Event 4")
        >>> controller.overlaps(new_event)
        False
        """

        is_overlaping = False
        for other in self.getEventsInDay(event.datetime):
            if other.save_format() == event.save_format():
                continue

            res = self.are_overlaping(other, event)

            if res:
                is_overlaping = True
                break

        return is_overlaping

    # Print all the availabe time slots between events 
    def print_time_table(self, datetime):
        """
        >>> from datetime import datetime
        >>> from event import Event
        >>> data = [Event("2023-1-11", "9:05", 20, "Event 1"), Event("2023-1-11", "11:32", 99, "Event 3"), Event("2023-1-23", "10:40", 18, "Event 2")]
        >>> controller = Controller()
        >>> for event in data:
        ...     controller.add(event)
        >>> controller.print_time_table(datetime(2023, 1, 11))
        00:00 -  9:05
         9:25 - 11:32
        13:11 - 23:59
        """

        events = self.getEventsInDay(datetime)
        
        # Print first's event start time
        prev_start = events[0].time
        if prev_start >= '00:00':
            print(f'00:00 - {prev_start:>5}')

        # For every other event in the day
        # print the time slots that there are not
        # any events
        for index in range(1, len(events)):
            total_prev_end = events[index-1].get_end_time_total_minutes()
            total_curr_start = events[index].get_total_minutes()

            if not total_curr_start > total_prev_end:
                continue

            prev_end_hour = total_prev_end // 60
            prev_end_minute = total_prev_end % 60

            curr_start_hour = total_curr_start // 60
            curr_start_minute = total_curr_start % 60

            if prev_end_minute < 10:
                prev_end = f'{prev_end_hour}:0{prev_end_minute}'
            else:
                prev_end = f'{prev_end_hour}:{prev_end_minute}'

            if curr_start_minute < 10:
                curr_start = f'{curr_start_hour}:0{curr_start_minute}'
            else:
                curr_start = f'{curr_start_hour}:{curr_start_minute}'

            print(f'{prev_end:>5} - {curr_start:>5}')           

        # Print final event's end time
        total_curr_end = events[len(events)-1].get_end_time_total_minutes()
        curr_end_hour = total_curr_end // 60
        curr_end_minute = total_curr_end % 60

        if curr_end_minute < 10:
            curr_end = f'{curr_end_hour}:0{curr_end_minute}'
        else:
            curr_end = f'{curr_end_hour}:{curr_end_minute}'

        if curr_end <= '23:59':
            print(f'{curr_end:>5} - 23:59') 
            