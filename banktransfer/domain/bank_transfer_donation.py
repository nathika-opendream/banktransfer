from datetime import datetime
from enum import Enum
from typing import Any

from bank_transfer_note import BankTransferNote
from bank_transfer_transaction import BankTransferTransaction

from shared.domain.donee import Donee
from shared.domain.donor import Donor
from shared.domain.money import Money


class BankTransferDonationStatus(Enum):
    NEW = "new"
    PENDING = "pending"
    PAID = "paid"


class BankTransferDonation:
    def __init__(
        self,
        id: int,
        donation_number: str,
        expected_amount: Money,
        donor: Donor,
        donee: Donee,
        notes: list[BankTransferNote] = [],
        transactions: list[BankTransferTransaction] = [],
        status: BankTransferDonationStatus = BankTransferDonationStatus.NEW,
        form_data: dict[str, Any] = {},
        meta: dict[str, Any] = {},
    ):
        self.id = id
        self.donation_number = donation_number
        self.expected_amount = expected_amount
        self.donor = donor
        self.donee = donee
        self.notes = notes
        self.transactions = transactions
        self.status = status
        self.form_data = form_data
        self.meta = meta

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
            self.status = BankTransferDonationStatus.PENDING
        else:
            raise ValueError("Donation already has transactions")

    def validate_note_id(self, note_id: int):
        is_valid = False
        for note in self.notes:
            if note.id == note_id:
                is_valid = True

        if not is_valid:
            raise ValueError("Note ID must be one of the Donation's Notes")

        return is_valid

    def confirm_transaction(
        self,
        transaction_id: int,
        date: datetime,
        amount: Money,
        note_id: int,
    ):
        if amount == 0:
            raise ValueError("Amount must be greater than 0")

        if self.validate_note_id(note_id):
            # return transaction if the transaction is already confirmed
            for transaction in self.transactions:
                if (
                    transaction.transaction_id == transaction_id
                    or transaction.note_id == note_id
                ):
                    return transaction

            transaction = BankTransferTransaction(
                transaction_id=transaction_id,
                date=date,
                amount=amount,
                note_id=note_id,
            )
            self.transactions.append(transaction)
            self.status = BankTransferDonationStatus.PAID

            return transaction