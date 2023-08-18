import sys
import os
from phonebook import Phonebook


def main():
    args = sys.argv[1:]
    text = []
    filename = 'phonebook.csv'
    
    # create list of commands for future use
    commands = [
        '--help', '-h', '--filename', '-f', '--clear', '-c', '--run', '-r'
    ]

    if any(arg in ['--help','-h'] for arg in args):
        text.extend([
            'Справка по коммандам:',
            '--help -h\t\tОтобразить эту информацию',
            '--filename -f [filename]\t\tУказать файл справочника',
            '--clear -c [filename]\t\tОчистить справочник',
            '--run -r\t\tЗапустить программу интерактивно'
        ])
        print('\n'.join(text))
        return

    if any(arg in ['--filename', '-f'] for arg in args):
        index = args.index('--filename') if '--filename' in args else args.index('-f')
        filename = args[index + 1]
        
        
    if any(arg in ['--clear', '-c'] for arg in args):
        index = args.index('--clear') if '--clear' in args else args.index('-c')
        filename = args[index + 1]
        if not os.path.exists(filename):
            print(f'Файл {filename} не найден')
            return 
        
        answer = input('Вы уверены, что хотите очистить справочник? (y/n)')
        if answer.lower() == 'y':
            Phonebook(filename).clear_data()
            return
        
        print('Действие отменено')

    if not args or any(arg in ['--run', '-r'] for arg in args):
        phonebook = Phonebook(filename)
        phonebook.run()
        return

    if not any(arg in commands for arg in args):
        print('Неизвестная команда')  

                


if __name__ == '__main__':
    main()