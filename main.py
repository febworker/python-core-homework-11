from datetime import datetime, timedelta
from collections import UserDict

# Клас Field для представлення загальних полів
class Field:
    def __init__(self, value):
        self._value = value

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, new_value):
        self._value = new_value

# Клас Name для представлення імен
class Name(Field):
    pass

# Клас Phone для представлення номерів телефонів
class Phone(Field):
    def __init__(self, value):
        # Перевірка валідності номеру телефону
        if not self.is_valid(value):
            raise ValueError("Invalid phone number")
        super().__init__(value)

    def is_valid(self, number):
        # Перевірка, чи є номер телефону валідним
        # Ваші власні правила перевірки можна додати тут
        return len(number) == 10 and number.isdigit()

    @Field.value.setter
    def value(self, new_value):
        if not self.is_valid(new_value):
            raise ValueError("Invalid phone number")
        self._value = new_value

# Клас Birthday для представлення днів народження
class Birthday(Field):
    def __init__(self, value):
        # Перевірка валідності дати народження
        if not self.is_valid(value):
            raise ValueError("Invalid birthday")
        super().__init__(value)

    def is_valid(self, date):
        # Перевірка, чи є дата народження валідною
        try:
            datetime.strptime(date, "%Y-%m-%d")
            return True
        except ValueError:
            return False

    @Field.value.setter
    def value(self, new_value):
        if not self.is_valid(new_value):
            raise ValueError("Invalid birthday")
        self._value = new_value

# Клас Record для представлення контактів з кількома полями
class Record:
    def __init__(self, name, birthday=None):
        self.name = Name(name)
        self.phones = []
        self.birthday = Birthday(birthday) if birthday else None

    def add_phone(self, phone):
        self.phones.append(Phone(phone))

    def find_phone(self, number):
        for phone in self.phones:
            if isinstance(phone, Phone) and phone.value == number:
                return phone
        return None

    def edit_phone(self, old_number, new_number):
        for phone in self.phones:
            if isinstance(phone, Phone) and phone.value == old_number:
                phone.value = new_number
                return
        raise ValueError(f"Phone number {old_number} not found.")

    def remove_phone(self, number):
        for phone in self.phones:
            if isinstance(phone, Phone) and phone.value == number:
                self.phones.remove(phone)
                return
        raise ValueError(f"Phone number {number} not found.")

    def days_to_birthday(self):
        if self.birthday:
            today = datetime.now().date()
            next_birthday = datetime(today.year, *map(int, self.birthday.value.split("-"))).date()
            if today > next_birthday:
                next_birthday = datetime(today.year + 1, *map(int, self.birthday.value.split("-"))).date()
            return (next_birthday - today).days
        else:
            return None

# Клас AddressBook для представлення книги адрес
class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.value] = record

    def find(self, name):
        return self.data.get(name)

    def delete(self, name):
        if name in self.data:
            del self.data[name]

    def iterator(self, chunk_size=5):
        records = list(self.data.values())
        for i in range(0, len(records), chunk_size):
            yield records[i:i + chunk_size]

# Клас Assistant для управління контактами та взаємодією з користувачем
class Assistant:
    def __init__(self):
        self.contacts = AddressBook()

    def hello(self):
        return "How can I help you?"

    def add_contact(self, name, phone_number, birthday=None):
        # Створення екземпляра Record для кожного контакту
        record = self.contacts.find(name) or Record(name, birthday)
        # Створення екземпляра Phone для кожного номеру телефону
        phone = Phone(phone_number)
        record.add_phone(phone)
        self.contacts.add_record(record)
        return f"Contact {name} added with phone number {phone_number}."

    def change_contact(self, name, new_phone_number):
        record = self.contacts.find(name)
        if record:
            record.edit_phone(record.phones[0].value, new_phone_number)
            return f"Phone number for {name} updated: {new_phone_number}."
        else:
            raise KeyError

    def phone_contact(self, name):
        record = self.contacts.find(name)
        if record:
            return f"Phone number for {name}: {record.phones[0].value}."
        else:
            raise KeyError

    def show_all_contacts(self):
        if self.contacts:
            result = "All saved contacts:\n"
            for chunk in self.contacts.iterator():
                for record in chunk:
                    result += f"{record.name.value}: {record.phones[0].value}"
                    if record.birthday:
                        result += f", Birthday: {record.birthday.value}"
                    result += "\n"
            return result.strip()
        else:
            return "No contacts saved."

    def main(self):
        while True:
            user_input = input("Enter a command: ").lower()
            if user_input in ["good bye", "close", "exit"]:
                print("Good bye!")
                break
            elif user_input.startswith("hello"):
                print(self.hello())
            elif user_input.startswith("add"):
                try:
                    _, name, phone_number, *birthday = user_input.split()
                    birthday = birthday[0] if birthday else None
                    print(self.add_contact(name, phone_number, birthday))
                except ValueError:
                    print("Error: Invalid command format. Usage: add [name] [phone_number] [birthday]")
            elif user_input.startswith("change"):
                try:
                    _, name, new_phone_number = user_input.split()
                    print(self.change_contact(name, new_phone_number))
                except ValueError:
                    print("Error: Invalid command format. Usage: change [name] [new_phone_number]")
            elif user_input.startswith("
