import os
import requests
from bs4 import BeautifulSoup
from CONSTANTS import HEADERS


def list_to_file(data, path):
    with open(path, 'w') as f:
        for line in data:
            f.write(f"{line}\n")


def get_soup(url):
    page = requests.get(url, headers=HEADERS)
    return BeautifulSoup(page.content, 'html.parser')