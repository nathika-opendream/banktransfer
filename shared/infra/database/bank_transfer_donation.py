from sqlalchemy import (
    JSON,
    UUID,
    Column,
    Composite,
    DateTime,
    Float,
    Integer,
    MetaData,
    String,
    Table,
)

from shared.domain.donee import Donee
from shared.domain.donor import Donor
from shared.domain.money import Money

metadata = MetaData()

bank_transfer_donation = Table(
    "bank_transfer_donation",
    metadata,
    Column("id", UUID, primary_key=True),
    Column("version", Integer),
    Column("created_at", DateTime),
    Column("updated_at", DateTime),
    Column("donation_number", String),
    Column(
        "donor",
        Composite(
            Donor,
            Column("donor_type", String),
            Column("donor_member_id", Integer),
            Column("donor_email", String),
            Column("donor_phone", String),
            Column("donor_name1", String),
            Column("donor_name2", String),
            Column("donor_name_prefix", String),
            Column("donor_tax_id", String),
        ),
    ),
    Column(
        "donee",
        Composite(
            Donee,
            Column("donee_ref_id", String),
            Column("donee_type", String),
            Column("donee_name", String),
            Column("donee_meta", JSON),
        ),
    ),
    Column(
        "money",
        Composite(
            Money,
            Column("expected_amount", Float),
            Column("currency", String),
        ),
    ),
    Column("status", String),
    Column("donation_created_at", DateTime),
    Column("meta", JSON),
    Column("form_data", JSON),
)
