import sys
import os

from phonebook import Phonebook


def process_file(data_folder: str = 'data', filename: str = 'phonebook_data.csv') -> str:
    """
    Check for file extension, directory and existence 
    or return default filename
    """
    file_path = os.path.join(data_folder, filename)

    if not os.path.exists(data_folder):
        return 'dir_not_found'

    # add extension if provided without
    if not filename.split('.')[-1] == 'csv':
        filename += '.csv'

    # check if file exists, create if not
    if not os.path.exists(file_path):
        columns = ['first_name', 'last_name', 'surname',
                   'company', 'work_number', 'personal_number']
        
        with open(file_path, 'w') as f:
            f.write(';'.join(columns))
        
    return filename


def main():
    """
    This method stands for basic config, work with CLI arguments
    and execute Phonebook class
    """
    # variables declaration
    args = sys.argv[1:]
    text = []
    filename = process_file()
    
    
    # list of commands for future use
    commands = [
        '--help', '-h', '--file', '-f'
    ]

    # it only gets here if command is unknown
    if args and not any(arg in commands for arg in args):
        print('Неизвестная команда')
        return
    
    # prints help, text list for better code readability
    if any(arg in ['--help','-h'] for arg in args):
        text.extend([
            'Запуск без аргументов запустит программу со значениями по умолчанию',
            '--help -h\t\tОтобразить эту информацию',
            '--file -f [path\\to\\file]\t\tУказать файл справочника',
        ])
        print('\n'.join(text))
        return

    # check for filename argument, rewrite filename variable if exists
    if any(arg in ['--file', '-f'] for arg in args):
        index = args.index('--file') if '--file' in args else args.index('-f')

        try:
            filepath = os.path.split(args[index + 1])
        except IndexError:
            print('Укажите имя файла')
            return

        filename = process_file(data_folder=filepath[0], filename=filepath[1])

        if filename == 'dir_not_found':
            print('Директория не найдена. Возможно целевая папка не создана.')
            return

    phonebook = Phonebook(filename)
    phonebook.run()                


if __name__ == '__main__':
    try:
        main()
    except (KeyboardInterrupt, SystemExit):
        print('До свидания!')