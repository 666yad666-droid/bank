# oop_demo.py — первое знакомство с классами

class BankAccount:
    """
    Класс для банковского счёта
    """

    def __init__(self, owner, initial_balance=0):
        """
        Конструктор класса. Вызывается при создании объекта.

        Параметры:
        - owner: владелец счёта (строка)
        - initial_balance: начальный баланс (по умолчанию 0)
        """
        self.owner = owner
        self.balance = initial_balance
        print(f"🏦 Создан счёт для {self.owner} с балансом {self.balance} руб.")

    def deposit(self, amount):
        """Пополнение счёта"""
        if amount <= 0:
            print("❌ Сумма должна быть положительной!")
            return
        self.balance += amount
        print(f"✅ Пополнено {amount} руб. Баланс: {self.balance} руб.")

    def withdraw(self, amount):
        """Снятие денег со счёта"""
        if amount <= 0:
            print("❌ Сумма должна быть положительной!")
            return
        if amount > self.balance:
            print("❌ Недостаточно средств!")
            return
        self.balance -= amount
        print(f"✅ Снято {amount} руб. Баланс: {self.balance} руб.")

    def show_balance(self):
        """Показать текущий баланс"""
        print(f"💰 Баланс {self.owner}: {self.balance} руб.")

    def transfer(self, other_account, amount):
        """Перевод денег на другой счёт"""
        if amount <= 0:
            print("❌ Сумма должна быть положительной!")
            return
        if amount > self.balance:
            print("❌ Недостаточно средств для перевода!")
            return

        self.balance -= amount
        other_account.balance += amount
        print(f"✅ Переведено {amount} руб. со счёта {self.owner} на счёт {other_account.owner}")

    def add_interest(self, rate):
        if rate <= 0:
            print("❌ Сумма должна быть положительной!")
        self.balance += (self.balance / 100 * rate)
        print(f"✅ Пополнено на {rate} %. Баланс: {self.balance} руб.")


# Демонстрация работы
print("=" * 50)
print("🏦 ДЕМОНСТРАЦИЯ РАБОТЫ КЛАССА BankAccount")
print("=" * 50)

# Создаём два счёта
account1 = BankAccount("Анна", 5000)
account2 = BankAccount("Борис", 3000)

print("\n--- Операции со счётом Анны ---")
account1.show_balance()
account1.deposit(1000)
account1.withdraw(500)
account1.show_balance()

print("\n--- Перевод между счетами ---")
account1.transfer(account2, 2000)
account1.show_balance()
account2.show_balance()

print("\n--- Ошибочные операции ---")
account1.withdraw(10000)  # недостаточно средств
account1.deposit(-100)  # отрицательная сумма

print("\n--- test ---")
account1.show_balance()
account1.add_interest(5)
