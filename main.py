# bank-python-app - версия 4 (с пользователями)
from selenium.webdriver import Proxy


def show_balance(balance):
    print(f"💰 Ваш баланс: {balance} руб.")


def deposit(balance):
    amount = int(input("Сумма пополнения: "))
    if amount <= 0:
        print("❌ Сумма должна быть положительной!")
        return balance
    balance += amount
    bonus = amount / 100
    print(f"✅ Счёт пополнен на {amount} руб. Появилось {bonus} бонусов.")
    return balance, bonus


def withdraw(balance):
    amount = int(input("Сумма снятия: "))
    if amount <= 0:
        print("❌ Сумма должна быть положительной!")
        return balance
    if amount > balance:
        print("❌ Недостаточно средств!")
        return balance
    balance -= amount
    print(f"✅ Снято {amount} руб.")
    return balance


def login(users):
    """Вход пользователя"""
    login = input("👤 Введите логин: ")
    if login in users:
        print(f"✅ Добро пожаловать, {login}!")
        return login, users[login]
    else:
        print("❌ Пользователь не найден!")
        return None, None


def register(users):
    """Регистрация нового пользователя"""
    login = input("📝 Придумайте логин: ")
    if login in users:
        print("❌ Такой логин уже существует!")
        return users
    users[login] = 0
    print(f"✅ Пользователь {login} создан!")
    return users


def bank_menu(username, balance):
    """Меню банковских операций"""
    while True:
        print(f"\n🏦 Добро пожаловать, {username}!")
        print("1 - Баланс")
        print("2 - Пополнить")
        print("3 - Снять")
        print("4 - Выйти из аккаунта")
        print("5 - Бонусы")

        choice = input("Выберите действие: ")

        if choice == "1":
            show_balance(balance)
        elif choice == "2":
            balance = deposit(balance)
        elif choice == "3":
            balance = withdraw(balance)
        elif choice == "4":
            print(f"👋 До свидания, {username}!")
            return balance
        elif choice == "5":
            print('1 - Баланс бонусов')
            print('2 - Вывов бонусов')
            choice
        else:
            print("❌ Неверный выбор!")


def main():
    users = {"admin": 10000}  # начальный пользователь

    while True:
        print("\n🏦 Банк 'Ученик'")
        print("1 - Вход")
        print("2 - Регистрация")
        print("3 - Выход")

        choice = input("Выберите действие: ")

        if choice == "1":
            username, balance = login(users)
            if username:
                new_balance = bank_menu(username, balance)
                users[username] = new_balance
        elif choice == "2":
            users = register(users)
        elif choice == "3":
            print("👋 До свидания!")
            break
        else:
            print("❌ Неверный выбор!")


if __name__ == "__main__":
    main()