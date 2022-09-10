from phonebook import AddressBook

from pathlib import Path
from pickle import load, dump


def dump_base(file_path: Path, db: dict) -> str:

    if file_path.is_file():

        with open(file_path, 'wb') as fh:
            dump(db, fh)

        return 'Phonebook saved.'

    return 'Phonebook don`t saved.'


def load_base(file_path: Path) -> AddressBook:

    if file_path.is_file():

        with open(file_path, 'rb') as fh:
            phonebook = load(fh)

        return phonebook

    else:
        return AddressBook()


if __name__ == '__main__':

    current_dir = Path(__file__).parent
    file_db = 'phone_db.bin'
    file_path = current_dir / file_db
    print('current_dir: ', current_dir)
    print('file_path: ', file_path)

    phonebook = load_base(file_path)
    print(type(phonebook))
    print(phonebook.items())

    print(dump_base(file_path, phonebook))
