import os
import sys
import requests
from bs4 import BeautifulSoup
from colorama import init, Fore


def parse_it(url):
    text = ''
    tags = ['p', 'a', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'ul', 'ol', 'li', 'span']
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    for t in soup.recursiveChildGenerator():
        if t.name in tags:
            if t.name == 'a':
                print(Fore.BLUE + t.text)
                text += t.text
            else:
                print(t.text)
                text += t.text
    return text


init()  # turns on colorama
directory = sys.argv[1]
if not os.path.exists(directory):
    os.mkdir(directory)
command = '.'
back_stack = []
ilbeback = 0
while command != 'exit':
    if command == 'back':
        if back_stack:
            back_stack.pop()
            command = back_stack.pop()
            ilbeback = 1
        else:
            command = '.'
            ilbeback = 0
    if command.find('.') == -1:
        print('Error: Incorrect URL')
    if command == os.path.exists(f'{directory}\\{command}'):
        link = command
        command = '.'
        with open(f'{directory}\\{link}', 'r') as file:
            print(file.read())
    if command.find('.') > 0 and command != '.':
        if command.find('https://') == 0:
            address = command
        else:
            address = 'https://' + command
        name = address[8:]
        with open(f'{directory}\\{name}', 'w') as file:
            parsed_text = parse_it(address)
            #print(parsed_text)
            if ilbeback == 0:
                back_stack.append(command)
            file.write(parsed_text)
            command = '.'
    command = input()