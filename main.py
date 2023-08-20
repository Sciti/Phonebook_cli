import sys
import os

from phonebook import Phonebook


def process_file(
    columns: list,
    data_folder: str = 'data',
    filename: str = 'phonebook_data.csv'
) -> str:
    """
    Check for file extension, directory and existence 
    or return default filename
    """

    if not os.path.exists(data_folder):
        return 'dir_not_found'

    # add extension if provided without
    if not filename.split('.')[-1] == 'csv':
        filename += '.csv'

    file_path = os.path.join(data_folder, filename)
    # check if file exists, create if not
    if not os.path.exists(file_path):
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(';'.join(columns) + '\n')
        
    return file_path


def main():
    """
    This method stands for basic config, work with CLI arguments
    and execute Phonebook class
    """

    columns = ['ИД', 'Имя', 'Фамилия', 'Отчество',
               'Компания', 'Рабочий номер', 'Личный номер']
    
    args = sys.argv[1:]
    text = []
    file = process_file(columns=columns)

    
    # list of commands for future use
    commands = ['--help', '-h', '--file', '-f']

    # it only gets here if command is unknown
    if args and not any(arg in commands for arg in args):
        print('Неизвестная команда')
        return
    
    if any(arg in ['--help','-h'] for arg in args):
        text.extend([
            'Запуск без аргументов запустит программу со значениями по умолчанию',
            '--help -h\t\tОтобразить эту информацию',
            '--file -f [path\\to\\file]\t\tУказать файл справочника',
        ])
        print('\n'.join(text))
        return

    if any(arg in ['--file', '-f'] for arg in args):
        index = args.index('--file') if '--file' in args else args.index('-f')

        try:
            filepath = os.path.split(args[index + 1])
        except IndexError:
            print('Укажите имя файла')
            return

        file = process_file(
            columns=columns,
            data_folder=filepath[0],
            filename=filepath[1]
        )

        if file == 'dir_not_found':
            print('Директория не найдена. Возможно целевая папка не создана.')
            return

    Phonebook(file, columns).run()
          


if __name__ == '__main__':
    try:
        main()
    except (KeyboardInterrupt, SystemExit):
        print('До свидания!')