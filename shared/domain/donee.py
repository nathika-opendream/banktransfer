from dataclasses import dataclass
from enum import Enum


class DoneeType(Enum):
    PROJECT = "proj"
    FUNDRAISER = "fund"
    CART = "cart"
    CAMPAIGNER = "camp"
    MICROSITE = "mics"


@dataclass(frozen=True)
class Donee:
    ref_id: int
    name: str
    donee_type: DoneeType
    meta: dict
