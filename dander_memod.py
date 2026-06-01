# magic_methods_demo.py — демонстрация магических методов

class BankAccount:
    """Класс банковского счёта с магическими методами"""

    bank_name = "Банк 'Ученик'"

    def __init__(self, owner, balance=0):
        self.owner = owner
        self.balance = balance
        print(f"🏦 Создан счёт для {self.owner}")

    # МАГИЧЕСКИЕ МЕТОДЫ

    def __str__(self):
        """
        Вызывается при print(объект) и str(объект)
        Должен возвращать понятное человеку описание
        """
        return f"Счёт владельца {self.owner} | Баланс: {self.balance} руб."

    def __repr__(self):
        """
        Вызывается при repr(объект) и в консоли Python
        Должен возвращать "техническое" представление,
        по которому можно воссоздать объект
        """
        return f"BankAccount('{self.owner}', {self.balance})"

    def __add__(self, other):
        """
        Вызывается при obj1 + obj2
        Позволяет складывать объекты банковских счетов

        isinstance(other, BankAccount) — проверяет, является ли other
        объектом класса BankAccount (или его наследником)

        isinstance(other, (int, float)) — проверяет, является ли other
        целым числом или числом с плавающей точкой
        """
        if isinstance(other, BankAccount):
            # Случай: счёт + счёт → возвращаем сумму балансов
            return self.balance + other.balance
        elif isinstance(other, (int, float)):
            # Случай: счёт + число → возвращаем сумму баланса и числа
            return self.balance + other
        else:
            # Неподдерживаемый тип — возвращаем NotImplemented
            return NotImplemented

    def __eq__(self, other):
        """Вызывается при obj1 == obj2"""
        if isinstance(other, BankAccount):
            return self.balance == other.balance
        return False

    def __lt__(self, other):
        """Вызывается при obj1 < obj2"""
        if isinstance(other, BankAccount):
            return self.balance < other.balance
        return False


# Демонстрация работы
print("=" * 50)
print("🏦 ДЕМОНСТРАЦИЯ МАГИЧЕСКИХ МЕТОДОВ")
print("=" * 50)

# Создаём счета
account1 = BankAccount("Алиса", 5000)
account2 = BankAccount("Боб", 3000)

print("\n--- Методы __str__ и __repr__ ---")
print(f"str(account1): {str(account1)}")
print(f"repr(account1): {repr(account1)}")
print(f"Просто print(account1): {account1}")

print("\n--- Метод __add__ с isinstance ---")
print(f"Сложение с другим счётом: {account1 + account2} руб.")
print(f"Сложение с числом: {account1 + 1000} руб.")
#print(f"Попытка сложить с неподдерживаемым типом: {account1 + 'строка'}")

print("\n--- Метод __eq__ и __lt__ ---")
print(f"account1 == account2: {account1 == account2}")
print(f"account1 < account2: {account1 < account2}")