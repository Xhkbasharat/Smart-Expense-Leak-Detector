
import csv
import io

from datetime import datetime, date
from collections import defaultdict

from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    flash,
    make_response
)

from database import db, Expense, Budget
from config import Config

from leak_detector import detect_money_leaks
from savings_advisor import generate_saving_tips


# =====================================
# APPLICATION CONFIGURATION
# =====================================

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)

with app.app_context():
    db.create_all()


# =====================================
# HOME DASHBOARD
# =====================================

@app.route("/")
def home():

    expenses = Expense.query.order_by(
        Expense.expense_date.desc()
    ).all()

    total = sum(
        expense.amount for expense in expenses
    )

    current_month = date.today().strftime("%Y-%m")

    # Monthly spending
    monthly_expenses = [
        expense for expense in expenses
        if expense.expense_date.strftime("%Y-%m")
        == current_month
    ]

    monthly_total = sum(
        expense.amount for expense in monthly_expenses
    )

    # Monthly budget
    budget = Budget.query.filter_by(
        month=current_month
    ).first()

    budget_amount = budget.amount if budget else 0

    remaining = budget_amount - monthly_total

    budget_percentage = (
        (monthly_total / budget_amount) * 100
        if budget_amount > 0 else 0
    )

    # Money leak detection
    leaks = detect_money_leaks(expenses)

    # Category analytics
    category_totals = defaultdict(float)

    for expense in expenses:
        category_totals[expense.category] += expense.amount

    chart_labels = list(category_totals.keys())
    chart_values = list(category_totals.values())

    # Saving recommendations
    saving_tips = generate_saving_tips(expenses)

    return render_template(
        "index.html",
        expenses=expenses,
        total=total,
        leaks=leaks,
        current_month=current_month,
        monthly_total=monthly_total,
        budget_amount=budget_amount,
        remaining=remaining,
        budget_percentage=budget_percentage,
        chart_labels=chart_labels,
        chart_values=chart_values,
        saving_tips=saving_tips
    )


# =====================================
# ADD EXPENSE
# =====================================

@app.route("/add", methods=["POST"])
def add_expense():

    title = request.form.get(
        "title", ""
    ).strip()

    category = request.form.get(
        "category", ""
    ).strip()

    try:
        amount = float(
            request.form.get("amount", "")
        )

        expense_date = datetime.strptime(
            request.form.get("expense_date", ""),
            "%Y-%m-%d"
        ).date()

        if (
            not title
            or not category
            or amount <= 0
        ):
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


# =====================================
# DELETE EXPENSE
# =====================================

@app.route(
    "/delete/<int:expense_id>",
    methods=["POST"]
)
def delete_expense(expense_id):

    expense = db.session.get(
        Expense,
        expense_id
    )

    if expense:
        db.session.delete(expense)
        db.session.commit()

        flash("Expense deleted successfully!")

    else:
        flash("Expense not found.")

    return redirect(url_for("home"))


# =====================================
# SET MONTHLY BUDGET
# =====================================

@app.route("/budget", methods=["POST"])
def set_budget():

    month = request.form.get(
        "month", ""
    ).strip()

    amount = request.form.get(
        "amount", ""
    )

    try:
        datetime.strptime(month, "%Y-%m")

        amount = float(amount)

        if amount <= 0:
            raise ValueError

    except (ValueError, TypeError):
        flash("Please enter a valid monthly budget.")
        return redirect(url_for("home"))

    budget = Budget.query.filter_by(
        month=month
    ).first()

    if budget:
        budget.amount = amount

    else:
        budget = Budget(
            month=month,
            amount=amount
        )

        db.session.add(budget)

    db.session.commit()

    flash("Monthly budget saved successfully!")

    return redirect(url_for("home"))


# =====================================
# DOWNLOAD MONTHLY EXPENSE REPORT
# =====================================

@app.route("/download-report")
def download_report():

    month = request.args.get(
        "month",
        date.today().strftime("%Y-%m")
    )

    try:
        datetime.strptime(month, "%Y-%m")

    except ValueError:
        flash("Invalid report month.")
        return redirect(url_for("home"))

    year = int(month[:4])
    month_number = int(month[5:7])

    expenses = Expense.query.filter(
        db.extract(
            "year",
            Expense.expense_date
        ) == year,

        db.extract(
            "month",
            Expense.expense_date
        ) == month_number

    ).order_by(
        Expense.expense_date.asc()
    ).all()

    output = io.StringIO()

    writer = csv.writer(output)

    writer.writerow([
        "Expense Name",
        "Amount",
        "Category",
        "Date"
    ])

    for expense in expenses:
        writer.writerow([
            expense.title,
            expense.amount,
            expense.category,
            expense.expense_date
        ])

    response = make_response(
        "\ufeff" + output.getvalue()
    )

    response.headers["Content-Type"] = (
        "text/csv; charset=utf-8"
    )

    response.headers["Content-Disposition"] = (
        f"attachment; filename=expense_report_{month}.csv"
    )

    return response


# =====================================
# APPLICATION START
# =====================================

if __name__ == "__main__":
    app.run(debug=True)
