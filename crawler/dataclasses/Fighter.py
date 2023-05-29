from dataclasses import dataclass
from dataclasses import asdict


@dataclass
class Fighter:
    id: str = ""
    firstname: str = ""
    lastname: str = ""
    record_win: int = 0
    record_loss: int = 0
    record_nc: int = 0
    height: int = 0
    weight: int = 0
    reach: int = 0
    stance: str = ""
    dob: str = ""

    def dict(self):
        return asdict(self)
