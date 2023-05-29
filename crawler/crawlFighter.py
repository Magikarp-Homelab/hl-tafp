import logging.config

from crawler.dataclasses.Fighter import Fighter
from util import util
from util import fighter_util
from CONSTANTS import URL_FIGHTER
from CONSTANTS import FEET_TO_CM_RATION
from CONSTANTS import INCH_TO_CM_RATION
from CONSTANTS import POUNDS_TO_KG_RATIO


def crawl_fighter_with_id(fighter_id):
    LOG = logging.getLogger(__name__)

    if fighter_util.check_fighter_id_in_db(fighter_id):
        LOG.debug(f'Skipping fighter {fighter_id}. Already in DB.')
        return

    LOG.debug(f'Crawling fighter {fighter_id}.')

    soup = util.get_soup(URL_FIGHTER + fighter_id)

    fighter = Fighter(id=fighter_id)

    fighter.firstname, fighter.lastname = __parse_name_from_soup(soup)
    fighter.record_win, fighter.record_loss, fighter.record_nc = __parse_record_from_soup(soup)
    fighter.height, fighter.weight, fighter.reach, fighter.stance, fighter.dob = __parse_fighter_details_from_soup(soup)

    LOG.debug(f'Writing fighter {fighter_id} to DB.')
    fighter_util.persist_fighter(fighter)


def __parse_name_from_soup(soup):
    element = soup.find('span', 'b-content__title-highlight')
    txt = element.text.strip().split(' ')
    if len(txt) == 2:
        return txt[0], txt[1]
    else:
        return '', txt[0]


def __parse_record_from_soup(soup):
    element = soup.find('span', 'b-content__title-record')
    txt = element.text.strip().split(' ')
    record_lst = txt[1].split('-')
    return record_lst[0], record_lst[1], record_lst[2]


def __parse_fighter_details_from_soup(soup):
    top_list = soup.find('ul', 'b-list__box-list')
    elements = top_list.findAll('li')
    height = __parse_details_height(elements[0])
    weight = __parse_details_weight(elements[1])
    reach = __parse_details_reach(elements[2])
    stance = __parse_details_stance(elements[3])
    dob = __parse_details_dob(elements[4])

    return height, weight, reach, stance, dob


def __parse_details_height(element):
    text = element.text.strip().split(':')[-1].strip().split(' ')
    if len(text) < 2:
        return 0
    return int(text[0].replace("'", '')) * FEET_TO_CM_RATION + int(text[1].replace('"', '')) * INCH_TO_CM_RATION


def __parse_details_weight(element):
    weight = element.text.strip().split(':')[-1].strip().split(' ')[0]
    if weight == '--':
        return 0
    return int(weight) * POUNDS_TO_KG_RATIO


def __parse_details_reach(element):
    reach = element.text.strip().split(':')[-1].strip().replace('"', '')
    if reach == '--':
        return 0
    return int(reach) * INCH_TO_CM_RATION


def __parse_details_stance(element):
    if len(element.text.strip().split(':') < 1):
        return ''
    return element.text.strip().split(':')[-1].strip()


def __parse_details_dob(element):
    dob_str = element.text.strip().split(':')[-1].strip()
    return util.string_short_month_to_date(dob_str)
