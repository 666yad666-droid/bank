# regex_demo.py — демонстрация регулярных выражений

import re


def check_email(email):
    """Проверяет корректность email"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z]+\.[a-zA-Z]{2,}$'
    if re.match(pattern, email):
        return True
    return False


def check_phone(phone):
    """Проверяет номер телефона (+7 123 456-78-90)"""
    # Удаляем все пробелы и дефисы
    cleaned = re.sub(r'[\s\-\(\)]', '', phone)
    pattern = r"^\+7\d{10}$"
    if re.match(pattern, cleaned):
        return True
    return False


def check_card_number(card):
    """Проверяет номер карты (16 цифр, может быть с пробелами)"""
    cleaned = re.sub(r'\s', '', card)
    pattern = r"^\d{16}$"
    if re.match(pattern, cleaned):
        return True
    return False


def main():
    print("🏦 Проверка данных банка")

    while True:
        print("\n1 - Проверить email")
        print("2 - Проверить телефон")
        print("3 - Проверить номер карты")
        print("4 - Выйти")

        choice = input("Выберите действие: ")

        if choice == "1":
            email = input("Введите email: ")
            if check_email(email):
                print("✅ Email корректен!")
            else:
                print("❌ Неверный email!")

        elif choice == "2":
            phone = input("Введите телефон (+7 123 456-78-90): ")
            if check_phone(phone):
                print("✅ Телефон корректен!")
            else:
                print("❌ Неверный телефон!")

        elif choice == "3":
            card = input("Введите номер карты (16 цифр): ")
            if check_card_number(card):
                print("✅ Номер карты корректен!")
            else:
                print("❌ Неверный номер карты!")

        elif choice == "4":
            print("👋 До свидания!")
            break
        else:
            print("❌ Неверный выбор!")


if __name__ == "__main__":
    main()