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
        self.chosen_record = None

        self.page = 1
        self.pages = 1
        self.items_on_page = 9

        self.columns = columns
        

    def _clear(self):
        """Clears console"""
        os.system('clear' if os.name == 'posix' else 'cls')

    
    def get_records(self):
        """Returns list of dicts of records from file"""
        with open(self.filename, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f, delimiter=';')
            return list(reader)
        
    def write_records(self, records: list):
        """Rewrites all records to file with header"""
        with open(self.filename, 'w', encoding='utf-8', newline='') as f:
            writer = csv.DictWriter(
                f=f,
                fieldnames=self.columns,
                delimiter=';',
                lineterminator='\n'
            )
            writer.writeheader()
            writer.writerows(records)


    def pagination(self, data: list) -> list:
        """Returns paginated list of records according to current page"""
        if len(data) > self.items_on_page:
            self.pages = (len(data) - 1) // self.items_on_page + 1

        start_index = (self.page - 1) * self.items_on_page
        end_index = start_index + self.items_on_page

        return data[start_index:end_index]
    
    
    def reverse_readline(self, buf_size=8192):
        """
        A generator that returns the lines of a file in reverse order
        source: https://stackoverflow.com/questions/2301789/how-to-read-a-file-in-reverse-order
        """
        with open(self.filename, 'rb') as fh:
            segment = None
            offset = 0
            fh.seek(0, os.SEEK_END)
            file_size = remaining_size = fh.tell()
            while remaining_size > 0:
                offset = min(file_size, offset + buf_size)
                fh.seek(file_size - offset)
                buffer = fh.read(min(remaining_size, buf_size)).decode(encoding='utf-8')
                remaining_size -= buf_size
                lines = buffer.split('\n')
                # The first line of the buffer is probably not a complete line so
                # we'll save it and append it to the last line of the next buffer
                # we read
                if segment is not None:
                    # If the previous chunk starts right from the beginning of line
                    # do not concat the segment to the last line of new chunk.
                    # Instead, yield the segment first 
                    if buffer[-1] != '\n':
                        lines[-1] += segment
                    else:
                        yield segment
                segment = lines[0]
                for index in range(len(lines) - 1, 0, -1):
                    if lines[index]:
                        yield lines[index]
            # Don't yield None if the file was empty
            if segment is not None:
                yield segment


    def add_record(self):
        """
        Record adding logic, preforms simple input validation and writes to file
        """
        self._clear()

        text = ['- Добавление записи -', 
                'Для выхода в главное меню введите "q"',
                'Имя может содержать только буквы, тире и двойные скобки. '
                'Отчество можно оставить пустым',
                'Номер должен начинаться с +, 7 или 8\n'
        ]
        
        print('\n'.join(text))

        data = {}
        user_input = None
        last_id = None

        # get last line for id
        for line in self.reverse_readline():
            # in case file has empty lines
            try:
                last_id = int(line.split(';')[0])
            except ValueError:
                continue
            
            break
        
        # columns stands for steps when adding new records
        for step in self.columns:
            text.append(f"{step}: ")
            last_id += 1

            # automatically assign ID
            if step == 'ИД':
                text[-1] += str(last_id)
                data[step] = last_id
                continue

            # break from this for cycle into main menu
            if user_input == 'q':
                break

            # check variable for input validation
            check = True
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
                    if user_input == '':
                        break

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
        with open(self.filename, 'a', encoding='utf-8', newline='') as f:
            writer = csv.DictWriter(
                f=f,
                fieldnames=self.columns,
                delimiter=';',
                lineterminator='\n'
            )
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
        number must start with +, 7 or 8 and can contain other symbols,
        e.g. +7(123)456-78-90

        Returns:
         - digits from number if number is valid
         - False if number is not valid
        """
        allowed = ['+', '7', '8']
        if any(number.startswith(symb) for symb in allowed):
            digits = re.sub(r'\D', '', number)
            return digits
        return False


    def delete_record(self):
        """Deletes record from file by it's ID"""

        # indicators to print success or not found message after clearing console
        success_indicator = False
        not_found = False

        while True:
            self._clear()
            
            print('\n'.join(
                [
                    '-- Удаление записи --',
                    'Для удаления записи отправьте её ИД',
                    'Для выхода в главное меню введите "q"'
                ]
            ))

            if success_indicator:
                print(f'Запись удалена!')
                success_indicator = False
            elif not_found:
                print('Запись не найдена')
                not_found = False

            user_input = input('>>> ')

            if user_input == 'q':
                break

            
            if not user_input.isdigit():
                continue

            records = self.get_records()
            
            # iterate over records copy but modify original
            for record in records.copy():
                if record['ИД'] == user_input:

                    # additional check before deleting
                    delete_input = input(
                        'Подтвердите удаление[y/n]:\n'
                        f'ФИО: {record["Имя"]} {record["Фамилия"]} {record["Отчество"]}\n'
                        f'Компания: {record["Компания"]}\n'
                        f'Рабочий номер: {record["Рабочий номер"]}, '
                        f'Личный номер: {record["Личный номер"]}\n'
                        '>>> '
                    )

                    if delete_input.lower() == 'y':
                        records.remove(record)
                        self.write_records(records)
                        success_indicator = True
                    else:
                        success_indicator = False
                        continue
                else:
                    not_found = True
                    continue

            continue



    def show_records(self, records: list = None):
        """
        Prints list of all records or print passed records
        
        :param records: list of records to show, None(default) for all
        """
        while True:
            if not records:
                records = self.get_records()

            self._clear()
            text = [
                '-- Список записей --',
                'Для выхода в главное меню введите "q"',
                'Для перехода на другую страницу введите "<"\\"p" или ">"\\"n"',
                'Отправьте номер записи для изменения\n'
            ]

            page_records = self.pagination(list(records))
            
            # generate printed message
            for row in page_records:
                text.extend([
                    f"-- {row['ИД']} -- ",
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
            
            # page changing handlers
            if user_input in ['<', 'p']:
                if self.page > 1:
                    self.page -= 1
                    continue

            if user_input in ['>', 'n']:
                if self.page < self.pages:
                    self.page += 1
                    continue

            # goto edit if record selected
            if user_input.isdigit():
                self.chosen_record = int(user_input)
                self.edit_menu(records)
                continue
            
    
    def edit_menu(self, records: list, record_number: int = None):
        """
        Entrypoint to record editing menu

        :param records: list of records to update records printed after edit
        :param record_number: record ID to edit
        """

        edit_menu = {
            '1': self.edit_name,
            '2': self.edit_company,
            '3': self.edit_phone
        }

        if not record_number:
            record_number = self.chosen_record

        while True:
            self._clear()

            print('\n'.join(
                [
                    f'-- Редактирование записи {record_number} --',
                    '1. Изменить ФИО',
                    '2. Изменить компанию',
                    '3. Изменить номер телефона',
                    'Для возврата назад введите "q"',
                ]
            ))

            user_input = input('>>> ')

            if user_input == 'q':
                break

            if user_input in ['1', '2', '3']:
                edit_menu[user_input](record_number, records)
                break

    def edit_name(self, record_number: int, records: list):
        """
        edit first name, last name and surname
        
        :param record_number: record ID to edit
        :param records: list of records to update
        """
        self._clear()
        
        print('Введите новое ФИО, что бы пропустить шаг поле можно оставить пустым\n'
              'Для возврата назад введите "q"')

        
        
        steps = ['Имя', 'Фамилия', 'Отчество']
        new_data = []
        for step in steps:
            while True:
                user_input = input(f'{step} > ')

                if user_input == 'q' or not user_input:
                    break

                name = self._check_name(user_input)

                if not name:
                    print('Некорректный ввод, попробуйте еще раз')
                    continue
                break
            
            new_data.append(name)

        for record in records:
            if record['ИД'] == str(record_number):
                record['Имя'], record['Фамилия'], record['Отчество'] = new_data
                
        self.write_records(records)


    def edit_company(self, record_number: int, records: list):
        """
        edit company name

        :param record_number: record ID to edit
        :param records: list of records to update
        """
        self._clear()

        print('Введите новое название компании, что бы вернуться назад введите "q"')
        
        while True:
            user_input = input('Название компании > ')

            if user_input == 'q':
                break

            if not user_input:
                print('Некорректный ввод, попробуйте еще раз')
                continue
            break

        for record in records:
            if record['ИД'] == str(record_number):
                record['Компания'] = user_input
        
        self.write_records(records)


    def edit_phone(self, record_number: int, records: list):
        """
        edit phone number

        :param record_number: record ID to edit
        :param records: list of records to update
        """
        self._clear()

        print('Введите новый номер телефона, что бы пропустить шаг поле можно оставить пустым\n'
              'Для возврата назад введите "q"')
        
        steps = ['Рабочий номер', 'Личный номер']
        new_data = []
        for step in steps:
            while True:
                user_input = input(f'{step} > ')
                
                if user_input == 'q' or not user_input:
                    break
                
                number = self._check_number(user_input)
                if not number:
                    print('Некорректный ввод, попробуйте еще раз')
                    continue

                break

            new_data.append(number)

        for record in records:
            if record['ИД'] == str(record_number):
                record['Рабочий номер'], record['Личный номер'] = new_data
    
        self.write_records(records)


    def search_records(self, search_term: str = None):
        """
        performs simple search on records by any field

        :param search_term: search term for other methods to use
        """
        # input validation check
        check = True
        not_found = False
        while True:
            self._clear()

            print('\n'.join(
                [
                    '-- Поиск по записям --',
                    'Напишите условие для поиска, '
                    'если условий несколько введите их через пробел',
                    'Для возврата назад введите "q"',
                ]
            ))

            if not check:
                print('Некорректный ввод, попробуйте еще раз')
                continue
            elif not_found:
                print('Ничего не найдено')
                not_found = False
            
            if search_term:
                user_input = search_term
            else:
                user_input = input('>>> ')

            if user_input == 'q':
                break

            if not user_input:
                check = False
                continue
            
            # main search logic, looks for matches in lowercase
            search_result = []
            with open(self.filename, 'r', encoding='utf-8') as f:
                data = csv.DictReader(f, delimiter=';')
                for record in data:
                    values = [value.lower() for value in record.values()]
                    search_terms = user_input.lower().split()
                    if all(term in str(values) for term in search_terms):
                        search_result.append(record)

            if not search_result:
                not_found = True
                continue
            
            break

        self.show_records(search_result)


    def generate_data(self):
        """
        simple generator for other methods tests
        """
        while True:
            self._clear()

            user_input = input('Количество записей: ')

            if user_input == 'q':
                break

            if user_input.isdigit():
                with open(self.filename, 'a', encoding='utf-8') as f:
                    writer = csv.writer(f, delimiter=';', lineterminator='\n')
                    for i in range(int(user_input)):
                        i += 1
                        row = [i, ]
                        for column in self.columns[1:]:
                            row.append(f'{column}{i}')
                        writer.writerow(row)
                break
            else:
                print('Неккоректный ввод, введите целое число')
                continue
        

    def run(self):
        """
        method to print main menu, all methods come back here when they finish working
        """

        # made to simplify selection
        main_menu = {
            '1': self.add_record,
            '2': self.delete_record,
            '3': self.show_records,
            '4': self.search_records,
            '5': self.generate_data
        }

        while True:
            self._clear()

            print('\n'.join(
                [
                    '-- Главное меню --',
                    '1. Добавить запись',
                    '2. Удалить запись',
                    '3. Показать все записи',
                    '4. Поиск по записям',
                    '5. Сгенерировать данные',
                    'q. Выход',
                    'Для изменения записи найдите её через поиск или '
                    'выберите при отображении всех записей'
                ]
            ))

            user_input = input('>>> ')
            
            # avoid printing unnecessary information and quit
            if user_input == 'q':
                break
            
            # choises must be digits, except for quit
            if not user_input.isdigit():
                self._clear()
                print('Неккоректный ввод, выберите пункт меню из предложенных: ')
                continue
            
            try:
                main_menu[user_input]()
            except KeyError:
                self._clear()
                print('Неккоректный ввод, выберите пункт меню из предложенных: ')

        print('До свидания!')
        return
            
