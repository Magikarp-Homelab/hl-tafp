

from util import util
from crawler.dataclasses.Fight import Fight
from crawler.dataclasses.FightDetail import FightDetail
from CONSTANTS import URL_FIGHT, FIGHT_TITLE_BOUT


def crawl_fight_with_id(fight_id: str):
    soup = util.get_soup(URL_FIGHT + fight_id)

    fight = Fight(id=fight_id)

    fighter1, fighter2 = __parse_both_fighter_from_soup(soup)
    fight.fighter1_id = fighter1
    fight.fighter2_id = fighter2
    fight.winner_id = __parse_winner_from_soup(soup)
    fight.champ_bout = __parse_champ_bout_from_soup(soup)
    fight.weight_class = __parse_weight_class_from_bout(soup)
    fight.method, fight.rounds, fight.round_time, fight.referee = __parse_bout_details_from_bout(soup)

    # get details, one detail for each round, roundnr = 0 for totals
    fighter_detail1 = FightDetail(fight_id=fight_id, fighter_id=fighter1)
    fighter_detail2 = FightDetail(fight_id=fight_id, fighter_id=fighter2)

    return


def __parse_both_fighter_from_soup(soup):
    elements = soup.findAll('a', 'b-fight-details__person-link')
    return elements[0].attrs['href'].strip().split('/')[-1], elements[1].attrs['href'].strip().split('/')[-1]


def __parse_winner_from_soup(soup):
    elements = soup.findAll('div', 'b-fight-details__person')
    for ele in elements:
        winner_ele = ele.findAll('i', 'b-fight-details__person-status_style_green')
        if len(winner_ele) > 0:
            tmp = ele.findAll('a', 'b-fight-details__person-link')[0]
            break

    return tmp.attrs['href'].strip().split('/')[-1]


def __parse_champ_bout_from_soup(soup):
    element = soup.findAll('i', 'b-fight-details__fight-title')[0]
    txt = element.text.strip()
    return True if FIGHT_TITLE_BOUT in txt else False


def __parse_weight_class_from_bout(soup):
    element = soup.findAll('i', 'b-fight-details__fight-title')[0]
    txt = element.text.strip()
    wc = txt.split('weight')[0].replace('UFC ', '')
    return wc + 'weight'


def __parse_bout_details_from_bout(soup):
    elements = soup.findAll('i', 'b-fight-details__text-item')
    method = elements[0].text.strip().split(' ')[-1]
    rounds = elements[1].text.strip().split(' ')[-1]
    round_time = elements[2].text.strip().split(' ')[-1]
    referee = ' '.join(elements[3].text.strip().split(' ')[-2:])
    return method, rounds, round_time, referee
