from collections import UserDict
from datetime import datetime
from typing import List


class AddressBook(UserDict):
    def __str__(self) -> str:
        result = ''

        for name, record in self.data.items():  #type: str, Record
            phones = []
            emails = []

            for obj_phone in record.phone:  #type: List[Phone]
                phones.append(obj_phone.value)  #type: str

            if record.email:
                for obj_email in record.email:  #type: List[Email]
                    emails.append(obj_email.value)  #type: str

            contact_phone = f' phones: {", ".join(phones)}'
            contact_birth = f' | birthday: {record.birthday}' if record.birthday else ''
            contact_email = f' | email: {", ".join(emails)}' if record.email else ''
            contact_address = f'\naddress: {self.address}' if self.address else ''

            result += f'{name}{contact_phone}{contact_birth}{contact_email}{contact_address}\n'

        return result

    def add_record(self, record: 'Record') -> None:
        self.data[record.name.value] = record

    def delete_record(self, name: str) -> None:
        del self[name]

    def iterator(self) -> str:
        for name, record in self.data.items():  #type: str, Record
            birth = record.birthday
            phones = []
            emails = []
            addr = record.address

            for obj_phone in record.phone:  #type: List[Phone]
                phones.append(obj_phone.value)  #type: str

            if record.email is not None:
                for obj_email in record.email:  #type: List[Email]
                    emails.append(obj_email.value)  #type: str

            result = (name, phones, birth, emails, addr)

            yield result


class Field:
    """Class Field is parent for all fields in Record class"""
    def __init__(self, value) -> None:
        self.__value = None
        self.value = value

    def __repr__(self) -> str:
        return f'{self.value}'

    def __str__(self) -> str:
        return self.value


class Birthday(Field):
    """
    Class Birthday for storage birthday's field
    :params: value: datetime obj
    """
    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, value: str):
        self.__value = datetime.strptime(value, '%d%m%Y').date()

    def __repr__(self) -> str:
        return self.value.strftime('%d.%m.%Y')

    def __str__(self) -> str:
        return self.value.strftime('%d-%m-%Y')


class Address(Field):
    """
    Class Address for storage address field
    :params: value: str
    """


class Email(Field):
    """
    Class Email for storage emails field
    :params: value: str
    """


class Name(Field):
    """
    Class Name for storage name's field
    :params: value: str
    """


class Phone(Field):
    """
    Class Phone for storage phone's field
    :params: value: str
    """


class Record:
    """
    Record class responsible for the logic of adding/removing/editing fields.
    :params: Name: str
    :params: Phone: str
    :params: Birthday: datetime obj
    :params: Email: str
    :params: Address: str
    """
    def __init__(self, name: Name, phone: Phone = None, birthday: Birthday = None,
                 email: Email = None, address: Address = None) -> None:
        self.__address = None
        self.__email = None
        self.__birthday = None
        self.__name = None
        self.__phone = None

        self.address = address
        self.birthday = birthday
        self.email = email
        self.name = name
        self.phone = phone

    def __repr__(self) -> str:
        phones = [str(phone) for phone in self.phone]
        emails = [str(email) for email in self.email]

        contact_birth = f' | birthday: {self.birthday}' if self.birthday else ''
        contact_email = f' | email: {", ".join(emails)}' if self.email else ''
        contact_phone = f' phones: {", ".join(phones)}'
        contact_address = f'\naddress: {self.address}' if self.address else ''

        return f'{self.name}{contact_phone}{contact_birth}{contact_email}{contact_address}'

    @property
    def address(self):
        return self.__address

    @address.setter
    def address(self, address: Address):
        self.__address = address

    @property
    def birthday(self):
        return self.__birthday

    @birthday.setter
    def birthday(self, birthday: Birthday):
        self.__birthday = birthday

    @property
    def email(self):
        return self.__email

    @email.setter
    def email(self, emails: List[Email]):
        self.__email = emails

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, name: Name):
        self.__name = name

    @property
    def phone(self):
        return self.__phone

    @phone.setter
    def phone(self, phones: List[Phone]):
        self.__phone = phones

    def add_address(self, addr: Address) -> None:
        self.address = addr

    def add_birthday(self, birth: Birthday) -> None:
        self.birthday = birth

    def add_email(self, email: Email) -> None:
        self.email.extend(email)

    def add_new_phone(self, phones: List[Phone]) -> None:
        self.phone.extend(phones)

    def change_email(self, email_indx: int, new_email: Email) -> None:
        self.email[email_indx] = new_email

    def change_phone(self, phone_indx: int, new_phone: Phone) -> None:
        self.phone[phone_indx] = new_phone

    def days_to_birthday(self) -> int:
        """
        Calculates the number of days until a birthday.
        """
        today = datetime.now().date()
        birth_day = self.__birthday.value.day
        birth_month = self.__birthday.value.month
        birth_year = today.year

        if today.month == birth_month and today.day <= birth_day or today.month < birth_month:
            birth_year = today.year

        else:
            birth_year += 1
            
        next_year_birth = datetime(year=birth_year, month=birth_month, day=birth_day).date()

        days_to_birth = (next_year_birth - today).days
        return days_to_birth

    def delete_email(self, email_indx: Email) -> None:
        del self.email[email_indx]

    def delete_phone(self, phone_indx: Phone) -> None:
        del self.phone[phone_indx]


if __name__ == '__main__':
    book = AddressBook()

    serj = Name('Serj')
    serj_phone = [Phone('321432546')]
    serj_birth = Birthday('01011900')
    serj_email = [Email('addr@gmail.com')]
    serj_addr = Address('London, Baker Street')

    rec_serj = Record(name=serj, phone=serj_phone, birthday=serj_birth,
                      email=serj_email, address=serj_addr)
    book[rec_serj.name.value] = rec_serj

    print('\nbook: ', book.data)
    print(f'book values: {book.data["Serj"]}')
