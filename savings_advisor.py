
from collections import defaultdict


def generate_saving_tips(expenses):
    tips = []

    category_totals = defaultdict(float)
    category_counts = defaultdict(int)

    for expense in expenses:
        category_totals[expense.category] += expense.amount
        category_counts[expense.category] += 1

    # Find the highest spending category
    if category_totals:
        highest_category = max(
            category_totals,
            key=category_totals.get
        )

        total = category_totals[highest_category]

        tips.append({
            "title": "Highest Spending Category",
            "message": (
                f"You spent ₹{total:.2f} "
                f"on {highest_category}."
            ),
            "suggestion": (
                f"Review your {highest_category} expenses "
                "and consider setting a spending limit."
            )
        })

    # Detect frequently purchased items
    repeated_items = defaultdict(int)

    for expense in expenses:
        repeated_items[expense.title.lower()] += 1

    for item, count in repeated_items.items():
        if count >= 3:
            tips.append({
                "title": "Frequent Purchases",
                "message": (
                    f"You purchased {item.title()} "
                    f"{count} times."
                ),
                "suggestion": (
                    "Consider whether you can reduce "
                    "the frequency of this purchase."
                )
            })

    # Identify accumulated small purchases
    small_expenses = [
        expense for expense in expenses
        if expense.amount <= 200
    ]

    small_total = sum(
        expense.amount for expense in small_expenses
    )

    if len(small_expenses) >= 5:
        tips.append({
            "title": "Small Expenses Add Up",
            "message": (
                f"Your small purchases total "
                f"₹{small_total:.2f}."
            ),
            "suggestion": (
                "Review these purchases and identify "
                "which ones you can avoid."
            )
        })

    if not tips:
        tips.append({
            "title": "Good Spending Habits",
            "message": "Not enough spending patterns detected yet.",
            "suggestion": (
                "Continue recording expenses to receive "
                "personalized saving suggestions."
            )
        })

    return tips
