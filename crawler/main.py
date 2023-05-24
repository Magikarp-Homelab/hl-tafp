from crawler import crawlMain
from util import util

import logging.config

if __name__ == '__main__':
    logging.config.fileConfig('logging.conf')
    LOG = logging.getLogger(__name__)

    LOG.info(f'Crawling Events...')
    event_ids_list = crawlMain.get_eventids_from_site()

    filepath = 'data/event_ids_sample'
    LOG.info(f'Writing event ids to {filepath}...')
    util.list_to_file(event_ids_list, filepath)
    LOG.info(f'Done writing {len(event_ids_list)} event ids to {filepath}')

    print('Done!')
