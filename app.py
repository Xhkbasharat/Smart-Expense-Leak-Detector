from collections import defaultdict
from flask import Flask, render_template, request, redirect, url_for, flash
from datetime import datetime
from database import db, Expense
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)

with app.app_context():
    db.create_all()


@app.route("/")
def home():
    expenses = Expense.query.order_by(
        Expense.expense_date.desc()
    ).all()

    total = sum(expense.amount for expense in expenses)

    return render_template(
        "index.html",
        expenses=expenses,
        total=total
    )


@app.route("/add", methods=["POST"])
def add_expense():
    title = request.form.get("title", "").strip()
    category = request.form.get("category", "").strip()

    try:
        amount = float(request.form.get("amount", ""))
        expense_date = datetime.strptime(
            request.form.get("expense_date", ""),
            "%Y-%m-%d"
        ).date()

        if not title or not category or amount <= 0:
            raise ValueError

    except (ValueError, TypeError):
        flash("Please enter valid expense details.")
        return redirect(url_for("home"))

    expense = Expense(
        title=title,
        amount=amount,
        category=category,
        expense_date=expense_date
    )

    db.session.add(expense)
    db.session.commit()

    flash("Expense added successfully!")
    return redirect(url_for("home"))


@app.route("/delete/<int:expense_id>", methods=["POST"])
def delete_expense(expense_id):
    expense = db.session.get(Expense, expense_id)

    if expense:
        db.session.delete(expense)
        db.session.commit()
        flash("Expense deleted successfully!")

    return redirect(url_for("home"))


if __name__ == "__main__":
    app.run(debug=True)
