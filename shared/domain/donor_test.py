from dataclasses import FrozenInstanceError

import pytest
from donor import Donor, DonorType


@pytest.fixture
def my_donor() -> Donor:
    return Donor(
        donor_type=DonorType.PER,
        email="email@mail,com",
        phone="0987654321",
        name1="John",
        name2="Doe",
        name_prefix="Mr.",
        tax_id="1234567890987",
        member_id="1234",
    )


class TestDonor:
    def test_donor(self):
        donor_1 = Donor(
            donor_type=DonorType.PER,
            email="email@mail,com",
            phone="0987654321",
            name1="John",
            name2="Doe",
            name_prefix="Mr.",
            tax_id="1234567890987",
            member_id="1234",
        )

        donor_2 = Donor(
            donor_type=DonorType.PER,
            email="email@mail,com",
            phone="0987654321",
            name1="John",
            name2="Doe",
            name_prefix="Mr.",
            tax_id="1234567890987",
            member_id="1234",
        )

        assert donor_1 == donor_2

    def test_immutable_donor(self, my_donor):
        donor_1 = my_donor

        with pytest.raises(FrozenInstanceError):
            donor_1.member_id = "1111"

    def test_change_donor_name(self, my_donor):
        donor_1 = my_donor

        new_donor = donor_1.change_name(name1="Jane", name2="Doe")
        assert new_donor.name1 == "Jane"
        assert new_donor.name2 == "Doe"
