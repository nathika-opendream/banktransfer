import uuid
from dataclasses import dataclass
from datetime import datetime

from shared.domain.money import Money


@dataclass
class BankTransferTransaction:
    id: int
    transaction_id: str
    date: datetime
    amount: Money
    note_id: int

    @staticmethod
    def new_bank_transfer_transaction(
        transaction_id: str, date: datetime, amount: Money, note_id: int
    ) -> "BankTransferTransaction":
        return BankTransferTransaction(
            id=uuid.uuid4(),
            transaction_id=transaction_id,
            date=date,
            amount=amount,
            note_id=note_id,
        )
