from datetime import datetime

import pytest

from domain.bank_transfer_donation import (
    BankTransferDonation,
    BankTransferDonationStatus,
)
from domain.donee import Donee, DoneeType
from domain.donor import Donor, DonorType
from domain.money import Money


@pytest.fixture
def my_donor() -> Donor:
    return Donor(
        donor_type=DonorType.Individual,
        email="email@mail,com",
        phone="0987654321",
        name1="John",
        name2="Doe",
        name_prefix="Mr.",
        tax_id="1234567890987",
        member_id="1234",
    )


@pytest.fixture
def my_donee() -> Donee:
    return Donee(
        ref_id=1,
        name="Covid-19 Relief Fund",
        donee_type=DoneeType.Project,
        meta={"key": "value"},
    )


class TestBankTransferDonation:
    def test_add_note_to_bank_transfer_donation(my_donor, my_donee):
        donor = my_donor
        donee = my_donee

        bank_transfer_donation = BankTransferDonation(
            id=1,
            donation_number="123456",
            expected_amount=Money(amount=100, currency="USD"),
            donor=donor,
            donee=donee,
        )

        assert bank_transfer_donation.notes == []
        assert bank_transfer_donation.transactions == []
        assert bank_transfer_donation.status == BankTransferDonationStatus.New
        assert bank_transfer_donation.form_data == {}
        assert bank_transfer_donation.meta == {}

        bank_transfer_donation.add_note(
            "test", Money(amount=100, currency="THB"), datetime.now()
        )
        assert bank_transfer_donation.status == BankTransferDonationStatus.Pending
        assert len(bank_transfer_donation.notes) == 1

    # TODO: Implement the test
    def test_approve_bank_transfer_donation(my_donor, my_donee):
        pass
