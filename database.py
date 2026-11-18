
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()


class Expense(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    title = db.Column(
        db.String(100),
        nullable=False
    )

    amount = db.Column(
        db.Float,
        nullable=False
    )

    category = db.Column(
        db.String(50),
        nullable=False
    )

    expense_date = db.Column(
        db.Date,
        nullable=False
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "amount": self.amount,
            "category": self.category,
            "expense_date": self.expense_date.isoformat(),
            "created_at": self.created_at.isoformat()
            if self.created_at else None
        }


class Budget(db.Model):
    id = db.Column(
        db.Integer,
        primary_key=True
    )

    month = db.Column(
        db.String(7),
        unique=True,
        nullable=False
    )

    amount = db.Column(
        db.Float,
        nullable=False
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    def to_dict(self):
        return {
            "id": self.id,
            "month": self.month,
            "amount": self.amount,
            "created_at": self.created_at.isoformat()
            if self.created_at else None
        }
