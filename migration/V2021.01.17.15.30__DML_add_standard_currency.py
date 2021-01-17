"""
Add standard currency
"""
from datetime import datetime

dependencies = []


def upgrade(db):
    data = {
        "name": "Brazilian real",
        "iso_code": "BRL",
        "standard": True,
        "creation_date": datetime.utcnow(),
        "update_date": datetime.utcnow(),
    }
    db.currency.insert_one(data)


def downgrade(db):
    pass
