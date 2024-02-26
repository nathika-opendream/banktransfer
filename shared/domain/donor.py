from dataclasses import dataclass
from enum import Enum


class DonorType(Enum):
    PER = "PER"
    ORG = "ORG"


@dataclass(frozen=True)
class Donor:
    donor_type: DonorType
    email: str
    phone: str
    name1: str
    name2: str
    name_prefix: str
    tax_id: str
    member_id: str = None

    def change_name(self, name1: str, name2: str) -> "Donor":
        return Donor(
            donor_type=self.donor_type,
            email=self.email,
            phone=self.phone,
            name1=name1,
            name2=name2,
            name_prefix=self.name_prefix,
            tax_id=self.tax_id,
            member_id=self.member_id,
        )
