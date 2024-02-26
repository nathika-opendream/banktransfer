from datetime import datetime

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import clear_mappers, sessionmaker

from banktransfer.domain.bank_transfer_donation import BankTransferDonation
from banktransfer.domain.bank_transfer_note import BankTransferNote
from banktransfer.domain.mapper import metadata, start_mapper
from banktransfer.infra.bank_transfer_repository import BankTransferDonationRepository
from shared.domain.donee import Donee, DoneeType
from shared.domain.donor import Donor, DonorType
from shared.domain.money import Money


@pytest.fixture
def my_donor() -> Donor:
    return Donor(
        donor_type=DonorType.PER,
        email="email@mail,com",
        phone="0987654321",
        name1="John",
        name2="Doe",
        name_prefix="Mr.",
        tax_id="1234567890987",
        member_id="1234",
    )


@pytest.fixture
def my_donee() -> Donee:
    return Donee(
        ref_id="111",
        name="Covid-19 Relief Fund",
        donee_type=DoneeType.PROJ,
        meta={},
    )


@pytest.fixture()
def session():
    start_mapper()

    DATABASE_URL = "postgresql+psycopg2://nathika@localhost:5432/test_donation"
    engine = create_engine(DATABASE_URL)
    Session = sessionmaker(bind=engine)
    session = Session()

    metadata.create_all(engine)
    yield session


def test_bank_transfer_mapper_can_add(session, my_donor, my_donee):
    donor = my_donor
    donee = my_donee

    donation = BankTransferDonation.new_bank_transfer_donation(
        donor=donor,
        donee=donee,
        donation_number="123",
        expected_amount=Money(amount=100, currency="THB"),
    )

    repo = BankTransferDonationRepository(session)

    all = repo.get_all()
    assert len(all) == 0

    add_donation = repo.add(donation)
    session.flush()

    donations = repo.get_all()
    assert add_donation == donation
    assert len(donations) == 1

    session.rollback()
