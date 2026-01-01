from calendar import monthrange

# Font Style
ITALICS = '\x1B[3m'
BOLD = '\033[1m'
BOLDITALICS = '\x1B[1;3m'
END = '\033[0m'


# * --------- Search for Events ---------------------------------------------------------------------------------------
def search(controller):
    print('=== Αναζήτηση γεγονότων ====')

    # Input year
    year = int(input(f'Εισάγετε έτος: {BOLD}'))

    # Check validity
    # while not year > 2022:
    #     print(f'{END}Ουπς, {BOLDITALICS}λάθος έτος{END}, ξαναπροσπαθήστε!')
    #     year = int(input(f'{END}Εισάγετε έτος: {BOLD}'))

    # Input month
    month = int(input(f'{END}Εισάγετε μήνα: {BOLD}'))

    # Check validity
    while (month not in range(1, 13)):
        print(f'{END}Ουπς, {BOLDITALICS}λάθος μήνας{END}, ξαναπροσπαθήστε!')
        month = int(input(f'{END}Εισάγετε μήνα: {BOLD}'))
    print(END, end="")

    # Get events in given month list
    events_in_selected_month:list = controller.eventsInMonth(year, month)

    if len(events_in_selected_month) == 0:
        print(f"{ITALICS}Δεν βρέθηκαν γεγονότα{END}")
        return []

    for index in range(len(events_in_selected_month)):
        print(f'{index}. {events_in_selected_month[index].text_format()}')

    return events_in_selected_month


# * --------- Input Date ----------------------------------------------------------------------------------------------
def input_date(value=None):
    if value != None:
        message = f'Ημερομηνία γεγονότος ({value}): {BOLD}'
    else: 
        message = f'Ημερομηνία γεγονότος: {BOLD}'
        
    # Input date
    date = input(message)

    # Check date validity
    if value != None and date == "":
        date = value
        is_valid = True

    elif date.count('-') == 2:
        ls = date.strip().split('-')
        year = int(ls[0])
        month = int(ls[1])
        day = int(ls[2])
            
        is_valid = year > 2022 and month in range(1, 13) and day in range(1, monthrange(year, month)[1] +1)

    else:
        is_valid = False

    while not is_valid:
        print(f'{END}Ουπς, {BOLDITALICS}λάθος ημερομηνία{END}, ξαναπροσπαθήστε!')
        date = input(f'{END}Ημερομηνία γεγονότος: {BOLD}')
        
        if value != None and date == "":
            date = value
            is_valid = True
            break
        
        elif date.count('-') == 2:
            ls = date.strip().split('-')
            year = int(ls[0])
            month = int(ls[1])
            day = int(ls[2])
                
            is_valid = year > 2022 and month in range(1, 13) and day in range(1, monthrange(year, month)[1] +1)

        else:
            is_valid = False
    print(END, end="")

    return date


# * --------- Input Time ----------------------------------------------------------------------------------------------
def input_time(value=None):
    if value != None:
        message = f'Ώρα γεγονότος ({value}): {BOLD}'
    else: 
        message = f'Ώρα γεγονότος: {BOLD}'
        
    # Input time
    time = input(message)

    # Check time validity
    if value != None and time == "":
        time = value
        is_valid = True

    elif time.count(':') == 1:
        ls = time.strip().split(':')
        hour = int(ls[0])
        minute = int(ls[1])
            
        is_valid = hour in range(0, 24) and minute in range(0, 60)

    else:
        is_valid = False

    while not is_valid:
        print(f'{END}Ουπς, {BOLDITALICS}λάθος ώρα{END}, ξαναπροσπαθήστε!')
        time = input(f'{END}{message}')

        if value != None and time == "":
            time = value
            is_valid = True
            break

        elif time.count(':') == 1:
            ls = time.strip().split(':')
            hour = int(ls[0])
            minute = int(ls[1])
                
            is_valid = hour in range(0, 24) and minute in range(0, 60)

        else:
            is_valid = False
    print(END, end="")

    return time


# * --------- Input Duration ------------------------------------------------------------------------------------------
def input_duration(value=None):
    if value != None:
        message = f'Διάρκεια γεγονότος ({value}): {BOLD}'
    else: 
        message = f'Διάρκεια γεγονότος: {BOLD}'
        
    # Input duration
    duration = input(message)

    if value != None and duration == "":
        duration = value

    while not int(duration) >= 0: 
        print(f'{END}Ουπς, {BOLDITALICS}λάθος διάρκεια{END}, ξαναπροσπαθήστε!')
        duration = int(input(f'{END}{message}'))

        if value != None and duration == "":
            duration = value
            break

    print(END, end="")

    return int(duration)


# * --------- Input Title ---------------------------------------------------------------------------------------------
def input_title(value=None):
    if value == None:
        message = f'Τίτλος γεγονότος: {BOLD}'
    else: 
        message = f'Τίτλος γεγονότος ({value}): {BOLD}'
        
    # Input title
    title = input(message)

    if value != None and title == "":
        title = value

    while not title.count(',') == 0: 
        print(f'{END}Ουπς, {BOLDITALICS}λάθος τίτλος{END}, ξαναπροσπαθήστε!')
        title = input(f'{END}{message}')

        if value != None and title == "":
            title = value
            break

    print(END, end="")

    return title