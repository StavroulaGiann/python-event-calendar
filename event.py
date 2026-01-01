"""
This class is a skeleton for the events
To create an event it takes as parameters:
Date, Hour, Duration, Title
"""
from datetime import datetime, timedelta


class Event:
    # The values given are supossed to be correct
    def __init__(self, date, time, duration, title) -> None:
        self.date = date
        self.time = time
        self.duration = int(duration)
        self.title = title
        self.datetime = self.to_datetime()

    # return a string that contains all the event info in a format
    # ready to be saved in a .csv file
    def save_format(self):
        """
        >>> event = Event("2023-1-23", "15:30", 120, "Εξέταση: Διακριτά Μαθηματικά") 
        >>> event.save_format().strip()
        '2023-1-23,15:30,120,Εξέταση: Διακριτά Μαθηματικά'
        """
        return f"{self.date},{self.time},{self.duration},{self.title}"

    # return a string that contains all the event info in a format
    # easy to read for the user
    def text_format(self):
        """
        >>> event = Event("2023-1-23", "15:30", 120, "Εξέταση: Διακριτά Μαθηματικά") 
        >>> event.text_format()
        '[Εξέταση: Διακριτά Μαθηματικά] -> Ημερομηνία: 2023-1-23, Ώρα: 15:30, Διάρκεια: 120'
        """

        return f"[{self.title}] -> Ημερομηνία: {self.date}, Ώρα: {self.time}, Διάρκεια: {self.duration}"

    # Create datetime from string date, time
    def to_datetime(self):
        """
        >>> from datetime import datetime
        >>> event = Event("2023-1-23", "15:30", 120, "Εξέταση: Διακριτά Μαθηματικά") 
        >>> dt = event.to_datetime()
        >>> type(dt)
        <class 'datetime.datetime'>
        >>> dt.year == 2023 and dt.month == 1 and dt.day == 23
        True
        >>> dt.hour == 15 and dt.minute == 30
        True
        """

        date_data = self.date.split("-")
        year = int(date_data[0])
        month = int(date_data[1])
        day = int(date_data[2])

        time_data = self.time.split(":")
        hour = int(time_data[0])
        minute = int(time_data[1])

        return datetime(year, month, day, hour, minute)

    # Chech if event is in given month
    def inMonth(self, year, month):
        """
        >>> event = Event("2023-1-23", "15:30", 120, "Εξέταση: Διακριτά Μαθηματικά") 
        >>> event.inMonth(2023, 1)
        True
        >>> event.inMonth(2023, 2)
        False
        """

        return (self.datetime.year == year) and (self.datetime.month == month)

    # Chech if event is in given day
    def inDay(self, datetime):
        """
        >>> from datetime import datetime
        >>> event = Event("2023-1-23", "15:30", 120, "Εξέταση: Διακριτά Μαθηματικά") 
        >>> dt = datetime(2023, 1, 23)
        >>> event.inDay(dt)
        True
        >>> dt = datetime(2023, 1, 22)
        >>> event.inDay(dt)
        False
        """

        return self.inMonth(datetime.year, datetime.month) and (self.datetime.day == datetime.day)

    # Chech if event is in given day but later than the current time
    def laterInDay(self, datetime):
        """
        >>> from datetime import datetime
        >>> event = Event("2023-1-23", "15:30", 120, "Εξέταση: Διακριτά Μαθηματικά") 
        >>> dt = datetime(2023, 1, 23, 12, 0)
        >>> event.laterInDay(dt)
        True
        >>> dt = datetime(2023, 1, 23, 16, 0)
        >>> event.laterInDay(dt)
        False
        """

        return self.inDay(datetime) and (self.datetime.hour > datetime.hour or (self.datetime.hour == datetime.hour and self.datetime.minute > datetime.minute))

    def get_total_minutes(self):
        """
        >>> event = Event("2023-1-23", "0:30", 120, "Event 1") 
        >>> event.get_total_minutes()
        30
        >>> event = Event("2023-1-23", "2:30", 120, "Event 2") 
        >>> event.get_total_minutes()
        150
        """

        delta = timedelta(hours=self.datetime.hour, minutes=self.datetime.minute)
        total_minutes = int(delta.total_seconds() // 60)

        return total_minutes

    # Calculate remaining time
    def getTimeUntil(self, hour, minute):
        """
        >>> hour_now, minute_now = 12, 37
        >>> event = Event("2023-1-23", "15:30", 120, "Εξέταση: Διακριτά Μαθηματικά") 
        >>> event.getTimeUntil(hour_now, minute_now)
        (2, 53)
        >>> event_2 = Event("2023-1-23", "18:3", 120, "Εξέταση: Διακριτά Μαθηματικά") 
        >>> event_2.getTimeUntil(hour_now, minute_now)
        (5, 26)
        >>> event_3 = Event("2023-1-23", "21:58", 120, "Εξέταση: Διακριτά Μαθηματικά") 
        >>> event_3.getTimeUntil(hour_now, minute_now)
        (9, 21)
        """

        delta_given = timedelta(hours=hour, minutes=minute)
        total_minutes_given = int(delta_given.total_seconds() // 60)

        difference = self.get_total_minutes() - total_minutes_given

        rem_hour = difference // 60
        rem_minute = difference % 60

        return rem_hour, rem_minute

    def get_end_time_total_minutes(self):
        """
        >>> event = Event("2023-1-23", "0:30", 120, "Event 1") 
        >>> event.get_end_time_total_minutes()
        150
        >>> event = Event("2023-1-23", "2:30", 120, "Event 2") 
        >>> event.get_end_time_total_minutes()
        270
        """

        return self.get_total_minutes() + self.duration

