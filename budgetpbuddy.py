import json
import os
from datetime import date

FILENAME = "transactions.json"
CATEGORIES = ["Food", "Transport", "Bills", "Shopping", "Entertainment", "Other"]


def load_transactions():
    if not os.path.exists(FILENAME):
        return []
    with open(FILENAME, "r") as f:
        return json.load(f)


def save_transactions(transactions):
    with open(FILENAME, "w") as f:
        json.dump(transactions, f, indent=2)


def add_transaction(transactions):

    while True:
        t_type = input("Тип (Income/Expense): ").strip().capitalize()
        if t_type in ("Income", "Expense"):
            break
        print("Ошибка: введите Income или Expense")

    print("Доступные категории:", ", ".join(CATEGORIES))
    while True:
        category = input("Категория: ").strip().capitalize()
        if category in CATEGORIES:
            break
        print("Ошибка: выберите категорию из списка")

    description = input("Описание: ").strip()
    while description == "":
        print("Описание не может быть пустым")
        description = input("Описание: ").strip()

    while True:
        raw_amount = input("Сумма: ").strip()
        try:
            amount = float(raw_amount)
            if amount <= 0:
                print("Ошибка: сумма должна быть больше нуля")
                continue
            break
        except ValueError:
            print("Ошибка: введите корректное число")

    today = str(date.today())

    transaction = {
        "date": today,
        "type": t_type,
        "category": category,
        "description": description,
        "amount": amount
    }

    transactions.append(transaction)
    save_transactions(transactions)
    print("Транзакция добавлена!\n")


def view_transactions(transactions):
    if not transactions:
        print("No transactions found.\n")
        return

    sorted_transactions = sorted(
        transactions,
        key=lambda t: (t["date"], t["type"], t["category"], t["description"], t["amount"])
    )

    print(f"{'DATE':<12}{'TYPE':<10}{'CATEGORY':<12}{'DESCRIPTION':<20}{'AMOUNT':>8}")
    print("-" * 62)
    for t in sorted_transactions:
        print(f"{t['date']:<12}{t['type']:<10}{t['category']:<12}{t['description']:<20}{t['amount']:>8.2f}")
    print()


def calculate_summary(transactions):
    if not transactions:
        print("Total Income: 0.00")
        print("Total Expenses: 0.00")
        print("Net Balance: 0.00")
        print("Largest Income: 0.00")
        print("Largest Expense: 0.00")
        print("Total Transactions: 0\n")
        return

    total_income = 0
    total_expenses = 0
    largest_income = 0
    largest_expense = 0

    for t in transactions:
        if t["type"] == "Income":
            total_income += t["amount"]
            if t["amount"] > largest_income:
                largest_income = t["amount"]
        elif t["type"] == "Expense":
            total_expenses += t["amount"]
            if t["amount"] > largest_expense:
                largest_expense = t["amount"]

    net_balance = total_income - total_expenses

    print(f"Total Income: {total_income:.2f}")
    print(f"Total Expenses: {total_expenses:.2f}")
    print(f"Net Balance: {net_balance:.2f}")
    print(f"Largest Income: {largest_income:.2f}")
    print(f"Largest Expense: {largest_expense:.2f}")
    print(f"Total Transactions: {len(transactions)}\n")


def category_breakdown(transactions):
    expenses = [t for t in transactions if t["type"] == "Expense"]

    if not expenses:
        print("No expenses recorded yet.\n")
        return

    totals_by_category = {}
    for t in expenses:
        category = t["category"]
        if category not in totals_by_category:
            totals_by_category[category] = 0
        totals_by_category[category] += t["amount"]

    total_spent = sum(totals_by_category.values())

    sorted_categories = sorted(totals_by_category.items(), key=lambda item: item[1], reverse=True)

    for category, amount in sorted_categories:
        percentage = (amount / total_spent) * 100
        print(f"{category:<15}: {amount:.2f} ({percentage:.0f}%)")
    print()


def main():
    transactions = load_transactions()

    while True:
        print("===== BudgetBuddy =====")
        print("1. Add transaction")
        print("2. View transactions")
        print("3. View summary")
        print("4. Category analysis")
        print("5. Exit")
        choice = input("Выберите пункт меню: ").strip()

        if choice == "1":
            add_transaction(transactions)
        elif choice == "2":
            view_transactions(transactions)
        elif choice == "3":
            calculate_summary(transactions)
        elif choice == "4":
            category_breakdown(transactions)
        elif choice == "5":
            print("До встречи!")
            break
        else:
            print("Неверный выбор, попробуйте снова\n")


if __name__ == "__main__":
    main()
    
