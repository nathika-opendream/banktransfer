from abc import ABC, abstractmethod

from bank_transfer_donation import BankTransferDonation


class IBankTransferRepository(ABC):
    @abstractmethod
    def save(self, bank_transfer: BankTransferDonation) -> None:
        raise NotImplementedError()

    @abstractmethod
    def get_by_id(self, bank_transfer_id: str) -> BankTransferDonation:
        raise NotImplementedError()

    def __getitem__(self, bank_transfer_id: str) -> BankTransferDonation:
        return self.get_by_id(bank_transfer_id)
