import uuid
from dataclasses import dataclass
from datetime import datetime

from shared.domain.money import Money


@dataclass
class BankTransferNote:
    id: int
    note: str
    amount: Money
    date: datetime

    @staticmethod
    def new_bank_transfer_note(
        note: str, amount: Money, date: datetime
    ) -> "BankTransferNote":
        return BankTransferNote(
            id=uuid.uuid4(),
            note=note,
            amount=amount,
            date=date,
        )
