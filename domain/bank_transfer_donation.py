from datetime import datetime
from enum import Enum
from domain.donee import Donee
from domain.donor import Donor
from domain.money import Money


class BankTransferDonationStatus(Enum):
    New = "NEW"
    Pending = "PENDING"
    Paid = "PAID"


class BankTransferNote:
    def __init__(self, note: str, amount: Money, date: datetime):
        self.note = note
        self.amount = amount
        self.date = date

    def __eq__(self, other):
        return (
            self.note == other.note
            and self.amount == other.amount
            and self.date == other.date
        )


class BankTransferDonation:
    def __init__(
        self,
        id: int,
        donation_number: str,
        expected_amount: Money,
        donor: Donor,
        donee: Donee,
    ):
        self.id = id
        self.donation_number = donation_number
        self.expected_amount = expected_amount
        self.donor = donor
        self.donee = donee
        self.notes = []
        self.transactions = []
        self.status = BankTransferDonationStatus.New
        self.form_data = {}
        self.meta = {}

    def add_note(self, note: str, amount: Money, date: datetime):
        if amount == 0:
            raise ValueError("Amount must be greater than 0")
        
        if not self.transactions:
            note = BankTransferNote(
                note=note,
                amount=amount,
                date=date,
            )
            self.notes.append(note)
            self.status = BankTransferDonationStatus.Pending
        else:
            raise ValueError("Donation already has transactions")
