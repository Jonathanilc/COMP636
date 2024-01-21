# ============== Selwyn Panel Beaters MAIN PROGRAM ==============
# Student Name: Jonathan Xu
# Student ID : 1159350
# NOTE: Make sure your two files are in the same folder
# =================================================================================

import spb_data    # spb_data.py MUST be in the SAME FOLDER as this file!
                    # spb_data.py contains the data
import datetime     # We areusing date times for this assessment, and it is
                    # available in the column_output() fn, so do not delete this line

# Data variables
#col variables contain the format of each data column and help display headings
#db variables contain the actual data
col_customers = spb_data.col_customers
db_customers = spb_data.db_customers
col_services = spb_data.col_services
db_services = spb_data.db_services
col_parts = spb_data.col_parts
db_parts = spb_data.db_parts
#col_bills is useful for displaying the headings when listing bills
col_bills = spb_data.col_bills

# =================================================================================
# Utility Functions

# this function would not allow empty input
def no_empty_input(question):
    response = input(question)
    while not response:
        response = input("Value can not be empty, please enter again: ")
    return response

# this function will validate if given digit id exist in db
def validate_db_input(db, question):
    response = input(question)
    while not response.isdigit():
        response = input("Please enter number only: ")
    while int(response) not in db.keys():
        response = input("No record found, please enter again: ")
    
    return int(response)

# this function will handle multiple add and return a tuple without duplication values
def recursively_add(db, question):
    has_more_to_add = input("Press enter to add record, or type 'No' to finish: ")
    list = []
    
    while has_more_to_add != "No":
        list.append(validate_db_input(db=db, question=question))
        has_more_to_add = input("Press enter to add more value, or enter No to finish: ")
    
    return tuple(set(list))

# this function will only allow digital input
def digit_input(question):
    response = input(question)
    while not response.isdigit():
        response = input("Value need to be digit, please enter again: ")
    return int(response)

# =================================================================================

def next_id(db_data):
    #Pass in the dictionary that you want to return a new ID number for, this will return a new integer value
    # that is one higher than the current maximum in the list.
    return max(db_data.keys())+1

def column_output(db_data, cols, format_str):
    # db_data is a list of tuples.
    # cols is a dictionary with column name as the key and data type as the item.
    # format_str uses the following format, with one set of curly braces {} for each column:
    #   eg, "{: <10}" determines the width of each column, padded with spaces (10 spaces in this example)
    #   <, ^ and > determine the alignment of the text: < (left aligned), ^ (centre aligned), > (right aligned)
    #   The following example is for 3 columns of output: left-aligned 5 characters wide; centred 10 characters; right-aligned 15 characters:
    #       format_str = "{: <5}  {: ^10}  {: >15}"
    #   Make sure the column is wider than the heading text and the widest entry in that column,
    #       otherwise the columns won't align correctly.
    # You can also pad with something other than a space and put characters between the columns, 
    # eg, this pads with full stops '.' and separates the columns with the pipe character '|' :
    #       format_str = "{:.<5} | {:.^10} | {:.>15}"
    print(format_str.format(*cols))
    for row in db_data:
        row_list = list(row)
        for index, item in enumerate(row_list):
            if item is None:      # Removes any None values from the row_list, which would cause the print(*row_list) to fail
                row_list[index] = ""       # Replaces them with an empty string
            elif isinstance(item, datetime.date):    # If item is a date, convert to a string to avoid formatting issues
                row_list[index] = str(item)
        print(format_str.format(*row_list))

def list_customers(no_prompt = False):
    # List the ID, name, telephone number, and email of all customers

    # Use col_Customers for display
    print(db_customers)
    # Convert the dictionary data into a list that displays the required data fields
    #initialise an empty list which will be used to pass data for display
    display_list = []
    #Iterate over all the customers in the dictionary
    for customer in db_customers.keys():
        #append to the display list the ID, Name, Telephone and Email
        display_list.append((customer,
                             db_customers[customer]['details'][0],
                             db_customers[customer]['details'][1],
                             db_customers[customer]['details'][2]))
    format_columns = "{: >4} | {: <15} | {: <12} | {: ^12}"
    print("\nCustomer LIST\n")    # display a heading for the output
    column_output(display_list, col_customers, format_columns)   # An example of how to call column_output function

    if not no_prompt:
        input("\nPress Enter to continue.")     # Pauses the code to allow the user to see the output

def list_parts(no_prompt = False):
    # List the ID, name, cost of all parts
    display_list = []
    
    for part_id in db_parts.keys():
        display_list.append((part_id,
                             db_parts[part_id][0],
                             db_parts[part_id][1]))
        
    display_list.sort(key=lambda x: x[1]) # this will sort based on the second value of the list which is name
    format_columns = "{: >4} | {: <10} | {: <12}"
    print("\nPart LIST\n")
    column_output(display_list, col_parts, format_columns)

    if not no_prompt:
        input("\nPress Enter to continue.")     # Pauses the code to allow the user to see the output

def list_services(no_prompt = False):
    # List the ID, name, cost of all services
    display_list = []
    
    for service_id in db_services.keys():
        #append to the display list the ID, Name, Telephone and Email
        display_list.append((service_id,
                             db_services[service_id][0],
                             db_services[service_id][1]))
        
    display_list.sort(key=lambda x: x[1]) # this will sort based on the second value of the list which is name
    format_columns = "{: >4} | {: <20} | {: <12}"
    print("\nService LIST\n")
    column_output(display_list, col_services, format_columns)
    
    if not no_prompt:
        input("\nPress Enter to continue.")     # Pauses the code to allow the user to see the output

def add_customer():
    # Add a customer to the db_customers database, use the next_id to get an id for the customer.
    # Remember to add all required dictionaries.

    # auto generate id
    id = next_id(db_customers)

    # manually enter data
    name = no_empty_input("Please enter customer name: ")
    phone_num = no_empty_input("Please enter customer phone number: ")
    email = no_empty_input("Please enter customer email address: ")

    # saving to db
    db_customers[id] = {"details": [name, phone_num, email], "jobs": {}}

    input("\nPress Enter to continue.")

def add_job():
    # Add a Job to a customer
    # Remember to validate part and service ids
    amount = 0
    # show customers but without prompt
    list_customers(no_prompt = True)
    customer_id = validate_db_input(db=db_customers, question= "Please enter customer id: ")
    
    # show parts but without prompt
    list_parts(no_prompt = True)
    part_ids = recursively_add(db=db_parts, question= "Please enter part id: ")
    
    # show services but without prompt
    list_services(no_prompt = True)
    service_ids = recursively_add(db=db_services, question= "Please enter service id: ")

    # calculate amount
    for id in part_ids:
        amount += db_parts[id][1]
    for id in service_ids:
        amount += db_services[id][1]
    timeNow = datetime.date.today()

    # saving to db
    db_customers[customer_id]["jobs"][timeNow] = [service_ids, part_ids, round(amount, 2), False]
    input("\nPress Enter to continue.")

def bills_to_pay(customer=None, no_prompt=False):
    display_list = []

    # condition based on if customer being passed
    if customer: 
        jobs = db_customers[customer]["jobs"]
        for job_id in jobs.keys():
            if jobs[job_id][3] == False: # only show when the job haven't been paid
                display_list.append((db_customers[customer]["details"][0], # customer name
                                    db_customers[customer]["details"][1], # customer phone number
                                    job_id, # which is the date when the job has been created
                                    jobs[job_id][2])) # cost of the job
    else:
        for customer_id in db_customers.keys():
            jobs = db_customers[customer_id]["jobs"]
            for job_id in jobs.keys():
                if jobs[job_id][3] == False:
                    display_list.append((db_customers[customer_id]["details"][0],
                                        db_customers[customer_id]["details"][1],
                                        job_id,
                                        jobs[job_id][2]))

    format_columns = "{: <20} | {: <15} | {: <12} | {: ^12}"
    print("\nBill LIST\n")
    column_output(display_list, col_bills, format_columns)

    if not no_prompt:
        input("\nPress Enter to continue.")

def pay_bill():
    # list the customer for reference
    list_customers(no_prompt=True)
    # select customer
    customer_id = validate_db_input(db=db_customers, question= "Please enter customer id: ")
    # show the unpaid bills for reference
    bills_to_pay(customer=customer_id, no_prompt=True)
    # since we don't have GUI interface, manually enter the date of the job
    print("Please enter the date of the bill you want to pay")
    year = digit_input(question="Year: ")
    month = digit_input(question="Month: ")
    day = digit_input(question="Day: ")
    # saving the paid job to customer table, and catching the wrong input date
    try:
        job = db_customers[customer_id]["jobs"][datetime.date(year=(year), month=month, day=day)]
        if job is not None:
            job[3] = True
            print("Thanks for your payment! ")
    except:
        print('We are having problem to process your payment.')

    input("\nPress Enter to continue.")
    

# function to display the menu
def disp_menu():
    print("==== WELCOME TO SELWYN PANEL BEATERS ===")
    print(" 1 - List Customers")
    print(" 2 - List Services")
    print(" 3 - List Parts")
    print(" 4 - Add Customer")
    print(" 5 - Add Job")
    print(" 6 - Display Unpaid Bills")
    print(" 7 - Pay Bill")
    print(" X - eXit (stops the program)")


# ------------ This is the main program ------------------------

# Display menu for the first time, and ask for response
disp_menu()
response = input("Please enter menu choice: ")

# Don't change the menu numbering or function names in this menu
# Repeat this loop until the user enters an "X"
while response not in ['x', 'X']:
    if response == "1":
        list_customers()
    elif response == "2":
        list_services()
    elif response == "3":
        list_parts()
    elif response == "4":
        add_customer()
    elif response == "5":
        add_job()
    elif response == "6":
        bills_to_pay()
    elif response == "7":
        pay_bill()
    else:
        print("\n***Invalid response, please try again (enter 1-6 or X)")

    print("")
    disp_menu()
    response = input("Please select menu choice: ")

print("\n=== Thank you for using Selywn Panel Beaters! ===\n")
