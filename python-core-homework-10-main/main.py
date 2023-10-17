from collections import UserDict

class Field:
    def __init__(self, value):
        self.value = value

class Name(Field):
    pass

class Phone(Field):
    def __init__(self, value):
        if not str(value).isdigit() or len(str(value)) != 10:
            raise ValueError("Phone number must have 10 digits and contain only numbers.")
        self.value = value

    def __eq__(self, other):
        if isinstance(other, Phone):
            return self.value == other.value
        return False

    def __str__(self):
        return self.value

class Record:
    def __init__(self, name: Name):
        self.name = name
        self.phones = []

    def add_phone(self, phone: Phone):
        self.phones.append(phone)

    def remove_phone(self, phone: Phone):
        self.phones.remove(phone)

    def edit_phone(self, old_phone: Phone, new_phone: Phone):
        index = self.phones.index(old_phone)
        self.phones[index] = new_phone

    def find_phone(self, phone: Phone):
        if phone in self.phones:
            return phone
        return None

class AddressBook(UserDict):
    def add_record(self, record: Record):
        if isinstance(record.name, Name):
            self.data[record.name.value] = record
        else:
            self.data[record.name] = record

    def find(self, name: str):
        return self.data.get(name, None)

    def delete(self, name: str):
        if name in self.data:
            del self.data[name]

def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except KeyError:
            return "Enter user name"
        except ValueError as ve:
            return str(ve)
        except IndexError:
            return "Give me name and phone please"
    return inner

@input_error
def hello(*args):
    return "How can I help you?"

@input_error
def add(address_book: AddressBook, name, phone):
    name_obj = Name(name)
    phone_obj = Phone(phone)
    record = address_book.find(name)
    
    if record:
        record.add_phone(phone_obj)
    else:
        new_record = Record(name_obj)
        new_record.add_phone(phone_obj)
        address_book.add_record(new_record)

    return "Contact added!"

@input_error
def change(address_book: AddressBook, name, old_phone, new_phone):
    old_phone_obj = Phone(old_phone)
    new_phone_obj = Phone(new_phone)
    record = address_book.find(name)
    
    if not record:
        raise KeyError

    if old_phone_obj not in record.phones:
        raise ValueError("Old phone number not found!")

    record.edit_phone(old_phone_obj, new_phone_obj)
    return "Phone number changed!"

@input_error
def phone(address_book: AddressBook, name):
    record = address_book.find(name)
    
    if not record:
        raise KeyError

    return ", ".join([phone.value for phone in record.phones])


@input_error
def remove_phone(address_book: AddressBook, name, phone):
    phone_obj = Phone(phone)
    record = address_book.find(name)
    
    if not record:
        raise KeyError

    if phone_obj not in record.phones:
        raise ValueError("Phone number not found!")

    record.remove_phone(phone_obj)
    return "Phone number removed!"

@input_error
def show_all(address_book: AddressBook):
    return "\n".join([f"{record.name.value}: {', '.join([phone.value for phone in record.phones])}" for name, record in address_book.data.items()])

@input_error
def delete_record(address_book: AddressBook, name):
    if not address_book.find(name):
        raise KeyError("Record not found!")

    address_book.delete(name)
    return f"Record for {name} deleted!"

def good_bye(data):
    return 'Good bye!'

def parse_command(full_command):
    split_command = full_command.split(' ', 1)
    primary_command = split_command[0]
    data = split_command[1] if len(split_command) > 1 else ""

    function_to_execute = None
    for func, cmds in COMMANDS.items():
        if primary_command in cmds:
            function_to_execute = func
            break

    # Перевіряємо, чи може команда бути двослівною
    if not function_to_execute:
        potential_two_word_command = full_command.split(' ', 2)
        if len(potential_two_word_command) > 1:
            two_word_command = " ".join(potential_two_word_command[:2])
            for func, cmds in COMMANDS.items():
                if two_word_command in cmds:
                    function_to_execute = func
                    data = potential_two_word_command[2] if len(potential_two_word_command) > 2 else ""
                    break

    return function_to_execute, data


COMMANDS = {
    hello: ['hello'],
    add: ['add'],
    change: ['change'],
    remove_phone: ['remove'],
    delete_record: ['delete'],
    phone: ['phone'],
    show_all: ['show all'],
    good_bye: ['good bye', 'close', 'exit']
}

@input_error
def main():
    address_book = AddressBook()

    while True:
        command = input("Enter command: ").lower()

        command_name, data = parse_command(command)

        func = command_name

        if not func:
            print("Command not found!")
            continue

        print(func(address_book, *data.split()))

        if command_name == good_bye:
            
            break

if __name__ == "__main__":
    main()
