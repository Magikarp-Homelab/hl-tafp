from CONSTANTS import COLLECTION_FIGHT_DETAIL
from util import db_util


def persist_fight_detail_list(fight_details):
    col = db_util.get_collection(COLLECTION_FIGHT_DETAIL)
    for fd in fight_details:
        col.insert_one(fd.dict())
