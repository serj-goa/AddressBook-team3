from base import dump_base, load_base
from phonebook import AddressBook, Birthday, Email, Name, Phone, Record

from pathlib import Path
from re import findall
from typing import List


def input_error(func):
    """
    Generic Exception Handler.
    """
    def inner(*args):
        try:
            return func(*args)
        except KeyError:
            print('Please enter a valid contact name!\n')
        except ValueError:
            print('Please enter a valid data!\n')
        except IndexError:
            print('Invalid command. Please enter the correct command and message.\n')
    return inner


def change_exist_contact(contact_name: str, exist_record: Record) -> bool:
    """
    Requests permission to change data from an existing contact.
    """
    print(f'\nContact {contact_name} is exist!')
    print(exist_record)

    print(f'\nDo you want to change it? (yes/no)')
    change_contact = input('>>> ').strip().lower()

    is_change = False

    if change_contact in ('yes', 'y'):
        is_change = True

    return is_change


@input_error
def command_add(user_data_list: list) -> str:
    """
    Adding a new contact to the phone book.
    """
    if not user_data_list[1]:
        raise KeyError

    user_message = get_message(user_data_list)  #type: str

    if len(user_message.split()) < 2:
        raise ValueError

    contact_name = get_contact_name(user_message)  #type: str
    phones = get_contact_phone(user_message)  #type: List[str]
    birth = get_contact_birthday(user_message)  #type: str or None
    emails = get_contact_email(user_message)  #type: List[str]

    if not phones:
        raise ValueError

    if contact_name not in phonebook:

        new_contact_name = Name(contact_name)
        new_contact_phones = [Phone(ph) for ph in phones]
        new_contact_birth = Birthday(birth) if birth else None
        new_contact_emails = [Email(eml) for eml in emails] if emails else None

        new_record = Record(name=new_contact_name, phone=new_contact_phones,
                            birthday=new_contact_birth, email=new_contact_emails)
        # new_record = Record(name=new_contact_name, phone=new_contact_phones, birthday=birth)
        phonebook[new_record.name.value] = new_record
        return contact_name

    exist_record = phonebook[contact_name]

    for ph in phones:
        if not is_uniq_phone(exist_record, ph):
            raise ValueError

    change_contact = change_exist_contact(contact_name, exist_record)

    if not change_contact:
        raise KeyError

    phones = [Phone(ph) for ph in phones]
    exist_record.add_new_phone(phones)

    if birth is not None:
        exist_record.add_birthday(Birthday(birth))

    for eml in emails:
        if is_uniq_email(exist_record, eml):
            exist_record.add_email(Email(eml))

    return contact_name


def command_add_birth(user_data_list: list) -> str:
    """
    Adding a contact's birthday.
    """
    if not user_data_list[1]:
        raise KeyError

    user_message = get_message(user_data_list)  #type: str
    contact_name = get_contact_name(user_message)  #type: str

    if contact_name not in phonebook:
        raise KeyError

    birth = get_contact_birthday(user_message)  #type: str

    if not birth:
        raise ValueError

    exist_record = phonebook[contact_name]  #type: Record
    exist_record.add_birthday(Birthday(birth))

    return contact_name


@input_error
def command_birth(user_data_list: list) -> None:
    """
    Calculates the number of days until the next birthday of an existing contact.
    """
    if not user_data_list[1]:
        raise KeyError

    user_message = get_message(user_data_list)  #type: str
    contact_name = get_contact_name(user_message)  #type: str

    if contact_name not in phonebook:
        raise KeyError

    record = phonebook[contact_name]  #type: Record

    if record.birthday is None:
        raise ValueError
    
    days_to_birth = record.days_to_birthday()

    if not days_to_birth:
        print(f'Today is {contact_name}\'s birthday.\n')
    else:
        print(f'There are {days_to_birth} days left until {contact_name}\'s birthday.\n')


@input_error
def command_change(user_data_list: list) -> str:
    """
    Change an existing contact in the phone book.
    """
    if not user_data_list[1]:
        raise KeyError

    user_message = get_message(user_data_list)  #type: str

    if len(user_message.split()) < 2:
        raise ValueError

    contact_name = get_contact_name(user_message)  #type: str
    phone_data = get_contact_phone(user_message).split()  #type: list
    contact_phone = phone_data[0]  #type: str
    new_contact_phone = phone_data[1]  #type: str

    if not contact_name in phonebook:
        raise KeyError

    elif not contact_phone:
        raise ValueError

    else:
        new_phone = Phone(new_contact_phone)
        record  = phonebook[contact_name]  #type: Record

        for idx, rec_phone in enumerate(record.phone):
            if rec_phone.value == contact_phone:
                record.change_phone(phone_indx=idx, new_phone=new_phone)

        return contact_name


def command_close_program(_) -> str:
    print('Good bye!\n')
    return 'quit'


def command_del(user_data_list: list) -> str:
    """
    Remove contact from the phone book.
    """
    if not user_data_list[1]:
        raise KeyError

    user_message = get_message(user_data_list)  #type: str
    contact_name = get_contact_name(user_message)  #type: str

    if contact_name in phonebook:
        phonebook.delete_record(contact_name)
        return contact_name

    else:
        raise KeyError


def command_find(user_data_list: list):
    """
    Finds contact data based on the entered pattern.
    """
    iter_phonebook = phonebook.iterator()
    some_data = ' '.join(user_data_list[1:]).split()
    search_matching = []

    for _ in range(len(phonebook)):
        name, phones, birth, email = next(iter_phonebook)
        str_phones = ' '.join(phones) if phones else ''
        str_email = ' '.join(email) if email else ''
        cnt = 0

        for user_kw in some_data:

            if user_kw.lower() in name.lower():
                cnt += 1
            elif user_kw in str_phones:
                cnt += 1
            elif user_kw in str_email:
                cnt += 1

        if cnt > 0:
            search_matching.append((name, phones, birth, email))

    if search_matching:

        for contact in search_matching:
            result = get_record_for_print(contact)
            print(result)
        print()

    else:
        print('Nothing was found according to your request.\n')


def command_hello(_) -> None:
    print('How can I help you?\n')


def command_help(_) -> None:
    print('''
"hello"                                 - greetings.
"add <new_name> <new_phone(s)> and optionaly[<birthday>]" - adding a new contact.
"add birth <name> <birthday>            - adding a contact's birthday (01.01.2000).
"change <name> <old_phone> <new_phone>" - change the phone number of an existing contact.            
"birth <name>"                          - show how many days are left until the next birthday.
"del <name>"                            - remove contact from phonebook.
"show all"                              - show all saved contacts with phone numbers.
"phone <name>"                          - show phone numbers for an existing contact.
"find <pattern>"                        - Finds contact data based on the entered pattern.
"good bye", "close", "exit"             - exit from the program. 
    ''')


@input_error
def command_phone(user_data_list: list) -> None:
    """
    Search for an existing contact in the phone book.
    """
    if not user_data_list[1]:
        raise KeyError

    user_message = get_message(user_data_list)   #type: str
    contact_name = get_contact_name(user_message)   #type: str

    if contact_name in phonebook:
        record = phonebook[contact_name]  #type: Record
        contact_phones = [phone.value for phone in record.phone]
        print(f'{contact_name}: {", ".join(contact_phones)}\n')
    else:
        raise KeyError


def command_show_all(_) -> None:
    """
    Display all existing contacts in the phone book.
    """
    print()
    cnt = 0
    limit_iter = len(phonebook)
    iter_phonebook = phonebook.iterator()
    user_choice = None

    while cnt < limit_iter:
        record_data = next(iter_phonebook)
        result = get_record_for_print(record_data)
        print(result)

        cnt += 1
        if cnt == limit_iter:
            break
        elif not cnt % 5:
            user_choice = input('\nPress "Enter" to show more contact or type "quit" for stop printing contacts ').strip()
        if user_choice == 'quit':
            break
    print()


def confirmation_report(contact_name: str, user_command: tuple) -> None:
    """
    Report on the successful addition or change of contact details.
    """
    print(f'Contact {contact_name} {user_command} successful.\n')


@input_error
def get_command(some_data: list) -> str:
    """
    Getting a user command.
    """
    if not some_data[0]:
        raise IndexError
    else:
        user_command = some_data[0].lower()
    return user_command


@input_error
def get_contact_birthday(some_string: str) -> str or None:
    """
    Getting the date of birth from the data transmitted by the user.
    """
    data_lst = some_string.split()
    birth = None

    if len(data_lst) > 1:

        for data in data_lst[::-1]:
            clear_data = normalize_msg(data)
            if clear_data.isdigit() and len(clear_data) == 8:
                birth = clear_data

    return birth


@input_error
def get_contact_email(some_string: str) -> list:
    """
    Getting the date of email from the data transmitted by the user.
    """
    emails = findall(r"[a-zA-Z][\w\.]+@[a-zA-Z]{2,}\.[a-zA-Z]{2,}", some_string)
    return emails


@input_error
def get_contact_name(some_string: str) -> str:
    """
    Getting the name from the data passed by the user.
    """
    data_lst = some_string.split()

    if len(data_lst) >= 1:
        name_data = []

        for data in data_lst:
            clear_data = normalize_msg(data)
            if clear_data.isdigit():
                break
            name_data.append(data)

        contact_name = ' '.join(name_data)

        return contact_name

    else:
        raise IndexError


def get_contact_phone(some_string: str) -> str:
    """
    Getting the phone from the data transmitted by the user.
    """
    clear_data = normalize_msg(some_string)
    result = findall(r'(?:\+\d{2})?\d{3,4}\D?\d{3}\D?\d{3}', clear_data)
    return result
    # data_lst = some_string.split()
    #
    # if len(data_lst) > 1:
    #     phone_data = []
    #
    #     for data in data_lst[::-1]:
    #         clear_data = normalize_msg(data)
    #         if clear_data.isdigit() and len(clear_data) >= 10:
    #             phone_data.insert(0, data)
    #         elif clear_data.isdigit():
    #             continue
    #         else:
    #             break
    #
    #     phones = ' '.join(phone_data)

    # return phones


@input_error
def get_message(some_data: list) -> str:
    """
    Receiving data (name, phone) transferred by the user.
    """
    if not some_data[1]:
        raise IndexError
    else:
        user_message = some_data[1].strip()
    return user_message


def get_record_for_print(record_data: tuple) -> str:
    name = record_data[0]
    phones = f' | phones: {", ".join(record_data[1])}' if record_data[1] else ''
    birthday = f' | birthday: {record_data[2]}' if record_data[2] else ''
    emails = f' | email: {", ".join(record_data[3])}' if record_data[3] else ''

    result = f'{name}{phones}{birthday}{emails}'

    return result


def is_uniq_email(exist_record: Record, email: str) -> bool:
    """
    Checks the uniqueness of a contact's phone number.
    """
    for eml in exist_record.email:  #type: List[Email]
        if email == eml.value:
            return False
    return True



def is_uniq_phone(exist_record: Record, phone: str) -> bool:
    """
    Checks the uniqueness of a contact's phone number.
    """
    for ph in exist_record.phone:  #type: List[Phone]
        if phone == ph.value:
            return False
    return True


def normalize_msg(message: str) -> str:
    """
    Clears a string of unnecessary characters.
    """
    symbols = '-=_./\\'
    for symb in symbols:
        message = message.replace(symb, '')
    return message


def parse_command_and_message(user_input: str) -> list:
    """
    Receiving command and data (name, phone) sent by the user.
    """
    separator = ' '
    for cmd in PROGRAM_CMD:
        if user_input.lower().startswith(cmd):
            separator = cmd
            user_input = cmd + user_input[len(cmd) + 1:]
            break

    some_string_lst = user_input.split(separator, 1)
    if separator != ' ':
        some_string_lst[0] = separator
    return some_string_lst


@input_error
def run_command(user_data_list: list) -> tuple:
    """
    Run a command received from the user.
    """
    if not user_data_list[0]:
        raise IndexError
    else:
        user_command = get_command(user_data_list)

        if PROGRAM_CMD.get(user_command) is None:
            raise IndexError
        else:
            return_contact_name = PROGRAM_CMD[user_command](user_data_list)
            return user_command, return_contact_name


def main():
    print('Please, enter your command: ')

    while True:
        user_input = input('cmd >>> ').strip()
        user_data_list = parse_command_and_message(user_input)
        data_after_run_cmd = run_command(user_data_list)

        if data_after_run_cmd and data_after_run_cmd[1] == 'quit':
            break

        elif data_after_run_cmd and data_after_run_cmd[1] is not None:
            confirmation_report(user_command=data_after_run_cmd[0], contact_name=data_after_run_cmd[1])


if __name__ == '__main__':

    CURRENT_DIR = Path(__file__).parent
    FILE_DB = 'phone_db.bin'
    FILE_PATH = CURRENT_DIR / FILE_DB

    phonebook = load_base(FILE_PATH)  #type: AddressBook
    PROGRAM_CMD = {
        'add birth': command_add_birth, 
        'add': command_add, 
        'birth': command_birth,
        'change': command_change, 
        'del': command_del, 
        'find': command_find, 
        'phone': command_phone,
        'hello': command_hello,
        'help': command_help,
        'show all': command_show_all,
        'good bye': command_close_program,
        'close': command_close_program, 
        'exit': command_close_program
        }

    try:
        main()

    except KeyboardInterrupt:
        print('Good bye!\n')
        
    finally:
        print(dump_base(FILE_PATH, phonebook))
