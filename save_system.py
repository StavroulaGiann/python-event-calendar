"""
This program is responsible for saving & loading
the events_list from a .csv file.
"""
from os.path import exists


class SaveSystem:
    def __init__(self, file) -> None:
        self.file = file

    # Write lines to file
    def save(self, lines):
        """
        >>> saveSystem = SaveSystem('events_test.csv')
        >>> lines = [str('2022-11-4,13:30,60,Python course'), str('2022-11-28,12:0,60,Event 3'), str('2022-11-29,9:30,15,Coffee Break'), str('2022-12-5,13:45,90,Event 2'), str('2022-12-25,12:0,60,Christmas')]
        >>> saveSystem.save(lines)
        >>> saveSystem.load()
        [['2022-11-4', '13:30', '60', 'Python course'], ['2022-11-28', '12:0', '60', 'Event 3'], ['2022-11-29', '9:30', '15', 'Coffee Break'], ['2022-12-5', '13:45', '90', 'Event 2'], ['2022-12-25', '12:0', '60', 'Christmas']]
        """

        for index in range(len(lines)-1):
            lines[index] += "\n"

        # Insert at the top the .csv headers
        lines.insert(0, "Date,Hour,Duration,Title\n")

        with open(self.file, 'w') as file:
            file.writelines(lines)

    # Load data from file and format them to line -> columns
    def load(self):
        """
        >>> saveSystem = SaveSystem("events_test.csv")
        >>> saveSystem.load()
        []
        >>> lines = [str('2022-11-4,13:30,60,Python course'), str('2022-11-28,12:0,60,Event 3'), str('2022-11-29,9:30,15,Coffee Break'), str('2022-12-5,13:45,90,Event 2'), str('2022-12-25,12:0,60,Christmas')]
        >>> saveSystem.save(lines)
        >>> saveSystem.load()
        [['2022-11-4', '13:30', '60', 'Python course'], ['2022-11-28', '12:0', '60', 'Event 3'], ['2022-11-29', '9:30', '15', 'Coffee Break'], ['2022-12-5', '13:45', '90', 'Event 2'], ['2022-12-25', '12:0', '60', 'Christmas']]
        """

        if exists(self.file) == False:
            return []

        with open(self.file, 'r') as file:
            lines = file.readlines()

        rows = []
        for line in lines:
            line.strip()
            row_data = line.split(",")
            row = [row_data[0].strip(), row_data[1].strip(),
                   row_data[2].strip(), row_data[3].strip()]
            rows.append(row)

        return rows[1:]
