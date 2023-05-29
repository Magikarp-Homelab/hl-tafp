from CONSTANTS import COLLECTION_FIGHTER
from util import db_util


def check_fighter_id_in_db(fighter_id):
    col = db_util.get_collection(COLLECTION_FIGHTER)
    if col.find_one({"id": fighter_id}):
        return True
    return False


def persist_fighter(fighter):
    col = db_util.get_collection(COLLECTION_FIGHTER)
    col.insert_one(fighter.dict())
