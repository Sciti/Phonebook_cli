from typing import Union

import os
import csv
import re


class Phonebook:
    def __init__(self, filename: str, columns: list):
        """
        Main logic class, allows to work with phonebook

        :param filename: path to phonebook file
        :param columns: list of columns in file
        """

        # clears console for better visuals
        self._clear()

        self.filename = filename
        self.record_check = False

        self.page = 1
        self.pages = 1
        self.items_on_page = 9

        self.columns = columns
        
        # made  to simplify main cycle in run method
        self.main_menu = {
            '1': self.add_record,
            '2': self.delete_record,
            '3': self.change_record,
            '4': self.show_all_records,
            '5': self.search_records,
            '6': self.generate_data
        }
        

    def _clear(self):
        """
        Clears console
        """
        os.system('clear' if os.name == 'posix' else 'cls')


    def pagination(self, data: list) -> list:
        
        if len(data) > self.items_on_page:
            self.pages = (len(data) - 1) // self.items_on_page + 1

        start_index = (self.page - 1) * self.items_on_page
        end_index = start_index + self.items_on_page

        return data[start_index:end_index]
    
    
    def read_last_line(self):
        with open(self.filename, 'r', encoding='utf-8') as f:
            # move to EoF
            f.seek(0, 2)
            
            # get end position of last line
            pos = f.tell()
            while pos > 0:
                # move one symbol towards start of file
                pos -= 1
                f.seek(pos, 0)

                # read this symbol
                char = f.read(1)

                # stop iterating when new line symbol found
                if char == '\n':
                    last_line = f.readline().strip()
                    if not last_line:
                        continue
                    else:
                        return last_line

            # last_line = f.readline()
            # return last_line.strip()

    def add_record(self):
        """
        Record adding logic, preforms simple input validation and writes to file
        """
        self._clear()

        text = ['- Добавление записи -', 
                'Для выхода в главное меню введите "q"',
                'Имя может содержать только буквы, тире и двойные скобки',
                'Номер должен начинаться с +7 или 8\n'
        ]
        
        print('\n'.join(text))

        data = {}
        user_input = None
        
        # columns stands for steps when adding new records
        for step in self.columns:
            text.append(f"{step}: ")

            # check for valid input
            check = True

            # break from this for cycle into main menu
            if user_input == 'q':
                break

            while True:

                # print out incorrect input message after clear
                if not check:
                    print('Некорректный ввод, попробуйте еще раз')
                    
                user_input = input(f'{step} > ')
            
                # break from this cycle and prevent executing unnecessary code
                if user_input == 'q':
                    break
                
                # for numbers input
                if 'номер' in step:
                    user_input = self._check_number(user_input)
                    if not user_input:
                        check = False
                        continue

                # for strings input
                else:
                    user_input = self._check_name(user_input)
                    if not user_input:
                        check = False
                        continue

                # all checks passed, data is valid
                check = True
                text[-1] += user_input
                data[step] = user_input

                # clear console and reprint text for better visuals
                self._clear()
                print('\n'.join(text))
                break
        
        # when data collection done, write it to file
        with open(self.filename, 'a', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=self.columns, delimiter=';')
            writer.writerow(data)

    
    def _check_name(self, name: str) -> bool:
        """
        helper function, preforms simple string input validation
        string can contain only RU\EN letters, hypens and double quotes

        Returns:
         - passed string if string is valid
         - False if string is not valid 
        """
        pattern = r'^[a-zA-Zа-яА-Я"\s-]*$'
        if re.search(pattern, name):
            return name
        return False
        
    
    def _check_number(self, number: str) -> Union[str, bool]:
        """
        helper function, preforms simple number input validation
        number must start with +7 or 8 and can contain other symbols,
        e.g. +7(123)456-78-90

        Returns:
         - digits from number if number is valid
         - False if number is not valid
        """
        allowed = ['+7', '8']
        if any(number.startswith(symb) for symb in allowed):
            digits = re.sub(r'\D', '', number)
            return digits
        return False


    def delete_record(self):
        self._clear()

        with open(self.filename, 'r', encoding='utf-8') as f:
            data = csv.DictReader(f, delimiter=';')
            
        # with open(self.filename, 'w', encoding='utf-8') as f:
        #     while True:


                
        # input()


    def change_record(self):
        self._clear()
        print(self.read_last_line())
        input()


    def show_all_records(self):
        self._clear()
        

        with open(self.filename, 'r', encoding='utf-8') as f:
            data = csv.DictReader(f, delimiter=';')
            all_records = list(data)

        while True:
            self._clear()
            text = [
                '-- Список записей --',
                'Для выхода в главное меню введите "q"',
                'Для перехода на другую страницу введите "<"\\"p" или ">"\\"n"',
                'Отправьте номер записи для изменения или удаления\n'
            ]
            # print('\n'.join(text))

            page_records = self.pagination(list(all_records))
            for i, row in enumerate(page_records, 1):
                text.extend([
                    f"-- {i} -- ",
                    f"ФИО: {row['Имя']} {row['Фамилия']} {row['Отчество']}",
                    f"Компания: {row['Компания']}",
                    f"Рабочий номер: {row['Рабочий номер']}, "
                    f"Личный номер: {row['Личный номер']}",
                ])
            
            text.append(f'\nСтраница: {self.page}/{self.pages}')
            print('\n'.join(text))

            user_input = input('>>> ')

            if user_input == 'q':
                break

            if user_input in ['<', 'p']:
                if self.page > 1:
                    self.page -= 1
                    continue

            if user_input in ['>', 'n']:
                if self.page < self.pages:
                    self.page += 1
                    continue

            if user_input.isdigit():
                self.chosen_record = int(user_input)
                break
            


    def search_records(self):
        self._clear()
        chosen = input('Поиск по записям')


    def generate_data(self):
        while True:
            self._clear()

            user_input = input('Количество записей: ')

            if user_input == 'q':
                break

            if user_input.isdigit():
                with open(self.filename, 'a', encoding='utf-8') as f:
                    writer = csv.writer(f, delimiter=';', lineterminator='\n')
                    for i in range(int(user_input)):
                        writer.writerow([
                            f'Имя{i}', f'Фамилия{i}', f'Отчество{i}',
                            f'Компания{i}', f'Рабочий номер{i}', f'Личный номер{i}'
                        ])
                break
            else:
                print('Неккоректный ввод, введите целое число')
                continue
        

    def run(self):

        main_menu = [
            '1. Добавить запись',
            '2. Удалить запись',
            '3. Изменить запись',
            '4. Показать все записи',
            '5. Поиск по записям',
            '6. Сгенерировать данные',
            'q. Выход'
        ]

        chosen = None
        while True:
            self._clear()

            if self.record_check:
                print('Записано!')

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
            
