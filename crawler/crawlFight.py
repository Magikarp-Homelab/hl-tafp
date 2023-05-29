import logging.config

from util import util
from util.fight_util import persist_fight
from util.fight_detail_util import persist_fight_detail_list
from crawler.crawlFighter import crawl_fighter_with_id
from crawler.dataclasses.Fight import Fight
from crawler.dataclasses.FightDetail import FightDetail
from CONSTANTS import URL_FIGHT
from CONSTANTS import FIGHT_TITLE_BOUT


def crawl_fight_with_id(fight_id: str):
    LOG = logging.getLogger(__name__)
    LOG.debug(f'Crawling fight {fight_id}...')

    soup = util.get_soup(URL_FIGHT + fight_id)

    fight = Fight(id=fight_id)

    fighter1, fighter2 = __parse_both_fighter_from_soup(soup)

    crawl_fighter_with_id(fighter1)
    crawl_fighter_with_id(fighter2)

    fight.fighter1_id = fighter1
    fight.fighter2_id = fighter2
    fight.winner_id = __parse_winner_from_soup(soup)
    fight.champ_bout = __parse_champ_bout_from_soup(soup)
    fight.weight_class = __parse_weight_class_from_bout(soup)
    fight.method, fight.rounds, fight.round_time, fight.referee = __parse_bout_details_from_bout(soup)

    # get details, one detail for each round, roundNr = 0 for totals
    fight_details = __crawl_fight_details(soup, fight_id, fighter1, fighter2)

    # persist data
    persist_fight_detail_list(fight_details)
    persist_fight(fight)

    return fight_details


def __crawl_fight_details(soup, fight_id, fighter1, fighter2):
    details = []
    fight_details_elements = soup.findAll('section', 'b-fight-details__section')

    totals_element = fight_details_elements[1]
    rounds_element = fight_details_elements[2].findAll('tr', 'b-fight-details__table-row')[1:]
    ss_rounds_element = fight_details_elements[4].findAll('tr', 'b-fight-details__table-row')[1:]

    tmp = soup.findAll('div', 'b-fight-details')
    ss_totals_element = tmp[0].findChildren('table', recursive=False)[0]

    fighter_detail1, fighter_detail2 = __parse_fight_detail_from_soup(totals_element, ss_totals_element)
    fighter_detail1.fight_id = fight_id
    fighter_detail1.fighter_id = fighter1
    fighter_detail1.round_nr = 0
    fighter_detail2.fight_id = fight_id
    fighter_detail2.fighter_id = fighter2
    fighter_detail2.round_nr = 0
    details.append(fighter_detail1)
    details.append(fighter_detail2)

    for idx, round_element in enumerate(rounds_element):
        fighter_detail1, fighter_detail2 = __parse_fight_detail_from_soup(round_element, ss_rounds_element[idx])
        fighter_detail1.fight_id = fight_id
        fighter_detail1.fighter_id = fighter1
        fighter_detail1.round_nr = idx+1
        fighter_detail2.fight_id = fight_id
        fighter_detail2.fighter_id = fighter2
        fighter_detail2.round_nr = idx+1

        details.append(fighter_detail1)
        details.append(fighter_detail2)

    return details


def __parse_fight_detail_from_soup(soup, ss_soup):
    fighter_detail1 = FightDetail()
    fighter_detail2 = FightDetail()

    # first table
    all_cells = soup.findAll('td')
    fighter_detail1.knockdowns, fighter_detail2.knockdowns = __parse_detail_kd(all_cells[1])

    fighter_detail1.sig_strikes_hit, fighter_detail1.sig_strikes_tot,\
        fighter_detail2.sig_strikes_hit, fighter_detail2.sig_strikes_tot = __parse_detail_counts(all_cells[2])

    fighter_detail1.overall_strikes_hit, fighter_detail1.overall_strikes_tot,\
        fighter_detail2.overall_strikes_hit, fighter_detail2.overall_strikes_tot = __parse_detail_counts(all_cells[4])

    fighter_detail1.takedown_success, fighter_detail1.takedown_attempts,\
        fighter_detail2.takedown_success, fighter_detail2.takedown_attempts = __parse_detail_counts(all_cells[5])

    fighter_detail1.sub_attempt, fighter_detail2.sub_attempt = __parse_detail_sub(all_cells[7])
    fighter_detail1.rev, fighter_detail2.rev = __parse_detail_sub(all_cells[8])
    fighter_detail1.control_time_sec, fighter_detail2.control_time_sec = __parse_detail_ctrl_time(all_cells[9])

    # second table
    all_cells = ss_soup.findAll('td')
    fighter_detail1.target_head_hit, fighter_detail1.target_head_tot,\
        fighter_detail2.target_head_hit, fighter_detail2.target_head_tot = __parse_detail_counts(all_cells[3])

    fighter_detail1.target_body_hit, fighter_detail1.target_body_tot, \
        fighter_detail2.target_body_hit, fighter_detail2.target_body_tot = __parse_detail_counts(all_cells[4])

    fighter_detail1.target_leg_hit, fighter_detail1.target_leg_tot, \
        fighter_detail2.target_leg_hit, fighter_detail2.target_leg_tot = __parse_detail_counts(all_cells[5])

    fighter_detail1.target_distance_hit, fighter_detail1.target_distance_tot, \
        fighter_detail2.target_distance_hit, fighter_detail2.target_distance_tot = __parse_detail_counts(all_cells[6])

    fighter_detail1.target_clinch_hit, fighter_detail1.target_clinch_tot, \
        fighter_detail2.target_clinch_hit, fighter_detail2.target_clinch_tot = __parse_detail_counts(all_cells[7])

    fighter_detail1.target_ground_hit, fighter_detail1.target_ground_tot, \
        fighter_detail2.target_ground_hit, fighter_detail2.target_ground_tot = __parse_detail_counts(all_cells[8])

    return fighter_detail1, fighter_detail2


def __parse_detail_ctrl_time(soup):
    p_eles = soup.findAll('p')
    times = []
    for pe in p_eles:
        time = pe.text.strip().split(':')
        times.append(int(time[0])*60 + int(time[1]))
    return times[0], times[1]


def __parse_detail_sub(soup):
    p_eles = soup.findAll('p')
    return p_eles[0].text.strip(), p_eles[1].text.strip()


def __parse_detail_counts(soup):
    p_eles = soup.findAll('p')
    text_eles = list(map(lambda x: x.text.strip(), p_eles))
    f1 = text_eles[0].split(' of ')
    f2 = text_eles[1].split(' of ')
    return f1[0], f1[1], f2[0], f2[1]


def __parse_detail_kd(soup):
    p_eles = soup.findAll('p')
    return list(map(lambda x: x.text.strip(), p_eles))


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
