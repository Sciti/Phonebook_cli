import os
import csv

from enum import Enum, auto

class States(Enum):
    MAIN_MENU = auto()
    ADD_RECORD = auto()
    DELETE_RECORD = auto()
    CHANGE_RECORD = auto()
    SEARCH_RECORD = auto()


class Phonebook:
    def __init__(self, phonebook_filename: str):
        self._clear()

        self.phonebook_filename = phonebook_filename
        self._check_file()

        self.current_state = States.MAIN_MENU

        self.main_menu = {
            '1': self.add_record,
            '2': self.delete_record,
            '3': self.change_record,
            '4': self.show_all_records,
            '5': self.search_records
        }
        

    def _check_file(self):
        # get phonebook source file extension and check format
        self.extension = self.phonebook_filename.split('.')[-1]
        if not self.extension == 'csv':
            print('Неизвестный формат файла справочника, попробуйте другой')
            return

        # check if file exists, create if not
        if not os.path.exists(self.phonebook_filename):
            # determine columns to cleanup code a bit
            columns = ['first_name', 'last_name', 'surname',
                       'company', 'work_number', 'personal_number']
            with open(self.phonebook_filename, 'w') as f:
                f.write(';'.join(columns))


    def _clear(self):
        os.system('clear' if os.name == 'posix' else 'cls')


    def clear_data(self):
        os.remove(self.phonebook_filename)
        self._check_file()


    def add_record(self):
        self._clear()
        chosen = input('Добавление записи')
        


    def delete_record(self):
        self._clear()
        chosen = input('Удаление записи')


    def change_record(self):
        self._clear()
        chosen = input('Изменение записи')


    def show_all_records(self):
        self._clear()
        chosen = input('Показать все записи')


    def search_records(self):
        self._clear()
        chosen = input('Поиск по записям')


    def run(self):
        self._check_file()

        main_menu = [
            '1. Добавить запись',
            '2. Удалить запись',
            '3. Изменить запись',
            '4. Показать все записи',
            '5. Поиск по записям',
            'q. Выход'
        ]

        chosen = None
        while chosen != 'q':
            print('\n'.join(main_menu))

            chosen = input('>>> ')
            
            if chosen == 'q':
                break
            
            if not chosen.isdigit():
                self._clear()
                print('Неккоректный ввод, выберите пункт меню из предложенных: ')
                continue
            
            self.main_menu[chosen]()

        print('До свидания!')
        return
            
