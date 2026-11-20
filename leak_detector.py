
from collections import defaultdict


def detect_money_leaks(expenses):

    leaks = []

    # =================================
    # 1. DETECT REPEATED PURCHASES
    # =================================

    repeated_items = defaultdict(list)

    for expense in expenses:

        name = expense.title.strip().lower()

        repeated_items[name].append(expense)

    for name, items in repeated_items.items():

        if len(items) >= 3:

            total = sum(
                item.amount for item in items
            )

            leaks.append({

                "type": "Repeated Spending",

                "title": name.title(),

                "message": (
                    f"You purchased {name.title()} "
                    f"{len(items)} times."
                ),

                "total": round(total, 2),

                "count": len(items)

            })


    # =================================
    # 2. DETECT SMALL EXPENSE LEAKS
    # =================================

    small_expenses = [

        expense for expense in expenses

        if expense.amount <= 200

    ]

    small_total = sum(

        expense.amount
        for expense in small_expenses

    )

    if (
        len(small_expenses) >= 5
        and small_total >= 1000
    ):

        leaks.append({

            "type": "Small Expense Leak",

            "title": "Small Expenses Adding Up",

            "message": (
                f"You made {len(small_expenses)} "
                "small purchases."
            ),

            "total": round(small_total, 2),

            "count": len(small_expenses)

        })


    # =================================
    # 3. DETECT HIGH CATEGORY SPENDING
    # =================================

    category_totals = defaultdict(float)

    category_counts = defaultdict(int)

    for expense in expenses:

        category = expense.category

        category_totals[category] += expense.amount

        category_counts[category] += 1

    for category, total in category_totals.items():

        if total >= 5000:

            leaks.append({

                "type": "High Category Spending",

                "title": category,

                "message": (
                    f"Your spending in {category} "
                    "has reached ₹5,000 or more."
                ),

                "total": round(total, 2),

                "count": category_counts[category]

            })


    return leaks
