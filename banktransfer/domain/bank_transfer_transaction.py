from datetime import datetime

from shared.domain.money import Money


class BankTransferTransaction:
    def __init__(
        self,
        transaction_id: str,
        date: datetime,
        amount: Money,
        note_id: int,
        id: int = None,
    ):
        self.id = id  # this will exist after the transaction is saved
        self.transaction_id = transaction_id
        self.date = date
        self.amount = amount
        self.note_id = note_id

    def __eq__(self, other):
        return (
            self.id == other.id
            and self.transaction_id == other.transaction_id
            and self.date == other.date
            and self.amount == other.amount
            and self.note_id == other.note_id
        )
