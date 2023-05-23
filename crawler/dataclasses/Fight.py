from dataclasses import dataclass


@dataclass
class Fight:
    id: str = ""
    fighter1_id: str = ""
    fighter2_id: str = ""
    winner_id: str = ""
    champ_bout: bool = False

    weight_class: str = ""
    method: str = ""
    rounds: str = ""
    round_time: str = ""
    referee: str = ""
