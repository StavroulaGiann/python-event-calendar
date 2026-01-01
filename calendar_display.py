"""
This class creates a calendar display
containg the events for the selected month
and print it
"""
import calendar


class CalendarDisplay:
    def __init__(self, firstWeekDay=0) -> None:
        self.firstWeekDay = firstWeekDay
        self.calendar = calendar
        self.calendar.setfirstweekday(self.firstWeekDay)


    # * --- Calendar Settings -------------------------------------------
    def setFirstWeekDay(self, day):
        """
        >>> calDisplay = CalendarDisplay()
        >>> calDisplay.firstWeekDay
        0
        >>> calDisplay.setFirstWeekDay(4)
        >>> calDisplay.firstWeekDay
        4
        """

        self.firstWeekDay = day
        self.calendar.setfirstweekday(self.firstWeekDay)


    # * --- Generate Calendar Headers -----------------------------------
    def get_month_header(self, year, month):
        """
        >>> calDisplay = CalendarDisplay()
        >>> print(calDisplay.get_month_header(2022, 6))
        ΙΟΥΝ 2022
        >>> print(calDisplay.get_month_header(2023, 2))
        ΦΕΒ 2023
        """

        names = {1: "ΙΑΝ", 2: "ΦΕΒ", 3: "ΜΑΡ", 4: "ΑΠΡ", 5: "ΜΑΙ", 6: "ΙΟΥΝ",
                 7: "ΙΟΥΛ", 8: "ΑΥΓ", 9: "ΣΕΠ", 10: "ΟΚΤ", 11: "ΝΟΕ", 12: "ΔΕΚ"}

        month_name = names[month]

        return f"{month_name} {year}"

    def get_weekday_header(self):
        """
        >>> calDisplay = CalendarDisplay()
        >>> print(calDisplay.get_weekday_header())
           ΔΕΥ |    ΤΡΙ |    ΤΕΤ |    ΠΕΜ |    ΠΑΡ |    ΣΑΒ |    ΚΥΡ
        
        >>> calDisplay.setFirstWeekDay(6)
        >>> print(calDisplay.get_weekday_header())
           ΚΥΡ |    ΔΕΥ |    ΤΡΙ |    ΤΕΤ |    ΠΕΜ |    ΠΑΡ |    ΣΑΒ
        """

        day_names = ["ΔΕΥ", "ΤΡΙ", "ΤΕΤ", "ΠΕΜ", "ΠΑΡ", "ΣΑΒ", "ΚΥΡ"]

        def h(index):
            offset = index + self.firstWeekDay
            if offset > 6:
                offset = offset - 7
            return day_names[offset]

        return f"   {h(0)} |    {h(1)} |    {h(2)} |    {h(3)} |    {h(4)} |    {h(5)} |    {h(6)}"


    # * --- Generate Month Days -----------------------------------------
    # Create list with the week and days of the current month
    # and the days of the month that contain an event
    def get_currentMonth(self, year, month, event_days):
        """
        >>> calDisplay = CalendarDisplay()
        >>> calDisplay.get_month_header(2022, 11)
        'ΝΟΕ 2022'
        >>> calDisplay.firstWeekDay
        0
        >>> calDisplay.get_currentMonth(2022, 11, [4, 17, 21])
        [[0, 1, 2, 3, -4, 5, 6], [7, 8, 9, 10, 11, 12, 13], [14, 15, 16, -17, 18, 19, 20], [-21, 22, 23, 24, 25, 26, 27], [28, 29, 30, 0, 0, 0, 0]]
        
        >>> calDisplay.get_currentMonth(2023, 1, [32])
        [[0, 0, 0, 0, 0, 0, 1], [2, 3, 4, 5, 6, 7, 8], [9, 10, 11, 12, 13, 14, 15], [16, 17, 18, 19, 20, 21, 22], [23, 24, 25, 26, 27, 28, 29], [30, 31, 0, 0, 0, 0, 0]]
        """

        month_list = self.calendar.monthcalendar(year, month)

        new_month = []
        for week in month_list:
            new_week = []
            for day in week:
                if day in event_days:
                    day = day * -1
                new_week.append(day)
            new_month.append(new_week)

        return new_month

    def get_previous(self, year, month):
        """
        >>> calDisplay = CalendarDisplay()
        >>> calDisplay.get_previous(2022, 11)
        (2022, 10)
        >>> calDisplay.get_previous(2023, 1)
        (2022, 12)
        >>> type(calDisplay.get_previous(2023, 1)) == tuple
        True
        >>> previous_year, previous_month = calDisplay.get_previous(2023, 1)
        >>> type(previous_year) == int and type(previous_month) == int
        True
        """
        
        if month == 1:
            month = 12
            year = year - 1
        else:
            month = month - 1

        return year, month

    # Create list with the last week days of the previous month
    def get_previousMonthWeek(self,  current_year, current_month, week):
        """
        >>> calDisplay = CalendarDisplay()
        >>> year, month = 2023, 1
        >>> month_list = calDisplay.get_currentMonth(year, month, [3, 7, 12, 15, 23, 29])
        >>> calDisplay.get_previousMonthWeek(year, month, month_list[0])   
        ['.26', '.27', '.28', '.29', '.30', '.31', 1]

        >>> year, month = 2023, 3
        >>> month_list = calDisplay.get_currentMonth(year, month, [9, 13, 14, 15, 21, 24])
        >>> calDisplay.get_previousMonthWeek(year, month, month_list[0])
        ['.27', '.28', 1, 2, 3, 4, 5]
        """

        year, month = self.get_previous(current_year, current_month)
        month_range = self.calendar.monthrange(year, month)

        duration = month_range[1]
        count = week.count(0)

        new_week = []
        day = duration - count + 1
        for weekDay in week:
            if weekDay == 0:
                new_week.append(f".{day}")
                day += 1
            else:
                new_week.append(weekDay)

        return new_week

    def get_next(self, year, month):
        """
        >>> calDisplay = CalendarDisplay()
        >>> calDisplay.get_next(2022, 11)
        (2022, 12)
        >>> calDisplay.get_next(2022, 12)
        (2023, 1)
        >>> type(calDisplay.get_next(2023, 1)) == tuple
        True
        >>> next_year, next_month = calDisplay.get_next(2023, 1)
        >>> type(next_year) == int and type(next_month) == int
        True
        """

        if month == 12:
            month = 1
            year = year + 1
        else:
            month = month + 1

        return year, month

    # Create list with the first week days of the next month
    def get_nextMonthWeek(self, week):
        """
        >>> calDisplay = CalendarDisplay()
        >>> year, month = 2022, 12
        >>> month_list = calDisplay.get_currentMonth(year, month, [3, 7, 12, 15, 23, 29])
        >>> calDisplay.get_nextMonthWeek(month_list[-1])   
        [26, 27, 28, -29, 30, 31, '.1']

        >>> year, month = 2023, 2
        >>> month_list = calDisplay.get_currentMonth(year, month, [28])
        >>> calDisplay.get_nextMonthWeek(month_list[-1])
        [27, -28, '.1', '.2', '.3', '.4', '.5']
        """

        new_week = []
        day = 1
        for weekDay in week:
            if weekDay == 0:
                new_week.append(f".{day}")
                day += 1
            else:
                new_week.append(weekDay)

        return new_week

    # Merge the current month with the last week from the previous month
    # and the first week of the next month. We do that so that the calendar
    # always starts on the first day of the week and ends on the last, even though
    # the month itself might start and end in the middles of the weeks.
    def mergeMonth(self, year, month, event_days):
        """
        >>> calDisplay = CalendarDisplay()
        >>> calDisplay.mergeMonth(2022, 11, [4, 17, 21])
        [['.31', 1, 2, 3, -4, 5, 6], [7, 8, 9, 10, 11, 12, 13], [14, 15, 16, -17, 18, 19, 20], [-21, 22, 23, 24, 25, 26, 27], [28, 29, 30, '.1', '.2', '.3', '.4']]

        >>> calDisplay.mergeMonth(2023, 2, [2, 13, 31])
        [['.30', '.31', 1, -2, 3, 4, 5], [6, 7, 8, 9, 10, 11, 12], [-13, 14, 15, 16, 17, 18, 19], [20, 21, 22, 23, 24, 25, 26], [27, 28, '.1', '.2', '.3', '.4', '.5']]
        """

        month_list = self.get_currentMonth(year, month, event_days)
        first_week = self.get_previousMonthWeek(year, month, month_list[0])
        last_week = self.get_nextMonthWeek(month_list[-1])

        month_list[0] = first_week
        month_list[-1] = last_week

        return month_list


    # * --- Display Calendar --------------------------------------------
    def dayToString(self, day):
        """
        >>> calDisplay = CalendarDisplay()
        >>> calDisplay.dayToString(25)
        '[ 25]'
        >>> calDisplay.dayToString(-1)
        '[ *1]'
        >>> calDisplay.dayToString('.17')
        '  17 '
        """

        if str(day).startswith("."):
            return f" {f'{str(day)[1:]}':>3} "
        elif day < 0:
            return f"[{f'*{day * -1}':>3}]"
        else:
            return f"[{f'{day}':>3}]"

    def weekToString(self, week):
        """
        >>> calDisplay = CalendarDisplay()
        >>> calDisplay.weekToString(['.30', '.31', 1, -2, 3, 4, 5])
        '   30  |    31  |  [  1] |  [ *2] |  [  3] |  [  4] |  [  5]'
        """

        string = ""
        for index in range(len(week)):
            if index == 0:
                string += f"{self.dayToString(week[index]):>6} |"
            elif index == 6:
                string += f" {self.dayToString(week[index]):>6}"
            else:
                string += f" {self.dayToString(week[index]):>6} |"

        return string

    def show(self, year, month, event_days):
        """
        >>> calDisplay = CalendarDisplay()
        >>> calDisplay.show(2023, 1, [2, 6, 15, 17, 28])
        ____________________________________________________________
        ΙΑΝ 2023
        ____________________________________________________________
           ΔΕΥ |    ΤΡΙ |    ΤΕΤ |    ΠΕΜ |    ΠΑΡ |    ΣΑΒ |    ΚΥΡ
           26  |    27  |    28  |    29  |    30  |    31  |  [  1]
         [ *2] |  [  3] |  [  4] |  [  5] |  [ *6] |  [  7] |  [  8]
         [  9] |  [ 10] |  [ 11] |  [ 12] |  [ 13] |  [ 14] |  [*15]
         [ 16] |  [*17] |  [ 18] |  [ 19] |  [ 20] |  [ 21] |  [ 22]
         [ 23] |  [ 24] |  [ 25] |  [ 26] |  [ 27] |  [*28] |  [ 29]
         [ 30] |  [ 31] |     1  |     2  |     3  |     4  |     5 
        ____________________________________________________________
        """

        month_list = self.mergeMonth(year, month, event_days)

        print("____________________________________________________________")
        print(self.get_month_header(year, month))
        print("____________________________________________________________")
        print(self.get_weekday_header())

        for week in month_list:
            print(self.weekToString(week))

        print("____________________________________________________________")
