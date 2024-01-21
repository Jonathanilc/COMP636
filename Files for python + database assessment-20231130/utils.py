# ============== Selwyn Panel Beaters MAIN PROGRAM ==============
# Student Name: Jonathan Xu
# Student ID : 1159350
# NOTE: this file is for utils fn
# =================================================================================

def no_empty_input(question):
    response = input(question)
    while not response:
        response = input("Value can not be empty, please enter again: ")
    return response

def validate_db_input(db, question):
    response = input(question)
    while not response.isdigit():
        response = input("Please enter number only: ")
    while int(response) not in db.keys():
        response = input("No record found, please enter again: ")
    
    return int(response)

def recursively_add(db, question):
    has_more_to_add = input("Press enter to add record, or type 'No' to finish: ")
    list = []
    
    while has_more_to_add != "No":
        list.append(validate_db_input(db=db, question=question))
        has_more_to_add = input("Press enter to add more value, or enter No to finish: ")
    
    return tuple(set(list))

def digit_input(question):
    response = input(question)
    while not response.isdigit():
        response = input("Value need to be digit, please enter again: ")
    return int(response)