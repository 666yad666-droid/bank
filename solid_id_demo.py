# solid_id_demo.py — демонстрация принципов I и D, функции hasattr

from datetime import datetime
from abc import ABC, abstractmethod


# ========== ПРИНЦИП I: РАЗДЕЛЯЕМ ИНТЕРФЕЙСЫ ==========
class InterestBearing(ABC):
    @abstractmethod
    def get_interest_rate(self):
        pass


class BonusBearing(ABC):
    @abstractmethod
    def get_bonus_percent(self):
        pass


class Named(ABC):
    @abstractmethod
    def get_name(self):
        pass


class RegularAccount(InterestBearing, BonusBearing, Named):
    def get_interest_rate(self): return 0.01

    def get_bonus_percent(self): return 0.01

    def get_name(self): return "Обычный"


class SimpleAccount(InterestBearing, Named):
    """Простой счёт — ТОЛЬКО проценты, без бонусов"""

    def get_interest_rate(self): return 0.005

    def get_name(self): return "Простой"
    # нет метода get_bonus_percent — он ему не нужен!


# ========== ПРИНЦИП D: ИНВЕРСИЯ ЗАВИСИМОСТЕЙ ==========
class Logger(ABC):
    @abstractmethod
    def log(self, message):
        pass


class ConsoleLogger(Logger):
    def log(self, message):
        print(f"📝 {message}")


class FileLogger(Logger):
    def __init__(self, filename="bank.log"):
        self.filename = filename

    def log(self, message):
        with open(self.filename, "a", encoding="utf-8") as f:
            f.write(f"{datetime.now()} - {message}\n")
        print(f"💾 Записано в файл {self.filename}")


class SilentLogger(Logger):
    def log(self, message):
        pass


# ========== КЛАСС БАЛАНС ==========
class Balance:
    def __init__(self, logger: Logger, initial_balance=0):
        self._logger = logger
        self._balance = initial_balance
        self._bonus_balance = 0
        self._logger.log(f"Создан баланс: {initial_balance} руб.")

    def deposit(self, amount, bonus_percent=0):
        if amount <= 0:
            raise ValueError("Сумма должна быть положительной!")
        self._balance += amount
        self._logger.log(f"Пополнение на {amount} руб.")

        if bonus_percent > 0:
            bonus = amount * bonus_percent
            self._bonus_balance += bonus
            self._logger.log(f"Начислено бонусов: {bonus:.2f} руб.")
            return bonus
        return 0

    def withdraw(self, amount):
        if amount <= 0:
            raise ValueError("Сумма должна быть положительной!")
        if amount > self._balance:
            raise ValueError("Недостаточно средств!")
        self._balance -= amount
        self._logger.log(f"Снятие {amount} руб.")
        return amount

    def get_balance(self):
        return self._balance

    def get_bonus_balance(self):
        return self._bonus_balance


# ========== ОСНОВНОЙ КЛАСС ==========
class BankAccount:
    def __init__(self, name, email, phone, account_type, logger: Logger, initial_balance=0):
        self.name = name
        self.email = email
        self.phone = phone
        self._account_type = account_type
        self._balance = Balance(logger, initial_balance)
        self._logger = logger
        self._created_at = datetime.now()

        # 🔑 hasattr — проверяем, есть ли у типа счёта метод get_name
        # Не все типы счетов его имеют, поэтому сначала проверяем
        account_name = self._get_account_name()
        self._logger.log(f"Создан {account_name} счёт для {name}")
        print(f"🏦 Создан {account_name} счёт для {self.name}")

    def _get_account_name(self):
        """
        🔑 Безопасно получаем название счёта.
        Сначала проверяем, есть ли у объекта метод get_name.
        Если есть — вызываем, если нет — возвращаем "Неизвестный".
        """
        if hasattr(self._account_type, 'get_name'):
            return self._account_type.get_name()
        return "Неизвестный"

    def deposit(self, amount):
        # 🔑 Проверяем, есть ли у типа счёта метод get_bonus_percent
        bonus_percent = 0
        if hasattr(self._account_type, 'get_bonus_percent'):
            bonus_percent = self._account_type.get_bonus_percent()

        try:
            bonus = self._balance.deposit(amount, bonus_percent)
            print(f"✅ Пополнено {amount} руб.")
            if bonus > 0:
                print(f"🎁 Начислено бонусов: {bonus:.2f} руб.")
        except ValueError as e:
            print(f"❌ Ошибка: {e}")

    def withdraw(self, amount):
        try:
            withdrawn = self._balance.withdraw(amount)
            print(f"✅ Снято {withdrawn} руб.")
        except ValueError as e:
            print(f"❌ Ошибка: {e}")

    def show_balance(self):
        print(f"\n💰 Баланс: {self._balance.get_balance():.2f} руб.")
        print(f"🎁 Бонусный счёт: {self._balance.get_bonus_balance():.2f} руб.")

    def __str__(self):
        return (f"🏦 Счёт: {self.name} ({self._get_account_name()})\n"
                f"💰 Баланс: {self._balance.get_balance():.2f} руб.")


# Демонстрация
print("🏦 БАНК С SOLID (Принципы I и D)")
print("=" * 50)

console_logger = ConsoleLogger()

print("\n--- Обычный счёт (есть бонусы и название) ---")
account1 = BankAccount("Алиса", "alice@mail.com", "+7 999 111-22-33",
                       RegularAccount(), console_logger, 5000)
account1.deposit(1000)
account1.withdraw(200)
account1.show_balance()

print("\n--- Простой счёт (без бонусов, но с названием) ---")
account2 = BankAccount("Борис", "boris@mail.com", "+7 999 444-55-66",
                       SimpleAccount(), console_logger, 10000)
account2.deposit(1000)  # бонусов не будет, т.к. метод get_bonus_percent отсутствует
account2.show_balance()