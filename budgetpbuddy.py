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


def main():
    transactions = load_transactions()

    while True:
        print("===== BudgetBuddy =====")
        print("1. Add transaction")
        print("2. Exit")
        choice = input("Выберите пункт меню: ").strip()

        if choice == "1":
            add_transaction(transactions)
        elif choice == "2":
            print("До встречи!")
            break
        else:
            print("Неверный выбор, попробуйте снова\n")


if __name__ == "__main__":
    main()
