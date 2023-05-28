from dataclasses import dataclass
from dataclasses import asdict


@dataclass
class FightDetail:
    fight_id: str = ""
    fighter_id: str = ""
    round_nr: int = 0

    knockdowns: int = 0
    sig_strikes_tot: int = 0
    sig_strikes_hit: int = 0

    overall_strikes_tot: int = 0
    overall_strikes_hit: int = 0

    takedown_attempts: int = 0
    takedown_success: int = 0

    sub_attempt: int = 0
    rev: int = 0
    control_time_sec: int = 0

    target_head_tot: int = 0
    target_head_hit: int = 0
    target_body_tot: int = 0
    target_body_hit: int = 0
    target_leg_tot: int = 0
    target_leg_hit: int = 0

    target_distance_tot: int = 0
    target_distance_hit: int = 0
    target_clinch_tot: int = 0
    target_clinch_hit: int = 0
    target_ground_tot: int = 0
    target_ground_hit: int = 0

    def dict(self):
        return asdict(self)
