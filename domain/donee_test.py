from dataclasses import FrozenInstanceError

import pytest

from domain.donee import Donee, DoneeType


@pytest.fixture
def my_donee() -> Donee:
    return Donee(
        ref_id=1,
        name="Covid-19 Relief Fund",
        donee_type=DoneeType.PROJECT,
        meta={"key": "value"},
    )


class TestDonee:
    def test_donee(self):
        donee_1 = Donee(
            ref_id=1,
            name="name",
            donee_type=DoneeType.PROJECT,
            meta={"key": "value"},
        )

        donee_2 = Donee(
            ref_id=1,
            name="name",
            donee_type=DoneeType.PROJECT,
            meta={"key": "value"},
        )

        assert donee_1 == donee_2

    def test_immutable_donee(self, my_donee):
        donee_1 = my_donee

        with pytest.raises(FrozenInstanceError):
            donee_1.ref_id = 2
