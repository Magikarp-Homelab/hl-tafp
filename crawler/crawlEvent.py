from util import util
from CONSTANTS import URL_EVENT


def get_fightid_from_event(event_id: str):
    soup = util.get_soup(URL_EVENT + event_id)

    link_elements = soup.findAll('a', 'b-flag b-flag_style_green')
    link_ids = []

    for le in link_elements:
        event_id = __parse_id_from_element(le)
        link_ids.append(event_id)

    return link_ids


def __parse_id_from_element(element):
    return element.attrs['href'].strip().split('/')[-1]
