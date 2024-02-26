from banktransfer.domain.bank_transfer_donation import BankTransferDonation


class BankTransferDonationRepository:
    def __init__(self, session) -> None:
        self.session = session

    def add(self, bank_transfer_donation):
        self.session.add(bank_transfer_donation)
        return bank_transfer_donation

    def get_by_id(self, id):
        return self.session.query(BankTransferDonation).get(id)

    def get_all(self):
        return self.session.query(BankTransferDonation).all()
