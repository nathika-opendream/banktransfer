from sqlalchemy import (
    JSON,
    UUID,
    Column,
    DateTime,
    Enum,
    Float,
    Integer,
    MetaData,
    String,
    Table,
)
from sqlalchemy.orm import composite, registry

from banktransfer.domain.bank_transfer_donation import (
    BankTransferDonation,
    BankTransferDonationStatus,
)
from shared.domain.donee import Donee, DoneeType
from shared.domain.donor import Donor, DonorType
from shared.domain.money import Money

metadata = MetaData()
mapper_registry = registry(metadata=metadata)


def start_mapper():
    table = Table(
        "bank_transfer_donation",
        metadata,
        Column("id", UUID, primary_key=True),
        Column("version", Integer),
        Column("created_at", DateTime(timezone=True)),
        Column("updated_at", DateTime),
        Column("donation_number", String),
        Column("donor_type", Enum(DonorType)),
        Column("donor_member_id", Integer),
        Column("donor_email", String),
        Column("donor_phone", String),
        Column("donor_name1", String),
        Column("donor_name2", String),
        Column("donor_name_prefix", String),
        Column("donor_tax_id", String),
        Column("donee_ref_id", String),
        Column("donee_type", Enum(DoneeType)),
        Column("donee_name", String),
        Column("donee_meta", JSON),
        Column("amount", Float),
        Column("currency", String),
        Column("status", Enum(BankTransferDonationStatus)),
        Column("donation_created_at", DateTime),
        Column("meta", JSON),
        Column("form_data", JSON),
    )

    mapper_registry.map_imperatively(
        BankTransferDonation,
        table,
        properties={
            "donor": composite(
                Donor,
                table.c.donor_type,
                table.c.donor_email,
                table.c.donor_phone,
                table.c.donor_name1,
                table.c.donor_name2,
                table.c.donor_name_prefix,
                table.c.donor_tax_id,
                table.c.donor_member_id,
            ),
            "donee": composite(
                Donee,
                table.c.donee_ref_id,
                table.c.donee_name,
                table.c.donee_type,
                table.c.donee_meta,
            ),
            "expected_amount": composite(
                Money,
                table.c.amount,
                table.c.currency,
            ),
        },
    )
