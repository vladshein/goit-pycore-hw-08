#HW7 task2
import os
from HW8_part1 import AddressBook, Record, Birthday
import pickle

#save data to the disk using pickle
def save_data(book, filename="addressbook.pkl"):
    with open(filename, "wb") as f:
        pickle.dump(book, f)

#load data from disk using pickle
def load_data(filename="addressbook.pkl"):
    try:
        with open(filename, "rb") as f:
            return pickle.load(f)
    except FileNotFoundError:
        return AddressBook()  


#decorator to work with incorrect input
def input_error(func):
    def inner(args, contacts):
        try:
            return func(args, contacts)

        except ValueError:
            return "Number of provided arguments is incorrect.Please correct your input."
        
        #checked also inside function by using  if-in operators
        except KeyError:
            return "Incorrect phone number or name. Please correct your input."
 
        except IndexError:
            "Index your are trying to access is incorrect. Please provide the correct one."

    return inner

#handler funcions
#function to parse input from user
def parse_input(user_input):
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower() 
    return cmd, *args

#function to add a contact in a dictionary
@input_error
def add_contact(args, book):
    name, phone, *_ = args
    record = book.find(name)
    message = "Contact updated"
    if record is None:
        record = Record(name)
        book.add_record(record)
        message = "Contact added"
    if phone:
        if len(phone) != 10:
            return f"Incorrect phone length"
        elif phone.isnumeric() != True:
            return f"Only digits can be entered"

        #check phone format before adding
        record.add_phone(phone)

    return message

#function to change a phone number by a name
@input_error
def change_contact(args, book):
    name, old_phone, new_phone, *_ = args
    record = book.find(name)
    record.edit_phone(old_phone, new_phone)

#function to show phone number by a name    
@input_error
def show_phone(args, book):
    name, *_ = args
    
    record = book.find(name)
    if record == None:
        return "Name is not in the address book"
    record.show_all_phones()    

#function to show all contacts
@input_error
def show_all(args, book):
    if len(book) == 0:
        return "Contacts are empty"
    
    for name, record in book.data.items():
        print(record)
    return "End of show all command"

@input_error
def add_birthday(args, book):
    name, bday, *_ = args 
    record = book.find(name)
    if record == None:
        return "Name is not in address book"
    birthday = Birthday(bday)
    record.add_birthday(birthday)
    return f"{name} birthday was processed"

@input_error
def show_birthday(args, book):
    name, *_ = args
    record = book.find(name)
    if record == None:
        return "Name is not in contact list"
    return f"{name} birthday: {record.birthday}"

@input_error
def birthdays(args, book):
    return book.get_upcoming_birthdays()
    
#main logic
def main():
    print("Welcome to the assistant bot")

    #book = AddressBook()
    book = load_data()

    while True:
        user_input = input("Enter a command:\n").strip().lower()

        command, *args = parse_input(user_input)

        if command == 'exit' or command == 'close':
            print("Good bye!")
            save_data(book)
            os._exit(0)

        elif command == 'hello':
            print('How can I help you?')
            continue

        elif command == 'add':
            print("\n=== Add contact start ===")
            print(add_contact(args, book))
            print("=== Add contact end ===\n")

        elif command == 'change':
            print("\n=== Change contact start ===")
            change_contact(args, book)
            print("=== Change contact end ===\n")

        elif command == 'phone':
            print("\n=== Show phone start ===")
            print(show_phone(args, book))  
            print("=== Show phone end ===\n")

        elif command == 'all':
            print("\n=== Show all contacts start ===")
            print(show_all(args, book))
            print("=== Show all contacts end ===\n")
        
        elif command == 'add_birthday':
            print("\n=== Add birthday start ===")
            print(add_birthday(args, book))
            print("=== Add birthday end ===\n")
        
        elif command == 'show_birthday':
            print("\n=== Show birthday start ===")
            print(show_birthday(args, book))
            print("=== Show birthday end ===\n")
        
        elif command == 'birthdays':
            print("\n=== Birthdays start ===")
            print(birthdays(args, book))
            print("=== Birthdays end ===\n")

        else:
            print("Invalid command. Please correct your input.")

    print("End of contact assistant work")
    

if __name__ == "__main__":
    main()
