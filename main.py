from datetime import datetime
from save_system import SaveSystem
from controller import Controller
from calendar_display import CalendarDisplay
from event import Event
from event_inputs import search, input_date, input_time, input_duration, input_title


# * --- Instatiations ----------------------------------------------
# Instatiate Save System
saveSystem = SaveSystem("events.csv")

# Instatiate Controller
controller = Controller()

# Instatiate Calendar Display
calDisplay = CalendarDisplay()


# * --- Initializations --------------------------------------------
# Load data list from saveSystem
data = saveSystem.load()

# Iterate through the data list
for event_data in data:
    new_event = Event(event_data[0], event_data[1], event_data[2], event_data[3])
    controller.add(new_event)


# * --- Show Events Scheduled for Later in Same Day (Bonus 2) -------
datetime_now = datetime.now()

events_later_in_day_list = controller.getEventsLaterInDay(datetime_now)

if len(events_later_in_day_list) > 0:
    for event in events_later_in_day_list:
        rem_hour, rem_minute = event.getTimeUntil(
            controller.datetime.hour, controller.datetime.minute)
        print(f"Ειδοποίηση: σε {rem_hour} ώρες και {rem_minute} λεπτά από τώρα έχει προγραμματιστεί το γεγονός «{event.text_format()}»")
elif len(controller.getEventsInDay(datetime_now)) > 0:
    print("Δέν υπάρχουν άλλα γεγονότα προγραμματισμένα για σήμερα")
else:
    print("Δέν υπάρχουν γεγονότα προγραμματισμένα για σήμερα")


# * --- Main Loop Setup --------------------------------------------
# Variables
action = ""
possible_actions = ["q", "", "-", "+", "*", "0", "1", "2", "3"]

# Font Style
ITALICS = '\x1B[3m'
BOLD = '\033[1m'
BOLDITALICS = '\x1B[1;3m'
END = '\033[0m'


# * --- Main Loop ---------------------------------------------------
while action != "q":
    # Show Calendar of Current Month
    calDisplay.show(year=controller.datetime.year, month=controller.datetime.month,
                    event_days=controller.daysContainingEvents())

    # * --- Menu ----------------------------------------------------
    print(f'Πατήστε {BOLD}ENTER{END} για προβολή του επόμενου μήνα, {BOLD}"q"{END} για έξοδο ή κάποια από τις παρακάτω επιλογές:')

    print(f'    {BOLD}"-"{END} για πλοήγηση στον προηγούμενο μήνα')
    print(f'    {BOLD}"+"{END} για διαχείριση των γεγονότων του ημερολογίου')
    print(f'    {BOLD}"*"{END} για εμφάνιση των γεγονότων ενός επιλεγμένου μήνα')

    action = input("    -> ")
    if action not in possible_actions:
        print(f'{ITALICS}Η ενέργεια δεν αναγνωρίστηκε{END}')
        continue


    # * --- Main Actions --------------------------------------------
    # Move to next month
    if action == "":
        controller.toNext()

    # Move to previous month
    elif action == "-":
        controller.toPrevious()

    # Show events for selected month
    elif action == "*":
        # Search for events in year, month and get a list of them
        events_in_selected_month = search(controller)

        if len(events_in_selected_month) == 0:
            continue

        input("Πατήστε οποιοδήποτε χαρακτήρα για επιστροφή στο κυρίως μενού: ")


    # * --- Secondary Actions ---------------------------------------
    # Show secondary menu
    elif action == "+":
        while action != "0":
            print(f'{BOLD}Διαχείριση γεγονότων ημερολογίου{END}, επιλέξτε ενέργεια:')
            print('    1 Καταγραφή νέου γεγονότος')
            print('    2 Διαγραφή γεγονότος')
            print('    3 Ενημέρωση γεγονότος')
            print('    0 Επιστροφή στο κυρίως μενού')

            action = input("    -> ")
            if action not in possible_actions:
                print(f'{ITALICS}Η ενέργεια δεν αναγνωρίστηκε{END}')
                continue
            
            
            # * --- Create New Event ----------------------------------------
            if action == "1":
                # Inputs
                date = input_date()
                time = input_time()
                duration = input_duration()
                title = input_title()

                # Create new event based on user's inputs
                new_event = Event(date, time, duration, title)                   
                

                # * --- Check Time Overlap (Bonus 1) -------------------------------
                while controller.overlaps(new_event):
                    print(f"\nΟυπς, φαίνεται πως {BOLDITALICS}υπάρχει χρονική επικάλυψη{END} με άλλα γεγονότα της ημέρας")
                    print(f'Παρακαλώ, {BOLD}εισάγεται διαφορετική ημερομηνία ή ώρα{END}.')
                    print(f'\n{BOLD}Διαθέσιμα κενά{END} που υπάρχουν μεταξύ άλλων γεγονότων:')
                    controller.print_time_table(new_event.datetime)
                    print("")

                    # Repeat inputs
                    date = input_date(new_event.date)
                    time = input_time(new_event.time)

                    # Create new event
                    new_event = Event(date, time, duration, title)

                # Add new event
                controller.add(new_event) 
                print(f"Το γεγονός δημιουργήθηκε: «{new_event.text_format()}»\n")



            # * --- Delete Existing Event -----------------------------------
            elif action == "2":
                # Search for events in year, month and get a list of them
                events_in_selected_month = search(controller)

                if len(events_in_selected_month) == 0:
                    print("")
                    continue
                
                # Input event's index for deletion 
                index_to_delete = int(input(f"Επιλέξτε γεγονός προς διαγραφή: {BOLD}"))

                # Check validity
                while index_to_delete not in range(0, len(events_in_selected_month)):
                    print(f'{END}Ουπς, {BOLDITALICS}λάθος αριθμός{END}, ξαναπροσπαθήστε!')
                    index_to_delete = int(input(f"Επιλέξτε γεγονός προς διαγραφή: {BOLD}"))
                print(END, end="")

                # Delete event
                event_for_deletion = events_in_selected_month[index_to_delete]
                controller.delete(event_for_deletion)
                print(f"Το γεγονός διαγράφθηκε: «{event_for_deletion.text_format()}»\n")


            # * --- Edit Existing Event -------------------------------------
            elif action == "3":
                events_in_selected_month = search(controller)

                if len(events_in_selected_month) == 0:
                    print("")
                    continue

                # Input event's index for deletion 
                index_to_edit = int(input(f"Επιλέξτε γεγονός προς επεξεργασία: {BOLD}"))

                # Check validity
                while index_to_edit not in range(0, len(events_in_selected_month)):
                    print(f'{END}Ουπς, {BOLDITALICS}λάθος αριθμός{END}, ξαναπροσπαθήστε!')
                    index_to_edit = int(input(f"Επιλέξτε γεγονός προς επεξεργασία: {BOLD}"))
                print(END, end="")

                old_event = events_in_selected_month[index_to_edit]

                # Inputs
                date = input_date(old_event.date)
                time = input_time(old_event.time)
                duration = input_duration(old_event.duration)
                title = input_title(old_event.title)
                
                # Create new event based on user's inputs
                new_event = Event(date, time, duration, title)

                print(old_event.save_format())
                print(new_event.save_format())

                # Check if edits were made
                if new_event.save_format() == old_event.save_format():
                    print(f"Δεν πραγματοποιήθηκε καμία αλλαγή στο γεγονός: «{new_event.text_format()}»\n")
                    continue
                    
                # Delete old event
                controller.delete(old_event)


                # * --- Check Time Overlap (Bonus 1) -------------------------------
                # Check for time overlap
                while controller.overlaps(new_event):
                    print(f"\nΟυπς, φαίνεται πως {BOLDITALICS}υπάρχει χρονική επικάλυψη{END} με άλλα γεγονότα της ημέρας")
                    print(f'Παρακαλώ, {BOLD}εισάγεται διαφορετική ημερομηνία ή ώρα{END}.')
                    print(f'\n{BOLD}Διαθέσιμα κενά{END} που υπάρχουν μεταξύ άλλων γεγονότων:')
                    controller.print_time_table(new_event.datetime)
                    print("")

                    # Repeat inputs
                    date = input_date(new_event.date)
                    time = input_time(new_event.time)

                    # Create new event
                    new_event = Event(date, time, duration, title)

                # Add new event
                controller.add(new_event) 
                print(f"Το γεγονός ενημερώθηκε: «{new_event.text_format()}»\n")

                
else:
# * --- Save Data On Exit ------------------------------------------
    # Export all event data for controller.event_list
    # to a string list
    string_data = []
    for event in controller.event_list:
        string_data.append(event.save_format())

    # Save string data
    saveSystem.save(string_data)
