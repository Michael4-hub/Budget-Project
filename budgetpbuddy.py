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


def main():
    transactions = load_transactions()

    while True:
        print("===== BudgetBuddy =====")
        print("1. Add transaction")
        print("2. View transactions")
        print("3. Exit")
        choice = input("Выберите пункт меню: ").strip()

        if choice == "1":
            add_transaction(transactions)
        elif choice == "2":
            view_transactions(transactions)
        elif choice == "3":
            print("До встречи!")
            break
        else:
            print("Неверный выбор, попробуйте снова\n")


if __name__ == "__main__":
    main()
        
