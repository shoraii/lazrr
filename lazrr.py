import argparse
import colorama
from colorama import Fore, Back, Style
from gforms import Form
from gforms.elements import default_callback, Short, Paragraph
from os.path import exists
from random import choice
from math import inf
import time
import threading
import string

responses = []
total_filled = 0

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

def thread_fill(form, cooldown, fuzzed=False, limit=inf):
    global total_filled
    while total_filled < limit:
        try:
            form.fill(fillform)
            form.submit()
        except Exception as e:
            print(Fore.RED + f'Failed to fill: {str(e)}')
        else:
            total_filled += 1
            print(Fore.CYAN + f'Filled {total_filled} forms!', end='\r')
        time.sleep(cooldown)
        if fuzzed:
            break

def main(url, threads=4, fuzzed=False, cooldown=0.0, limit=inf):
    global total_filled
    if 'docs.google.com/forms/d/e/' not in url or '/viewform' not in url:
        print(Fore.BLACK + Back.RED + Style.BRIGHT + f'Invalid url format!')
        print(Fore.RED + 'Correct url format: https://docs.google.com/forms/d/e/.../viewform')
        return
    form = Form(url)
    form.load()
    print(Fore.BLACK + Back.CYAN + Style.BRIGHT + f'Loaded form {form.title}')
    if fuzzed:
        thread_fill(form, cooldown, fuzzed, limit)
    
    for _ in range(threads):
        threading.Thread(target=thread_fill, args=(form, cooldown, False, limit)).start()

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
    parser.add_argument(
        '-t',
        default=4,
        required=False,
        action='store',
        help='Number of threads (4 by default)')
    parser.add_argument(
        '--fuzzed',
        default=False,
        required=False,
        action='store',
        help='Set to True if you are using libfuzzer')
    parser.add_argument(
        '--cooldown',
        default=0.0,
        required=False,
        action='store',
        help='Set cooldown for form filling')
    parser.add_argument(
        '-f',
        default=inf,
        required=False,
        action='store',
        help='Set the limit of filled forms')
    args = parser.parse_args()
    args.t = int(args.t)
    args.cooldown = float(args.cooldown)
    args.f = float(args.f)
    main(args.url, args.t, args.fuzzed, args.cooldown, args.f)
