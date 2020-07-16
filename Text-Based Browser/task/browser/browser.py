import sys
import os
from collections import deque
import requests
from bs4 import BeautifulSoup
from colorama import init, Fore


def open_file(filename):
    os.makedirs(os.path.dirname(filename), exist_ok=True)


def check_url(url):
    if '.' in url:
        return True
    else:
        return False


def directory_walk(path, entry_name):
    for folderName, subfolders, filenames in os.walk(path):
        # print('The current folder is ' + folderName)

        # for subfolder in subfolders:
        #     print('SUBFOLDER OF ' + folderName + ': ' + subfolder)

        for filename in filenames:
            # print('FILE INSIDE ' + folderName + ': ' + filename)
            if entry_name == filename:
                # print("entry_name", entry_name)
                with open(path + entry_name, "r") as file_load:
                    for line in file_load:
                        print(line, end='')
                    return True
    return False


def load_history2(path, entry_name, history):
    if not directory_walk(path, entry_name):
        print("Error: Incorrect URL")
    else:
        history.append(entry_name)


def open_url2(url, url_list, path, history, previous_entry):
    url = url.split('.')
    if url[0] in list_websites:
        print(list_websites[url[0]])
        history.append(
            previous_entry)  # potentialy add condition if string not empty as first str is empty, but still be added
    with open(path + url[0], "w") as file_load:
        if url[0] not in url_list:
            for web in list_websites:
                if url[0] in web:
                    file_load.write(list_websites[web])
            url_list.append(url[0])
            return url[0]


def print_history(path, history):
    if len(history) != 0:
        directory_walk(path, history.pop())


def check_https(url):
    if "https://" in url:
        return True
    else:
        False


def parse_print_write_request(request, file_save):
    text = ''
    tags = ['p', 'a', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'ul', 'ol', 'li', 'span']
    # page = requests.get(url)
    soup = BeautifulSoup(request.content, 'html.parser')
    for t in soup.recursiveChildGenerator():
        if t.name in tags:
            if t.name == "a":
                text += t.text
                print(Fore.BLUE + t.text)
            else:
                print(t.text)
    file_save.write(text)

    return text


def send_request(url, current_page, url_list, path, history):
    #print("url", url)
    r = requests.get(url)
    #print(r.text)
    if r:
        url = url.split('.')
        history.append(current_page)
        with open(path + url[1], "w") as file_save:
            if url[1] not in url_list:
                parsed_text = parse_print_write_request(r, file_save)
                url_list.append(url[1])

    return url


def take_input(path, url_list, history):
    print("Type in url")
    current_page = ""
    while True:
        url = input()
        if check_url(url):
            # check if has https if not add
            if not check_https(url):
                url = "https://" + url
            current_page = send_request(url, current_page, url_list, path, history)
        elif url == "back":
            # keep it for that moment
            print_history(path, history)
        else:
            # keep it for that moment
            load_history2(path, url, history)  # add to the history url if valid
            if url == "exit":
                sys.exit()


init()  #turns on colorama
url_list = []
history = deque()
args = sys.argv
directory = args[1]
# dirname = os.path.dirname(__file__)
dirname = "C:\\Users\\piotr\\PycharmProjects\\Text-Based Browser\\Text-Based Browser\\task"
path = dirname + "\\" + directory + "\\"
open_file(path)
take_input(path, url_list, history)
