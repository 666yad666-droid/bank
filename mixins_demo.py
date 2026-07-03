# mixins_demo.py — демонстрация миксинов

from datetime import datetime
from abc import ABC, abstractmethod


# ========== МИКСИНЫ ==========

class LoggerMixin:
    """
    Миксин для логирования.
    Добавляет метод log() и сохраняет историю сообщений.
    """

    def __init__(self, *args, **kwargs):
        # 🔑 Важно! super() вызывает __init__ следующего класса в цепочке
        super().__init__(*args, **kwargs)
        self._logs = []

    def log(self, message):
        timestamp = datetime.now().strftime("%H:%M:%S")
        log_entry = f"[{timestamp}] {message}"
        self._logs.append(log_entry)
        print(f"📝 {log_entry}")

    def show_logs(self, last_n=5):
        if not self._logs:
            print("Нет записей в логе")
            return
        print("\n📜 ПОСЛЕДНИЕ ЗАПИСИ:")
        for log in self._logs[-last_n:]:
            print(f"   {log}")


class BonusMixin:
    """
    Миксин для бонусной системы.
    Добавляет бонусный счёт и методы для работы с бонусами.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._bonus_balance = 0
        self._bonus_rate = 0.01  # 1% бонуса от пополнения

    def calculate_bonus(self, amount):
        return amount * self._bonus_rate

    def add_bonus(self, amount):
        bonus = self.calculate_bonus(amount)
        self._bonus_balance += bonus
        return bonus

    def get_bonus_balance(self):
        return self._bonus_balance

    def use_bonus(self):
        if self._bonus_balance <= 0:
            raise ValueError("Нет бонусов!")
        return self._bonus_balance


class InterestMixin:
    """
    Миксин для начисления процентов.
    Добавляет процентную ставку и метод начисления процентов.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._interest_rate = 0.01  # 1% годовых

    def set_interest_rate(self, rate):
        self._interest_rate = rate

    def calculate_interest(self, balance):
        return balance * self._interest_rate


class ValidationMixin:
    """
    Миксин для проверки данных.
    Добавляет статические методы для валидации.
    """

    @staticmethod
    def validate_card(card_number):
        return len(card_number) == 16 and card_number.isdigit()

    @staticmethod
    def validate_phone(phone):
        import re
        cleaned = re.sub(r'[\s\-\(\)]', '', phone)
        return bool(re.match(r"^\+7\d{10}$", cleaned))

    @staticmethod
    def validate_email(email):
        import re
        pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        return bool(re.match(pattern, email))


# ========== ОСНОВНОЙ КЛАСС (СОБИРАЕТ ВСЕ МИКСИНЫ) ==========

class BankAccount(LoggerMixin, BonusMixin, InterestMixin, ValidationMixin):
    """
    Банковский счёт, собранный из миксинов.
    Порядок наследования важен! MRO будет:
    BankAccount → LoggerMixin → BonusMixin → InterestMixin → ValidationMixin → object
    """

    def __init__(self, owner, balance=0):
        # 🔑 super() вызывает __init__ следующего класса в MRO
        # Благодаря этому все миксины инициализируются автоматически
        super().__init__()
        self.owner = owner
        self._balance = balance
        self.log(f"Создан счёт для {owner} с балансом {balance}")

    @property
    def balance(self):
        return self._balance

    def deposit(self, amount):
        if amount <= 0:
            self.log("❌ Ошибка: сумма должна быть положительной!")
            return

        self._balance += amount
        bonus = self.add_bonus(amount)
        self.log(f"✅ Пополнение: +{amount} руб. (бонус: +{bonus:.2f} руб.)")

    def withdraw(self, amount):
        if amount <= 0:
            self.log("❌ Ошибка: сумма должна быть положительной!")
            return
        if amount > self._balance:
            self.log("❌ Ошибка: недостаточно средств!")
            return

        self._balance -= amount
        self.log(f"💰 Снятие: -{amount} руб.")

    def apply_interest(self):
        interest = self.calculate_interest(self._balance)
        self._balance += interest
        self.log(f"📈 Начислены проценты: +{interest:.2f} руб. (ставка {self._interest_rate * 100}%)")

    def show_info(self):
        print(f"\n🏦 СЧЁТ: {self.owner}")
        print(f"💰 Баланс: {self.balance:.2f} руб.")
        print(f"🎁 Бонусы: {self.get_bonus_balance():.2f} руб.")
        print(f"📈 Процентная ставка: {self._interest_rate * 100}%")

    def __str__(self):
        return f"BankAccount(owner='{self.owner}', balance={self.balance})"


# ========== ДЕМОНСТРАЦИЯ ==========

print("🏦 БАНК С ИСПОЛЬЗОВАНИЕМ МИКСИНОВ")
print("=" * 50)

# Проверка валидации (статический метод из ValidationMixin)
print("\n--- Валидация (из ValidationMixin) ---")
print(f"Номер карты '1234567890123456': {BankAccount.validate_card('1234567890123456')}")
print(f"Телефон '+7 999 123-45-67': {BankAccount.validate_phone('+7 999 123-45-67')}")
print(f"Email 'user@mail.com': {BankAccount.validate_email('user@mail.com')}")

# Создаём счёт
print("\n--- Создание счёта ---")
account = BankAccount("Алиса", 5000)

# Выполняем операции
print("\n--- Операции ---")
account.deposit(1000)
account.withdraw(200)
account.apply_interest()

# Показываем информацию
print("\n--- Информация о счёте ---")
account.show_info()

# Показываем логи
account.show_logs()

print("\n" + "=" * 50)
print(account)