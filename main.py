from collections import UserDict


class Field:
    def __init__(self, value):
        self._value = value

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, new_value):
        self._value = new_value


class Name(Field):
    pass


class Phone(Field):
    def __init__(self, phone_number):
        if not self.validate(phone_number):
            raise ValueError("Invalid phone number format. It should contain exactly 10 digits.")
        super().__init__(phone_number)

    @staticmethod
    def validate(phone_number):
        return phone_number.isdigit() and len(phone_number) == 10


class Record:
    def __init__(self, name, phone=None):
        self.name = Name(name)
        self.phones = []
        if phone:
            self.add_phone(phone)

    def add_phone(self, phone_number):
        self.phones.append(Phone(phone_number))

    def remove_phone(self, phone_number):
        phone = self.find_phone(phone_number)
        if phone:
            self.phones.remove(phone)

    def edit_phone(self, old_phone, new_phone):
        phone = self.find_phone(old_phone)
        if phone:
            phone.value = new_phone

    def find_phone(self, phone_number):
        for phone in self.phones:
            if phone.value == phone_number:
                return phone
        return None


class AddressBook(UserDict):
    def add_record(self, name, phone=None):
        record = Record(name, phone)
        self.data[name] = record

    def find(self, name):
        return self.data.get(name, None)

    def delete(self, name):
        if name in self.data:
            del self.data[name]


# Тут починається ваш код програми-асистента:

def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except (KeyError, IndexError):
            return "Name not found."
        except ValueError as e:
            return str(e)
    return inner


@input_error
def add_contact(data):
    name, phone = data.split()
    if name not in phonebook:
        phonebook.add_record(name, phone)
    else:
        record = phonebook.find(name)
        record.add_phone(phone)
    return "Contact added."


@input_error
def change_phone(data):
    name, phone = data.split()
    record = phonebook.find(name)
    if not record:
        raise KeyError
    if not record.find_phone(phone):
        record.add_phone(phone)
    else:
        raise ValueError("Phone already exists.")
    return "Phone number added."


@input_error
def get_phone(name):
    record = phonebook.find(name)
    if not record:
        raise KeyError
    return ', '.join([phone.value for phone in record.phones])


@input_error
def show_all():
    return "\n".join([f"{name}: {', '.join([phone.value for phone in record.phones])}" for name, record in phonebook.items()])


def hello():
    return "How can I help you?"


def good_bye():
    return "Good bye!"


def parse_command(full_command):
    # Якщо команда з двох слів
    command_name = " ".join(full_command.split()[:2])
    function_to_execute = None
    for func, cmds in COMMANDS.items():
        if command_name in cmds:
            function_to_execute = func
            break

    if not function_to_execute:
        command_name = full_command.split()[0]  # використовуємо лише перше слово
        for func, cmds in COMMANDS.items():
            if command_name in cmds:
                function_to_execute = func
                break

    data = " ".join(full_command.split()[len(command_name.split()):])

    return function_to_execute, data


COMMANDS = {
    hello: ['hello'],
    add_contact: ['add'],
    change_phone: ['change'],
    get_phone: ['phone'],
    show_all: ['show all'],
    good_bye: ['good bye', 'close', 'exit']
}

phonebook = AddressBook()


def main():
    print("Bot Assistant is here to help you!")
    while True:
        full_command = input("Enter a command: ").strip().lower()
        function_to_execute, data = parse_command(full_command)

        if function_to_execute:
            if function_to_execute in [hello, show_all, good_bye]:
                response = function_to_execute()
            else:
                response = function_to_execute(data)
            print(response)
            if function_to_execute == good_bye:
                break
        else:
            print("Unknown command. Try again.")


if __name__ == "__main__":
    main()
