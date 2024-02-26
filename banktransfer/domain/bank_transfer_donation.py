import uuid
from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Any

from banktransfer.domain.bank_transfer_note import BankTransferNote
from banktransfer.domain.bank_transfer_transaction import BankTransferTransaction
from shared.domain.donee import Donee
from shared.domain.donor import Donor
from shared.domain.money import Money


class BankTransferDonationStatus(Enum):
    NEW = "NEW"
    PENDING = "PENDING"
    PAID = "PAID"


@dataclass
class BankTransferDonation:
    id: uuid.UUID
    version: int
    created_at: datetime
    updated_at: datetime
    donation_number: str
    expected_amount: Money
    donor: Donor
    donee: Donee
    notes: list[BankTransferNote]
    transactions: list[BankTransferTransaction]
    status: BankTransferDonationStatus
    form_data: dict
    meta: dict
    donation_created_at: datetime

    @staticmethod
    def new_bank_transfer_donation(
        donor: Donor,
        donee: Donee,
        donation_number: str,
        expected_amount: Money,
    ) -> "BankTransferDonation":
        return BankTransferDonation(
            id=uuid.uuid4(),
            version=1,
            created_at=datetime.now(),
            updated_at=datetime.now(),
            donation_number=donation_number,
            expected_amount=expected_amount,
            donor=donor,
            donee=donee,
            notes=[],
            transactions=[],
            status=BankTransferDonationStatus.NEW,
            form_data={},
            meta={},
            donation_created_at=None,
        )

    def add_note(self, note: str, amount: Money, date: datetime):
        if amount == 0:
            raise ValueError("Amount must be greater than 0")

        if not self.transactions:
            note = BankTransferNote.new_bank_transfer_note(
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

            transaction = BankTransferTransaction.new_bank_transfer_transaction(
                transaction_id=transaction_id,
                date=date,
                amount=amount,
                note_id=note_id,
            )
            self.transactions.append(transaction)
            self.status = BankTransferDonationStatus.PAID

            return transaction
