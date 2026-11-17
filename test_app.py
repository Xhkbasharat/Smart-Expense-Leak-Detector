
import pytest

from app import app
from database import db, Expense


@pytest.fixture
def client():
    app.config.update({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
        "SECRET_KEY": "test-secret"
    })

    with app.app_context():
        db.drop_all()
        db.create_all()

        with app.test_client() as client:
            yield client

        db.session.remove()
        db.drop_all()


def test_home_page(client):
    response = client.get("/")
    assert response.status_code == 200


def test_add_expense(client):
    response = client.post("/add", data={
        "title": "Lunch",
        "amount": "150",
        "category": "Food",
        "expense_date": "2026-11-17"
    }, follow_redirects=True)

    assert response.status_code == 200

    expense = Expense.query.first()
    assert expense is not None
    assert expense.title == "Lunch"
    assert expense.amount == 150


def test_delete_expense(client):
    with app.app_context():
        from datetime import date

        expense = Expense(
            title="Coffee",
            amount=50,
            category="Food",
            expense_date=date(2026, 11, 17)
        )

        db.session.add(expense)
        db.session.commit()
        expense_id = expense.id

    response = client.post(
        f"/delete/{expense_id}",
        follow_redirects=True
    )

    assert response.status_code == 200
    assert db.session.get(Expense, expense_id) is None
