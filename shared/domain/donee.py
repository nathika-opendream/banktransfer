from dataclasses import dataclass
from enum import Enum


class DoneeType(Enum):
    PROJ = "PROJ"
    FUND = "FUND"
    CART = "CART"
    CAMP = "CAMP"
    MICS = "MICS"


@dataclass(frozen=True)
class Donee:
    ref_id: int
    name: str
    donee_type: DoneeType
    meta: dict
