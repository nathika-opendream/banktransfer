import uuid

from fastapi import FastAPI
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from banktransfer.domain.bank_transfer_donation import BankTransferDonation
from banktransfer.domain.mapper import metadata, start_mapper
from banktransfer.infra.bank_transfer_repository import BankTransferDonationRepository
from shared.domain.donee import Donee
from shared.domain.donor import Donor
from shared.domain.money import Money


# start to connect to the database
def get_db():
    print("Connecting to the database...")
    start_mapper()

    DATABASE_URL = "postgresql+psycopg2://nathika@localhost:5432/test_donation"
    engine = create_engine(DATABASE_URL)
    Session = sessionmaker(bind=engine)
    session = Session()

    metadata.create_all(engine)
    return session, engine


app = FastAPI()
session, engine = get_db()


@app.on_event("shutdown")
async def shutdown_event():
    print("Shutting down")
    session.close()
    engine.dispose()


@app.get("/")
def read_root():
    return {"message": "bank transfer donation service is running..."}


@app.get("/bank-transfer-donations/")
def get_all_bank_transfer_donations():
    repo = BankTransferDonationRepository(session)
    donations = repo.get_all()
    return donations


@app.get("/bank-transfer-donation/{donation_id}")
def get_bank_transfer_donation_by_id(donation_id: uuid.UUID):
    repo = BankTransferDonationRepository(session)
    donation = repo.get_by_id(donation_id)
    return donation


@app.post("/bank-transfer-donation/")
def add_bank_transfer_donation(
    donation_number: str,
    donor: Donor,
    donee: Donee,
    amount: str,
    currency: str,
):
    donation = BankTransferDonation.new_bank_transfer_donation(
        donation_number=donation_number,
        donor=donor,
        donee=donee,
        expected_amount=Money(amount=amount, currency=currency),
    )

    repo = BankTransferDonationRepository(session)

    added_donation = repo.add(donation)
    session.commit()

    return added_donation
