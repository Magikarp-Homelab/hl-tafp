import logging.config

from crawler import crawlMain
from crawler import crawlEvent
from util import util


if __name__ == '__main__':
    logging.config.fileConfig('logging.conf')
    LOG = logging.getLogger(__name__)

    LOG.info(f'Crawling Events...')
    event_ids_list = crawlMain.get_eventids_from_site()

    filepath = 'data/event_ids'
    LOG.info(f'Writing event ids to {filepath}...')
    util.list_to_file(event_ids_list, filepath)
    LOG.info(f'Done writing {len(event_ids_list)} event ids to {filepath}')

    fight_ids_list = []
    for event_id in event_ids_list:
        LOG.info(f'Crawling fight for event id: {event_id} ...')
        fight_ids_list.extend(crawlEvent.get_fightid_from_event(event_id))

    filepath = 'data/fight_ids'
    LOG.info(f'Writing fight ids to {filepath}...')
    util.list_to_file(fight_ids_list, filepath)
    LOG.info(f'Done writing {len(fight_ids_list)} fight ids to {filepath}')

    print('Done!')
