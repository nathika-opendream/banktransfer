from dataclasses import dataclass
from enum import Enum


class DoneeType(Enum):
    Project = "PROJ"
    Fundraiser = "FUND"
    Cart = "CART"
    Campaigner = "CAMP"
    Microsite = "MICS"

@dataclass(frozen=True)
class Donee:
    ref_id: int
    name: str
    donee_type: DoneeType
    meta: dict
   