
import clean

from base import dump_base, load_base
from birthlist import get_birthdays_per_week
from phonebook import AddressBook, Address, Birthday, Email, Name, Phone, Record

from pathlib import Path
from re import findall
from typing import List

from Notes import Notes

def input_error(func):
    """
    Generic Exception Handler.
    """
    def inner(*args):
        try:
            return func(*args)
        except AttributeError:
            print('Please enter a valid data!\n')
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


@input_error
def command_add_address(user_data_list: list) -> str:
    """
    Adding a contact address.
    """
    user_message = get_message(user_data_list)  # type: str

    contact_name = None
    contact_addr = None

    if user_message is not None:
        for name in phonebook.keys():
            if user_message.startswith(name):
                contact_name = name
                contact_addr = user_message.lstrip(name + ' ')

        if contact_name is None:
            raise KeyError

        if not contact_addr:
            raise ValueError

        if contact_name and contact_addr:
            exist_record = phonebook[contact_name]  #type: Record
            exist_record.add_address(Address(contact_addr))

    return contact_name


@input_error
def command_add_birth(user_data_list: list) -> str:
    """
    Adding a contact birthday.
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
def command_add_email(user_data_list: list):
    """
    Adding a contact email.
    """
    user_message = get_message(user_data_list)  # type: str
    contact_name = get_contact_name(user_message)  # type: str

    if contact_name not in phonebook:
        raise KeyError

    emails = get_contact_email(user_message)  #type: list

    if not emails:
        print('Email must match the pattern <username@domein.com>')
        raise ValueError

    new_contact_emails = [Email(eml) for eml in emails]
    exist_record = phonebook[contact_name]  #type: Record

    if exist_record.email is None:
        exist_record.email = new_contact_emails
    else:
        exist_record.add_email(new_contact_emails)

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
def command_birth_week(user_data_list: list) -> None:
    get_birthdays_per_week(phonebook)


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


@input_error
def command_change_email(user_data_list: list) -> str:
    """
    Change the email address of an existing contact in the phone book.
    """
    if not user_data_list[1]:
        raise KeyError

    user_message = get_message(user_data_list)  # type: str

    if len(user_message.split()) < 2:
        raise ValueError

    contact_name = get_contact_name(user_message)  # type: str
    email_data = get_contact_email(user_message)  # type: list
    contact_email = email_data[0]  # type: str
    new_contact_email = email_data[1]  # type: str

    if not contact_name in phonebook:
        raise KeyError

    elif not contact_email:
        raise ValueError

    new_email = Email(new_contact_email)
    record = phonebook[contact_name]  # type: Record

    for idx, rec_email in enumerate(record.email):
        if rec_email.value == contact_email:
            record.change_email(email_indx=idx, new_email=new_email)

            return contact_name

    print(f'{contact_name} contact does not have this email {contact_email}.')
    raise ValueError


def command_clean(user_data_list: list):
    """
    Sorts files in a folder selected by the user.
    """
    user_message = get_message(user_data_list)  # type: str

    if user_message:

        try:
            path_argv = Path(user_message)
            print(f'path_argv: {path_argv}')
        except IndexError:
            print('Please add sorting path!')

        if not Path(path_argv).is_dir():
            print('Incorrect path. Please add valid path!')

        else:
            clean.main(path_argv)


def command_close_program(_) -> str:
    print('Good bye!\n')
    return 'quit'


@input_error
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


@input_error
def command_del_email(user_data_list: list) -> str:
    """
    Remove contact email from the phone book.
    """
    if not user_data_list[1]:
        raise KeyError

    user_message = get_message(user_data_list)  # type: str
    contact_name = get_contact_name(user_message)  # type: str
    email_data = get_contact_email(user_message)  # type: list

    if contact_name not in phonebook:
        raise KeyError

    record = phonebook[contact_name]  # type: Record

    if not email_data:
        raise ValueError

    if record.email is None:
        raise ValueError

    flag = False
    del_idx = []
    for idx, rec_email in enumerate(record.email):
        for email in email_data:
            if rec_email.value == email:
                del_idx.append(idx)
                flag = True

    if flag:
        for idx in del_idx[::-1]:
            record.delete_email(email_indx=idx)
        return contact_name

    print(f'{contact_name} contact does not have this email {contact_email}.')
    raise ValueError


@input_error
def command_del_phone(user_data_list: list) -> str:
    """
    Remove contact phone from the phone book.
    """
    if not user_data_list[1]:
        raise KeyError

    user_message = get_message(user_data_list)  # type: str
    contact_name = get_contact_name(user_message)  # type: str

    if contact_name not in phonebook:
        raise KeyError

    phone_data = get_contact_phone(user_message)  # type: list
    record = phonebook[contact_name]  # type: Record

    if not phone_data:
        raise ValueError

    if record.phone is None:
        raise ValueError

    flag = False
    for idx, rec_phone in enumerate(record.phone):
        for phone in phone_data:
            if rec_phone.value == phone:
                record.delete_phone(phone_indx=idx)
                flag = True

    if flag:
        return contact_name

    print(f'{contact_name} contact does not have this phone {contact_phone}.')
    raise ValueError


def command_find(user_data_list: list):
    """
    Finds contact data based on the entered pattern.
    """
    iter_phonebook = phonebook.iterator()
    some_data = ' '.join(user_data_list[1:]).split()
    search_matching = []

    for _ in range(len(phonebook)):
        name, phones, birth, email, addr = next(iter_phonebook)
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
            search_matching.append((name, phones, birth, email, addr))

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
"add <new_name> <new_phone(s)> optionaly[<birthday>] optionaly[<email>]" 
                                        - adding a new contact.
"add address <name> <address>           - adding a contact's address.
"add birth <name> <birthday>            - adding a contact's birthday (01.01.2000).
"change <name> <old_phone> <new_phone>" - change the phone number of an existing contact.            
"birth <name>"                          - show how many days are left until the next birthday.
"del <name>"                            - remove contact from phonebook.
"show all"                              - show all saved contacts with phone numbers.
"phone <name>"                          - show phone numbers for an existing contact.
"find <pattern>"                        - finds contact data based on the entered pattern.
"good bye", "close", "exit"             - exit from the program. 
"add note <notice>"                     - adding a notice
"upd note <notice>"                     - update existing notice 
"remove note"                           - remove existing notice
"search note <notice>"                  - search notice
"search tag"                            - displays notice(s) according to defined tag
"sort <order>"                          - sort notice(s) according to defined tag ('asc'/'desc')
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
            if clear_data.isdigit() or not clear_data.isalnum():
                break
            name_data.append(data)

        contact_name = ' '.join(name_data)

        return contact_name

    else:
        raise IndexError


def get_contact_phone(some_string: str) -> list:
    """
    Getting the phone from the data transmitted by the user.
    """
    clear_data = normalize_msg(some_string)
    result = findall(r'(?:\+\d{2})?\d{3,4}\D?\d{3}\D?\d{3}', clear_data)
    return result


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
    phones = f' phones: {", ".join(record_data[1])}' if record_data[1] else ''
    birthday = f' | birthday: {record_data[2]}' if record_data[2] else ''
    emails = f' | email: {", ".join(record_data[3])}' if record_data[3] else ''
    address = f'\naddress: {record_data[4]}' if record_data[4] else ''

    result = f'{name}{phones}{birthday}{emails}{address}'

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
    
    NOTE_DB = 'note_db.bin'
    NOTE_PATH = CURRENT_DIR / NOTE_DB

    book = load_base(NOTE_PATH, dict=Notes())
    PROGRAM_CMD = {
        'add address': command_add_address,
        'add note': book.create_notice,
        'add birth': command_add_birth, 
        'add email': command_add_email,
        'add': command_add,
        'birth week': command_birth_week,
        'birth': command_birth,
        'change email': command_change_email,
        'change': command_change,
        'clean': command_clean,
        'del email': command_del_email,
        'del phone': command_del_phone,
        'del': command_del,
        'find': command_find,
        'phone': command_phone,
        'hello': command_hello,
        'help': command_help,
        'show all': command_show_all,
        'good bye': command_close_program,
        'close': command_close_program, 
        'exit': command_close_program,
        'upd note': book.upd_notice,
        'remove note': book.del_notice,
        'search note': book.search_notice,
        'search tag': book.search_tag,
        'sort': book.sorted
        }

    try:
        main()

    except KeyboardInterrupt:
        print('Good bye!\n')
        
    finally:
        print(dump_base(FILE_PATH, phonebook))
        dump_base(NOTE_PATH, book)
