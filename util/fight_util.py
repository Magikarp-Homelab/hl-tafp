import pymongo

from CONSTANTS import COLLECTION_FIGHT
from util import db_util


def check_fight_id_in_db(fight_id):
    col = db_util.get_collection(COLLECTION_FIGHT)
    if col.find_one({"id": fight_id}):
        return True
    return False
