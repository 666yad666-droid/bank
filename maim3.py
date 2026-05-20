# bank-python-app - версия 7 (с валидацией данных)

import re
from datetime import datetime


def get_timestamp():
    return datetime.now().strftime("%d.%m.%Y %H:%M:%S")


def add_to_history(user_data, operation, amount, recipient=None):
    time_str = get_timestamp()
    if recipient:
        record = f"[{time_str}] {operation}: {amount} руб. → {recipient}"
    else:
        record = f"[{time_str}] {operation}: {amount} руб."
    user_data["history"].append(record)


# ========== ФУНКЦИИ ПРОВЕРКИ ==========

def check_email(email):
    """Проверяет корректность email"""
    pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    return bool(re.match(pattern, email))


def check_phone(phone):
    """Проверяет номер телефона (+7XXXXXXXXXX)"""
    cleaned = re.sub(r'[\s\-\(\)]', '', phone)
    pattern = r"^\+7\d{10}$"
    return bool(re.match(pattern, cleaned))


def check_password(password):
    """Проверяет надёжность пароля"""
    if len(password) < 8:
        return False
    if not re.search(r'\d', password):
        return False
    if not re.search(r'[A-Z]', password):
        return False
    return True


# ========== ОСТАЛЬНЫЕ ФУНКЦИИ ==========

def show_balance(user_data):
    print(f"💰 Ваш баланс: {user_data['balance']:.2f} руб.")


def deposit(user_data):
    amount = int(input("Сумма пополнения: "))
    if amount <= 0:
        print("❌ Сумма должна быть положительной!")
        return user_data
    user_data["balance"] += amount
    add_to_history(user_data, "ПОПОЛНЕНИЕ", amount)
    print(f"✅ Счёт пополнен на {amount} руб.")
    return user_data


def withdraw(user_data):
    amount = int(input("Сумма снятия: "))
    if amount <= 0:
        print("❌ Сумма должна быть положительной!")
        return user_data
    if amount > user_data["balance"]:
        print("❌ Недостаточно средств!")
        return user_data
    user_data["balance"] -= amount
    add_to_history(user_data, "СНЯТИЕ", amount)
    print(f"✅ Снято {amount} руб.")
    return user_data


def transfer(user_data, users, sender_name):
    recipient = input("👤 Введите логин получателя: ")

    if recipient == sender_name:
        print("❌ Нельзя перевести самому себе!")
        return user_data, users

    if recipient not in users:
        print("❌ Пользователь не найден!")
        return user_data, users

    amount = int(input("💰 Сумма перевода: "))

    if amount <= 0:
        print("❌ Сумма должна быть положительной!")
        return user_data, users

    if amount > user_data["balance"]:
        print("❌ Недостаточно средств!")
        return user_data, users

    user_data["balance"] -= amount
    users[recipient]["balance"] += amount

    add_to_history(user_data, "ПЕРЕВОД", amount, recipient)
    add_to_history(users[recipient], "ПОЛУЧЕНИЕ", amount, sender_name)

    print(f"✅ Переведено {amount} руб. пользователю {recipient}")
    return user_data, users


def show_history(user_data):
    history = user_data.get("history", [])
    if not history:
        print("📭 История пуста")
        return
    print("\n📜 ИСТОРИЯ ОПЕРАЦИЙ:")
    print("-" * 50)
    for record in history[-10:]:  # последние 10
        print(record)
    print("-" * 50)


def bank_menu(username, user_data, users):
    bonus_balance = 0

    while True:
        print(f"\n🏦 Добро пожаловать, {username}!")
        print("1 - Баланс")
        print("2 - Пополнить")
        print("3 - Снять")
        print("4 - Перевести")
        print("5 - История операций")
        print("6 - Бонусы")
        print("7 - Выйти из аккаунта")
        print("8 - Настроить профиль")

        choice = input("Выберите действие: ")

        if choice == "1":
            show_balance(user_data)
            print(f"🎁 Бонусный счёт: {bonus_balance:.2f} руб.")
        elif choice == "2":
            user_data = deposit(user_data)
        elif choice == "3":
            user_data = withdraw(user_data)
        elif choice == "4":
            user_data, users = transfer(user_data, users, username)
        elif choice == "5":
            show_history(user_data)
        elif choice == "6":
            if bonus_balance <= 0:
                print("🎁 У вас нет бонусов!")
                continue
            print(f"🎁 У вас {bonus_balance:.2f} бонусных рублей.")
            use = input("Использовать бонусы? (да/нет): ")
            if use.lower() == "да":
                user_data["balance"] += bonus_balance
                add_to_history(user_data, "БОНУСЫ", bonus_balance)
                print(f"✅ Бонусы зачислены! Новый баланс: {user_data['balance']:.2f} руб.")
                bonus_balance = 0
        elif choice == "7":
            print(f"👋 До свидания, {username}!")
            return user_data, users
        elif choice == "8":
        else:
            print("❌ Неверный выбор!")


def login(users):
    login = input("👤 Введите логин: ")
    if login in users:
        print(f"✅ Добро пожаловать, {login}!")
        return login, users[login]
    else:
        print("❌ Пользователь не найден!")
        return None, None


def register(users):
    print("\n📝 РЕГИСТРАЦИЯ НОВОГО ПОЛЬЗОВАТЕЛЯ")

    login = input("Придумайте логин: ")
    if login in users:
        print("❌ Такой логин уже существует!")
        return users

    # Проверка email
    while True:
        email = input("Введите email: ")
        if check_email(email):
            break
        print("❌ Неверный email! Пример: user@mail.com")

    # Проверка телефона
    while True:
        phone = input("Введите телефон (+7 123 456-78-90): ")
        if check_phone(phone):
            break
        print("❌ Неверный телефон! Пример: +7 999 123-45-67")

    # Проверка пароля
    while True:
        password = input("Придумайте пароль (мин. 8 символов, цифра, заглавная буква): ")
        if check_password(password):
            break
        print("❌ Слабый пароль! Используйте 8+ символов, цифру и заглавную букву")

    # Создаём пользователя
    users[login] = {
        "balance": 0,
        "history": [f"[{get_timestamp()}] СИСТЕМА: аккаунт создан"],
        "email": email,
        "phone": phone
    }

    print(f"\n✅ Пользователь {login} создан!")
    print(f"📧 Email: {email}")
    print(f"📱 Телефон: {phone}")
    return users


def show_account_info(user_data):
    """Показывает информацию об аккаунте"""
    print("\n📋 ИНФОРМАЦИЯ ОБ АККАУНТЕ:")
    print("-" * 30)
    print(f"💰 Баланс: {user_data['balance']:.2f} руб.")
    print(f"📧 Email: {user_data.get('email', 'не указан')}")
    print(f"📱 Телефон: {user_data.get('phone', 'не указан')}")
    print(f"📊 Всего операций: {len(user_data.get('history', []))}")
    print("-" * 30)


def main():
    users = {
        "admin": {
            "balance": 10000,
            "history": [f"[{get_timestamp()}] СИСТЕМА: аккаунт создан"],
            "email": "admin@bank.com",
            "phone": "+7 999 123-45-67"
        }
    }

    while True:
        print("\n🏦 Банк 'Ученик'")
        print("1 - Вход")
        print("2 - Регистрация")
        print("3 - Выход")

        choice = input("Выберите действие: ")

        if choice == "1":
            username, user_data = login(users)
            if username:
                updated_user, updated_users = bank_menu(username, user_data, users)
                users[username] = updated_user
                users = updated_users
        elif choice == "2":
            users = register(users)
        elif choice == "3":
            print("👋 До свидания!")
            break
        else:
            print("❌ Неверный выбор!")


if __name__ == "__main__":
    main()