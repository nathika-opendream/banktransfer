from abc import ABC, abstractmethod

from bank_transfer_donation import BankTransferDonation
from sqlalchemy.orm import Session


class IBankTransferRepository(ABC):
    def __init__(self, session: Session) -> None:
        self._session = session

    @abstractmethod
    def add(self, bank_transfer: BankTransferDonation) -> None:
        raise NotImplementedError()

    @abstractmethod
    def get_by_id(self, bank_transfer_id: str) -> BankTransferDonation:
        raise NotImplementedError()

    @abstractmethod
    def get_all(self) -> list[BankTransferDonation]:
        raise NotImplementedError()
