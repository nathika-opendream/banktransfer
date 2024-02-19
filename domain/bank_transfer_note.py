from datetime import datetime

from domain.money import Money


class BankTransferNote:
    def __init__(
        self,
        note: str,
        amount: Money,
        date: datetime,
        id: int = None,
    ):
        self.id = id  # this will exist after the note is saved
        self.note = note
        self.amount = amount
        self.date = date

    def __eq__(self, other):
        return (
            self.id == other.id
            and self.note == other.note
            and self.amount == other.amount
            and self.date == other.date
        )
