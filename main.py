from collections import UserDict

class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

class Name(Field):
    pass

class Phone(Field):
    def __init__(self, value):
        if len(value) == 10 and value.isdigit():
            super().__init__(value)
        else:
            raise ValueError("Phone number must have 10 digits")

class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []

    def add_phone(self, phone):
        self.phones.append(Phone(phone))

    def remove_phone(self, phone):
        phone_to_remove = None
        for p in self.phones:
            if p.value == phone:
                phone_to_remove = p
                break
        if phone_to_remove:
            self.phones.remove(phone_to_remove)

    def edit_phone(self, old_phone, new_phone):
        for phone in self.phones:
            if phone.value == old_phone:
                phone.value = new_phone
                return f"Phone {old_phone} was changed to {new_phone}."
        return f"Phone {old_phone} not found."

    def __str__(self):
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}"

class AddressBook(UserDict):
    def add_record(self, name, phone):
        if name in self.data:
            self.data[name].add_phone(phone)
        else:
            new_record = Record(name)
            new_record.add_phone(phone)
            self.data[name] = new_record

    def __str__(self):
        return "\n".join(str(record) for record in self.data.values())

def hello(data):
    return "Hello!"

def add_contact(data):
    name, phone = data.split()
    book.add_record(name, phone)
    return f"Added contact {name} with phone {phone}."

def change_phone(data):
    name, old_phone, new_phone = data.split()
    if name in book:
        return book[name].edit_phone(old_phone, new_phone)
    return f"Contact {name} not found."

def get_phone(data):
    name = data.strip()
    if name in book:
        return str(book[name])
    return f"Contact {name} not found."

def show_all(data):
    return str(book)

def good_bye(data):
    return "Goodbye!"

from collections import UserDict

class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

class Name(Field):
    pass

class Phone(Field):
    def __init__(self, value):
        if len(value) == 10 and value.isdigit():
            super().__init__(value)
        else:
            raise ValueError("Phone number must have 10 digits")

class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []

    def add_phone(self, phone):
        self.phones.append(Phone(phone))

    def remove_phone(self, phone):
        phone_to_remove = None
        for p in self.phones:
            if p.value == phone:
                phone_to_remove = p
                break
        if phone_to_remove:
            self.phones.remove(phone_to_remove)

    def edit_phone(self, old_phone, new_phone):
        for phone in self.phones:
            if phone.value == old_phone:
                phone.value = new_phone
                return f"Phone {old_phone} was changed to {new_phone}."
        return f"Phone {old_phone} not found."

    def __str__(self):
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}"

class AddressBook(UserDict):
    def add_record(self, name, phone):
        if name in self.data:
            self.data[name].add_phone(phone)
        else:
            new_record = Record(name)
            new_record.add_phone(phone)
            self.data[name] = new_record

    def __str__(self):
        return "\n".join(str(record) for record in self.data.values())

def hello(data):
    return "Hello!"

def add_contact(data):
    name, phone = data.split()
    book.add_record(name, phone)
    return f"Added contact {name} with phone {phone}."

def change_phone(data):
    name, old_phone, new_phone = data.split()
    if name in book:
        return book[name].edit_phone(old_phone, new_phone)
    return f"Contact {name} not found."

def get_phone(data):
    name = data.strip()
    if name in book:
        return str(book[name])
    return f"Contact {name} not found."

def show_all(data):
    return str(book)

def good_bye(data):
    return "Goodbye!"

def parse_command(full_command):
    split_command = full_command.split(' ', 1)
    primary_command = split_command[0]
    data = split_command[1] if len(split_command) > 1 else ""

    function_to_execute = None
    for func, cmds in COMMANDS.items():
        if primary_command in cmds:
            function_to_execute = func
            break

    if not function_to_execute and len(full_command.split()) > 1:
        potential_two_word_command = " ".join(full_command.split()[:2])
        for func, cmds in COMMANDS.items():
            if potential_two_word_command in cmds:
                function_to_execute = func
                break

    return function_to_execute, data

def remove_phone(data):
    name, phone = data.split()
    if name in book:
        book[name].remove_phone(phone)
        return f"Phone {phone} removed from contact {name}."
    return f"Contact {name} not found."


book = AddressBook()

COMMANDS = {
    hello: ['hello'],
    add_contact: ['add'],
    change_phone: ['change'],
    remove_phone: ['remove'],
    get_phone: ['phone'],
    show_all: ['show all'],
    good_bye: ['good bye', 'close', 'exit']
}

def main():
    while True:
        full_command = input("Enter your command: ")
        command_function, data = parse_command(full_command)
        if command_function:
            print(command_function(data))
            if command_function == good_bye:
                break
        else:
            print("Unknown command.")


if __name__ == "__main__":
    main()
