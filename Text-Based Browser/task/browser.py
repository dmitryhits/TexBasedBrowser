import argparse
from pathlib import Path
import requests
from bs4 import BeautifulSoup
from colorama import Fore


class Browser:
    def __init__(self, websites):
        self.history = []
        self.saved_websites = {}
        self.websites = websites
        self.current_index = -1
        self.current_page = ''

    def process_input(self, user_input):
        if user_input == 'exit':
            exit()
        elif user_input == 'back' and len(self.history) > 1:
            self.back()
        elif user_input in self.saved_websites.keys():
            self.print_from_file(user_input)
        elif '.' not in user_input:
            print("Error: Incorrect URL")
        else:
            if user_input.startswith('https://'):
                # self.print_from_cache(user_input)
                address = user_input
            else:
                address = 'https://' + user_input
            self.retrieve_page(address)
            self.save_page(address)

    def print_from_cache(self, user_input):
        print(websites[user_input])

    def print_from_file(self, user_input):
        with open(self.saved_websites[user_input]) as f:
            print(f.read())

    def save_page(self, url):
        r_dot_index = url.rfind('.')
        file_name = url[:r_dot_index].lstrip('https://')
        file_path = store_directory.joinpath(file_name)
        self.saved_websites.setdefault(file_name, file_path)
        file_path.write_text(self.current_page)
        self.history.append(file_name)

    def back(self):
        if len(self.history) > abs(self.current_index):
            self.current_index -= 1
        self.print_from_file(self.history[self.current_index])

    def retrieve_page(self, address):
        user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) " \
                     "Chrome/70.0.3538.77 Safari/537.36"
        r = requests.get(address, headers={'User-Agent': user_agent})
        if r and r.status_code == 200:
            # self.current_page = r.text
            soup = BeautifulSoup(r.content, 'html.parser')
            body = soup.find('body')
            links = [el.get_text().strip() for el in body.find_all('a') if el.get_text().strip()]
            page = body.get_text()
            strips = []
            for link in links:
                i = page.find(link) + len(link)
                strips.append(page[:i].replace(link, '\n' + Fore.BLUE + link + Fore.RESET, 1))
                page = page[i:]

            self.current_page = ''.join(strips)
            print(self.current_page)


parser = argparse.ArgumentParser()
parser.add_argument('dir')
args = parser.parse_args()
store_directory = Path(args.dir)
if not store_directory.exists():
    store_directory.mkdir()

nytimes_com = '''
This New Liquid Is Magnetic, and Mesmerizing

Scientists have created “soft” magnets that can flow 
and change shape, and that could be a boon to medicine 
and robotics. (Source: New York Times)


Most Wikipedia Profiles Are of Men. This Scientist Is Changing That.

Jessica Wade has added nearly 700 Wikipedia biographies for
 important female and minority scientists in less than two 
 years.

'''

bloomberg_com = '''
The Space Race: From Apollo 11 to Elon Musk

It's 50 years since the world was gripped by historic images
 of Apollo 11, and Neil Armstrong -- the first man to walk 
 on the moon. It was the height of the Cold War, and the charts
 were filled with David Bowie's Space Oddity, and Creedence's 
 Bad Moon Rising. The world is a very different place than 
 it was 5 decades ago. But how has the space race changed since
 the summer of '69? (Source: Bloomberg)


Twitter CEO Jack Dorsey Gives Talk at Apple Headquarters

Twitter and Square Chief Executive Officer Jack Dorsey 
 addressed Apple Inc. employees at the iPhone maker’s headquarters
 Tuesday, a signal of the strong ties between the Silicon Valley giants.
'''
websites = {"nytimes.com": nytimes_com,
            "bloomberg.com": bloomberg_com}

files = {}

if __name__ == '__main__':
    webbrowser = Browser(websites)
    while True:
        u_input = input()
        webbrowser.process_input(u_input)


