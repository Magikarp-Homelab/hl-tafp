import requests
from bs4 import BeautifulSoup
from datetime import datetime

from CONSTANTS import URL_EVENTLIST
from CONSTANTS import HEADERS


def get_eventids_from_site():
    page = requests.get(URL_EVENTLIST, headers=HEADERS)
    soup = BeautifulSoup(page.content, 'html.parser')

    link_elements = soup.findAll('i', 'b-statistics__table-content')
    link_ids = []

    for le in link_elements:
        event_id, event_date = __parse_id_and_date_from_parent(le)
        if event_date > datetime.now():
            continue
        link_ids.append(event_id)

def __parse_id_and_date_from_parent(parent_element):
    parsed_id = parent_element.contents[1].attrs['href'].strip().split('/')[-1]
    parsed_date = parent_element.contents[3].text.strip()
    return parsed_id, __string_to_date(parsed_date)

def __string_to_date(string_date):
    try:
        date = datetime.strptime(string_date, "%B %d, %Y")
        return date
    except ValueError:
        raise ValueError("Invalid date format. Expected format: 'Month DD, YYYY'")