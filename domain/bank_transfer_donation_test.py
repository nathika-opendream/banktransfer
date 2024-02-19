from datetime import datetime

import pytest

from domain.bank_transfer_donation import (
    BankTransferDonation,
    BankTransferDonationStatus,
)
from domain.bank_transfer_note import BankTransferNote
from domain.donee import Donee, DoneeType
from domain.donor import Donor, DonorType
from domain.money import Money


@pytest.fixture
def my_donor() -> Donor:
    return Donor(
        donor_type=DonorType.INDIVIDUAL,
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
        donee_type=DoneeType.PROJECT,
        meta={"key": "value"},
    )


@pytest.fixture
def my_note() -> BankTransferNote:
    return BankTransferNote(
        id=1,
        note="note",
        amount=Money(amount=100, currency="THB"),
        date=datetime.now(),
    )


class TestBankTransferDonation:
    def test_create_bank_transfer_donation(my_donor, my_donee):
        donor = my_donor
        donee = my_donee

        bank_transfer_donation = BankTransferDonation(
            id=1,
            donation_number="123456",
            expected_amount=Money(amount=100, currency="USD"),
            donor=donor,
            donee=donee,
        )

        assert bank_transfer_donation.id == 1
        assert bank_transfer_donation.donation_number == "123456"
        assert bank_transfer_donation.expected_amount == Money(
            amount=100, currency="USD"
        )
        assert bank_transfer_donation.donor == donor
        assert bank_transfer_donation.donee == donee
        assert bank_transfer_donation.notes == []
        assert bank_transfer_donation.transactions == []
        assert bank_transfer_donation.status == BankTransferDonationStatus.NEW
        assert bank_transfer_donation.form_data == {}
        assert bank_transfer_donation.meta == {}

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
        assert bank_transfer_donation.status == BankTransferDonationStatus.NEW
        assert bank_transfer_donation.form_data == {}
        assert bank_transfer_donation.meta == {}

        bank_transfer_donation.add_note(
            note="test",
            amount=Money(amount=100, currency="THB"),
            date=datetime.now(),
        )
        assert bank_transfer_donation.status == BankTransferDonationStatus.PENDING
        assert len(bank_transfer_donation.notes) == 1

    def test_confirm_bank_transfer_donation(my_donor, my_donee, my_note):
        donor = my_donor
        donee = my_donee
        note = my_note

        bank_transfer_donation = BankTransferDonation(
            id=1,
            donation_number="123456",
            expected_amount=Money(amount=100, currency="USD"),
            donor=donor,
            donee=donee,
            notes=[note],
        )

        transaction = bank_transfer_donation.confirm_transaction(
            transaction_id=1,
            date=datetime.now(),
            amount=Money(amount=100, currency="THB"),
            note_id=1,
        )
        assert bank_transfer_donation.status == BankTransferDonationStatus.PAID
        assert len(bank_transfer_donation.transactions) == 1
        assert transaction.amount == Money(amount=100, currency="THB")
        assert transaction.note_id == note.id
        assert transaction.date is not None
