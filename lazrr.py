import argparse
import colorama
from colorama import Fore, Back, Style
from gforms import Form
from gforms.elements import default_callback, Short, Paragraph
from os.path import exists
from random import choice
import time
import string

responses = []

def randstr(size):
    return ''.join(choice(string.ascii_letters + string.digits) for _ in range(size))

def fillform(elem, page_index, elem_index):
    result = None
    try:
        result = default_callback(elem, page_index, elem_index)
    except:
        if isinstance(elem, Short) or isinstance(elem, Paragraph):
            result = choice(responses)
        else:
            raise NotImplementedError(f'Cannot fill {elem._type_str()}')
    return result

def main(url):
    if 'docs.google.com/forms/d/e/' or '/viewform' not in url:
        print(Fore.BLACK + Back.RED + Style.BRIGHT + f'Invalid url format!')
        print(Fore.RED + 'Correct url format: https://docs.google.com/forms/d/e/.../viewform')
        return
    form = Form(url)
    form.load()
    print(Fore.BLACK + Back.CYAN + Style.BRIGHT + f'Loaded form {form.title}')
    filled = 0
    while True:
        try:
            form.fill(fillform)
            form.submit()
        except Exception as e:
            print(Fore.RED + f'Failed to fill: {str(e)}')
        else:
            filled += 1
            print(Fore.CYAN + f'Filled {filled} forms!')
        time.sleep(0.1)

if __name__ == '__main__':
    colorama.init(autoreset=True)
    if not exists('responses.txt'):
        responses = [randstr(10) for _ in range(10)]
    else:
        with open('responses.txt', 'r') as rfile:
            responses = rfile.readlines()
            responses = [resp.strip() for resp in responses]
    parser = argparse.ArgumentParser(description='lazrr: Google Forms autofill script')
    parser.add_argument(
        'url',
        action='store',
        help='url (https://docs.google.com/forms/d/e/.../viewform)')
    args = parser.parse_args()
    main(args.url)
