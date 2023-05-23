from dataclasses import dataclass


@dataclass
class Fighter:
    id: str = ""
    firstname: str = ""
    lastname: str = ""
    height: int = 0
    weight: int = 0
    reach: int = 0
    stance: str = ""
    dob: str = ""
