import os
from datetime import datetime
import logging.config

import requests
from bs4 import BeautifulSoup
from CONSTANTS import HEADERS


def list_to_file(data, path):
    with open(path, 'w') as f:
        for line in data:
            f.write(f"{line}\n")


def get_soup(url):
    LOG = logging.getLogger(__name__)

    page = requests.get(url, headers=HEADERS)
    if page.status_code != 200:
        LOG.error(f'Error with request {url}. Got {page.status_code} {page.reason} instead of 200.')
    return BeautifulSoup(page.content, 'html.parser')


def string_to_date(string_date):
    try:
        date = datetime.strptime(string_date, "%B %d, %Y")
        return date
    except ValueError:
        LOG = logging.getLogger(__name__)
        LOG.error(f"Invalid date format. Expected format: 'Month DD, YYYY'. Got {string_date}")
        return ''


def string_short_month_to_date(string_date):
    try:
        date = datetime.strptime(string_date, "%b %d, %Y")
        return date
    except ValueError:
        LOG = logging.getLogger(__name__)
        LOG.error(f"Invalid date format. Expected format: 'Month DD, YYYY'. Got {string_date}")
        return ''
