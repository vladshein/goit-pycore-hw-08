#HW7 task1

from collections import UserDict
from datetime import datetime
import re

# base class field
class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

# name class inherited from base class Field
class Name(Field):
    # реалізація класу
	pass

# phone class inherited from base class Field
class Phone(Field):
    # реалізація класу
    def check_phone(self, phone):
        if len(phone) != 10:
            return f"Incorrect phone length"
        elif phone.isnumeric() != True:
            return f"Length of phone is correct, but not only digits entered"
        else:
            return f"Phone number is correct and can be added to the book"

#new class Birthday
class Birthday(Field):
    def __init__(self, value):
        try:
            #check if value is string
            if type(value) != str:
               raise ValueError
            #check if value has correct length
            elif len(value) != 10:
                raise ValueError

            #check the format of provided date string 
            date_format = r"^\d{2}\.\d{2}\.\d{4}$"
            date_match = re.search(date_format, value)    
            if date_match:
                parsed_date = datetime.strptime(value, "%d.%m.%Y").date()
                self.value = parsed_date

        except ValueError:
            print("Invalid date format. Use DD.MM.YYYY")

# record class to store and process phone records
class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None

    def __str__(self):
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}, birthday: {self.birthday}"

    def add_birthday(self, birthday):
        self.birthday = birthday

    def add_phone(self, phone):
        self.phones.append(Phone(phone))

    def remove_phone(self, phone):
        for i in range(len(self.phones)):
            if phone == self.phones[i].value:
                self.phones.remove(self.phones[i])
                break
        
    def edit_phone(self, phone, new_phone):
        for i in range(len(self.phones)):
            if phone == self.phones[i].value:
                self.phones[i].value = new_phone
        
    def find_phone(self, phone):
        for i in range(len(self.phones)):
            if phone == self.phones[i].value:
                return phone
            else:
                return None
    
    def show_all_phones(self):
        if not self.phones:
            print("List of phones is empty")
        else:
            print(f"phones: {'; '.join(p.value for p in self.phones)}")


# create address book         
class AddressBook(UserDict):
    # реалізація класу
    def add_record(self, record):
        self.data[record.name] = record

    #find record by name
    def find(self, name):
        for key in self.data.keys():
            if key.value == name:
                return self.data[key]
    
    def delete(self, name):
        for key in self.data.keys():
            if name == key.value:
                self.data.pop(key)
                break
    
    def get_upcoming_birthdays(self):
        congrats_list = []

        #get current date
        current_date = datetime.now().date()
        print(f"Today is {current_date}")

        for rec_name, record in self.data.items():
            birthday_this_year = record.birthday.value.replace(year=2024)
            if birthday_this_year < current_date:
                print("Birtday will be in next year")
                continue
            else:
                delta = (birthday_this_year - current_date).days 
                print(delta)

                if delta <= 7:
                    print("Birthday is within 7 days.")
                    #check weekend case
                    congratulation_date = birthday_this_year
                    if birthday_this_year.weekday() == 5:
                        print("Birthday is on a weekend. Congratulate on Monday")
                        updated_date = int(birthday_this_year.day) + 2
                        congratulation_date = birthday_this_year.replace(day=updated_date) 
                        print(congratulation_date)
                
                    elif birthday_this_year.weekday() == 6:
                        print("Birthday is on a weekend. Congratulate on Monday")
                        updated_date = int(birthday_this_year.day) + 1
                        congratulation_date = birthday_this_year.replace(day=updated_date) 
                        print(congratulation_date) 
                    #add name and congratulation data to list of dicts
                    local_dict = {}
                    local_dict[rec_name.value] = congratulation_date
                    congrats_list.append(local_dict)

        print(congrats_list)
        return congrats_list

def main():
    #test data
    # Створення запису для john
    john_record = Record("John")
    jane_record = Record("Jane")

    #add johns phones
    john_record.add_phone("1234567890")
    john_record.add_phone("5555555555")
    john_record.add_phone("3333333333")
    john_record.add_phone("7777777777")

    #add janes phones
    jane_record.add_phone("2223332222")
    jane_record.add_phone("1112221111")

    print(jane_record)
    print(john_record)

    #add birthdays 
    bd_john = "01.08.2022"
    john_birthday = Birthday(bd_john)
    john_record.add_birthday(john_birthday)

    bd_jane = "02.09.1999"
    jane_birthday = Birthday(bd_jane)
    jane_record.add_birthday(jane_birthday)
    #print record and birthday
    print(john_record)
    print(jane_record)

    found_phone = john_record.find_phone("1234567890")

    john_record.edit_phone("1234567890", "2345678901")
    print(john_record)

    john_record.remove_phone("3333333333")
    print(john_record)

    book = AddressBook()

    book.add_record(john_record)
    book.add_record(jane_record)
    john = book.find("John")
    print(john)

    upcoming_bdays = book.get_upcoming_birthdays()
    print(f"upcoming_bdays are {upcoming_bdays}")

    for name, record in book.data.items():
        print(record)

    book.delete("John")

    for name, record in book.data.items():
        print(record)

if __name__ == "__main__":
    main()