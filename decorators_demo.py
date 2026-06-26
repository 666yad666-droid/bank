# decorators_demo.py — демонстрация декораторов

from datetime import datetime
from dataclasses import dataclass
from typing import List


# ========== @dataclass — класс для хранения данных ==========
@dataclass
class Transaction:
    """Одна операция в истории"""
    date: str
    type: str
    amount: float
    bonus: float = 0.0

    def __str__(self):
        if self.bonus > 0:
            return f"[{self.date}] {self.type}: {self.amount} руб. (бонус: {self.bonus:.2f})"
        return f"[{self.date}] {self.type}: {self.amount} руб."


@dataclass
class User:
    """
    Данные пользователя

    🔑 Почему created_at: str = None, а не текущая дата сразу?

    Если написать:
        created_at: str = datetime.now().strftime(...)
    то дата зафиксируется в момент ЗАГРУЗКИ класса (когда программа запускается),
    а не в момент создания каждого пользователя. Все пользователи получат
    ОДНУ И ТУ ЖЕ дату (время запуска программы)!

    Поэтому мы ставим None как маркер "дата не задана",
    а в __post_init__ создаём текущую дату для КАЖДОГО нового объекта.
    """
    name: str
    email: str
    phone: str
    created_at: str = None

    def __post_init__(self):
        """Вызывается автоматически после __init__"""
        if self.created_at is None:
            self.created_at = datetime.now().strftime("%d.%m.%Y %H:%M:%S")


# ========== КЛАСС БАЛАНС ==========
class Balance:
    def __init__(self, initial_balance=0):
        self._balance = initial_balance
        self._bonus_balance = 0

    @property
    def balance(self):
        """Читаем баланс"""
        return self._balance

    @balance.setter
    def balance(self, value):
        """Устанавливаем баланс с проверкой"""
        if value < 0:
            raise ValueError("Баланс не может быть отрицательным!")
        self._balance = value

    @property
    def bonus_balance(self):
        return self._bonus_balance

    def add_bonus(self, amount):
        self._bonus_balance += amount


# ========== ОСНОВНОЙ КЛАСС ==========
class BankAccount:
    _total_accounts = 0

    def __init__(self, user: User, initial_balance=0):
        """
        🔑 Аннотация user: User — это ПОДСКАЗКА.
        Она не запрещает передать что-то другое, но помогает редактору кода
        и программисту понять, что ожидается объект типа User.
        """
        self.user = user
        self._balance = Balance(initial_balance)
        self._transactions: List[Transaction] = []
        BankAccount._total_accounts += 1
        print(f"🏦 Создан счёт для {self.user.name}")

    @classmethod
    def get_total_accounts(cls):
        """Классовый метод — возвращает количество аккаунтов"""
        return cls._total_accounts

    @staticmethod
    def validate_card(card: str) -> bool:
        """Статический метод — проверяет номер карты (16 цифр)"""
        return len(card) == 16 and card.isdigit()

    def deposit(self, amount: float):
        if amount <= 0:
            print("❌ Сумма должна быть положительной!")
            return

        self._balance.balance += amount
        bonus = amount * 0.01
        self._balance.add_bonus(bonus)

        timestamp = datetime.now().strftime("%d.%m.%Y %H:%M:%S")
        self._transactions.append(Transaction(timestamp, "ПОПОЛНЕНИЕ", amount, bonus))
        print(f"✅ Пополнено {amount} руб.")
        print(f"🎁 Начислено бонусов: {bonus:.2f} руб.")

    def withdraw(self, amount: float):
        if amount <= 0:
            print("❌ Сумма должна быть положительной!")
            return
        if amount > self._balance.balance:
            print("❌ Недостаточно средств!")
            return

        self._balance.balance -= amount
        timestamp = datetime.now().strftime("%d.%m.%Y %H:%M:%S")
        self._transactions.append(Transaction(timestamp, "СНЯТИЕ", amount))
        print(f"✅ Снято {amount} руб.")

    @property
    def balance(self):
        """
        🔑 Свойство — позволяет обращаться к балансу как к обычной переменной,
        но внутри вызывает метод get_balance() из класса Balance.
        """
        return self._balance.balance

    @property
    def bonus_balance(self):
        return self._balance.bonus_balance

    def show_balance(self):
        print(f"\n💰 Баланс {self.user.name}: {self.balance:.2f} руб.")
        print(f"🎁 Бонусный счёт: {self.bonus_balance:.2f} руб.")

    def show_transactions(self, last_n=5):
        if not self._transactions:
            print("📭 История пуста")
            return
        print(f"\n📜 ПОСЛЕДНИЕ ОПЕРАЦИИ ({self.user.name}):")
        print("-" * 50)
        for t in self._transactions[-last_n:]:
            print(t)
        print("-" * 50)

    def __str__(self):
        return (f"🏦 Счёт: {self.user.name}\n"
                f"💰 Баланс: {self.balance:.2f} руб.\n"
                f"🎁 Бонусы: {self.bonus_balance:.2f} руб.")


# Демонстрация
print("🏦 БАНК С ДЕКОРАТОРАМИ")
print("=" * 50)

# Статический метод — вызываем от класса, без создания объекта
print(f"Проверка карты '1234567890123456': {BankAccount.validate_card('1234567890123456')}")

# Классовый метод
print(f"Всего аккаунтов: {BankAccount.get_total_accounts()}")

# Создаём пользователя и аккаунт
user = User("Алиса", "alice@mail.com", "+7 999 111-22-33")
print(f"Создан пользователь: {user}")

account = BankAccount(user, 5000)
print(f"Всего аккаунтов: {BankAccount.get_total_accounts()}")

account.deposit(1000)
account.withdraw(200)
account.show_balance()
account.show_transactions()

print("\n" + "=" * 50)
print(account)