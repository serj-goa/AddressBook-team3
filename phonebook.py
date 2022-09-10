from collections import UserDict
from datetime import datetime
from typing import List
from unittest import result


class AddressBook(UserDict):
    def __str__(self) -> str:
        result = ''

        for name, record in self.data.items():  #type: str, Record
            phones = []

            for obj_phone in record.phone:  #type: List[Phone]
                phones.append(obj_phone.value)  #type: str

            if record.birthday:  #type: Birthday
                result += f'Contact name: {name}, phones: {", ".join(phones)}, birthday: {record.birthday}\n'
            else:
                result += f'Contact name: {name}, phones: {", ".join(phones)}\n'

        return result

    def add_record(self, record: 'Record') -> None:
        self.data[record.name.value] = record

    def delete_record(self, name: str) -> None:
        del self[name]

    def iterator(self) -> str:
        for name, record in self.data.items():  #type: str, Record
            birth = record.birthday
            phones = []

            for obj_phone in record.phone:  #type: List[Phone]
                phones.append(obj_phone.value)  #type: str

            result = (name, phones, birth)

            # if record.birthday:  #type: Birthday
            #     result = f'Contact name: {name}, phones: {", ".join(phones)}, birthday: {record.birthday}'
            # else:
            #     result = f'Contact name: {name}, phones: {", ".join(phones)}'

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
    """
    def __init__(self, name: Name, phone: Phone = None, birthday: Birthday = None) -> None:
        self.__birthday = None
        self.__name = None
        self.__phone = None

        self.birthday = birthday
        self.name = name
        self.phone = phone

    def __repr__(self) -> str:
        phones = [str(phone) for phone in self.phone]
        
        if self.birthday:
            return f'Phone: {", ".join(phones)}, Birthday: {self.birthday.value}'

        return f'Phone: {", ".join(phones)}'

    @property
    def birthday(self):
        return self.__birthday

    @birthday.setter
    def birthday(self, birthday: Birthday):
        self.__birthday = birthday

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, name):
        self.__name = name

    @property
    def phone(self):
        return self.__phone

    @phone.setter
    def phone(self, phones: List[Phone]):
        self.__phone = phones

    def add_birthday(self, birth: Birthday) -> None:
        self.birthday = birth

    def add_new_phone(self, phones: List[Phone]) -> None:
        self.phone.extend(phones)

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

        if today.month >= birth_month and today.day > birth_day:
            birth_year += 1
            
        next_year_birth = datetime(year=birth_year, month=birth_month, day=birth_day).date()

        days_to_birth = (next_year_birth - today).days
        return days_to_birth

    def delete_phone(self, remove_phone: Phone) -> None:
        self.phone.remove(remove_phone)


if __name__ == '__main__':
    book = AddressBook()

    serj = Name('Serj')
    serj_phone = [Phone('321432546')]
    serj_birth = Birthday('01011900')
    serj_birth = Birthday('01012000')
    print(serj_birth.value)
    rec_serj = Record(serj, serj_phone, serj_birth)

    new_phone_1 = Phone('433465675')
    new_phone_2 = Phone('753367888')

    rec_serj.add_new_phone([new_phone_1, new_phone_2])

    print('rec_name: ', rec_serj.name.value)
    print('rec_phone: ', rec_serj.phone)

    rec_serj.change_phone(phone_indx=0, new_phone=Phone('11111111111'))

    print('\nrec_phone after deleting phone: ', rec_serj.phone)
    print('rec_phone after change: ', rec_serj.phone[0])

    book.add_record(record=rec_serj)
    print('\nbook: ', book.data)
    print(f'book values: {book.data["Serj"]}')
