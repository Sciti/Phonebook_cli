import os
import csv

from enum import Enum



class States(Enum):
    MAIN_MENU = 'main_menu'
    ADD_RECORD = 'add_record'
    DELETE_RECORD = 'delete_record'
    CHANGE_RECORD = 'change_record'
    SEARCH_RECORD = 'search_records'


class Phonebook:
    def __init__(self, filename: str):

        # clears console for better visuals
        self._clear()

        self.current_state = States.MAIN_MENU

        self.columns = ['first_name', 'last_name', 'surname',
                       'company', 'work_number', 'personal_number']
        
        # made to simplify main cycle in run method
        self.main_menu = {
            '1': self.add_record,
            '2': self.delete_record,
            '3': self.change_record,
            '4': self.show_all_records,
            '5': self.search_records
        }
        

    def _clear(self):
        """
        Clears console
        """
        os.system('clear' if os.name == 'posix' else 'cls')


    def clear_data(self):
        """
        Clears phonebook data by recreating file
        """
        os.remove(self.filename)
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

        main_menu = [
            '1. Добавить запись',
            '2. Удалить запись',
            '3. Изменить запись',
            '4. Показать все записи',
            '5. Поиск по записям',
            'q. Выход'
        ]

        chosen = None
        while True:
            print('\n'.join(main_menu))

            chosen = input('>>> ')
            
            # avoid printing unnecessary information and quit
            if chosen == 'q':
                break
            
            # choises must be digits, except for quit
            if not chosen.isdigit():
                self._clear()
                print('Неккоректный ввод, выберите пункт меню из предложенных: ')
                continue
            
            try:
                self.main_menu[chosen]()
            except KeyError:
                self._clear()
                print('Неккоректный ввод, выберите пункт меню из предложенных: ')

        print('До свидания!')
        return
            
