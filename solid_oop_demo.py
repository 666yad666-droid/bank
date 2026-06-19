# solid_oop_dem.py — SOLID: O и L с ABC

from datetime import datetime
from solid_oop_demo import ABC, abstractmethod


# ========== АБСТРАКТНЫЙ БАЗОВЫЙ КЛАСС ДЛЯ ТИПА СЧЁТА ==========
class AccountType(ABC):
    """
    Абстрактный класс — шаблон для всех типов счетов.
    Нельзя создать объект этого класса — только наследоваться.

    Зачем это нужно?
    - Задаёт "контракт": каждый тип счёта ОБЯЗАН уметь возвращать
      процентную ставку, бонусный процент и название.
    - Без этого мы можем забыть реализовать какой-то метод в новом типе счёта.
    """

    @abstractmethod
    def get_interest_rate(self):
        """Процентная ставка (должен быть переопределён)"""
        pass

    @abstractmethod
    def get_bonus_percent(self):
        """Бонус за пополнение (должен быть переопределён)"""
        pass

    @abstractmethod
    def get_name(self):
        """Название типа счёта"""
        pass


class RegularAccount(AccountType):
    """Обычный счёт"""

    def get_interest_rate(self):
        return 0.01  # 1% годовых

    def get_bonus_percent(self):
        return 0.01  # 1% бонуса от пополнения

    def get_name(self):
        return "Обычный"


class GoldAccount(AccountType):
    """Золотой счёт (для VIP)"""

    def get_interest_rate(self):
        return 0.05  # 5% годовых

    def get_bonus_percent(self):
        return 0.03  # 3% бонуса от пополнения

    def get_name(self):
        return "Золотой"


class StudentAccount(AccountType):
    """Студенческий счёт (льготный)"""

    def get_interest_rate(self):
        return 0.02  # 2% годовых

    def get_bonus_percent(self):
        return 0.02  # 2% бонуса от пополнения

    def get_name(self):
        return "Студенческий"


class VipAccount(AccountType):
    def get_interest_rate(self):
        return 0.07

    def get_bonus_percent(self):
        return 0.05

    def get_name(self):
        return "VIP"


# ========== КЛАСС ДЛЯ РАБОТЫ С БАЛАНСОМ (С ЛИМИТОМ БОНУСОВ) ==========
class Balance:
    def __init__(self, initial_balance=0):
        self._balance = initial_balance
        self._bonus_balance = 0
        self._daily_bonus_used = 0.0
        self._last_bonus_date = datetime.now().date()

    def _reset_daily_bonus_if_needed(self):
        today = datetime.now().date()
        if today != self._last_bonus_date:
            self._daily_bonus_used = 0.0
            self._last_bonus_date = today

    def deposit(self, amount, bonus_percent):
        """Пополнение счёта с начислением бонусов"""
        if amount <= 0:
            raise ValueError("Сумма должна быть положительной!")

        self._balance += amount
        bonus = amount * bonus_percent

        self._reset_daily_bonus_if_needed()
        if self._daily_bonus_used + bonus > 500:
            allowed_bonus = max(0, 500 - self._daily_bonus_used)
            self._bonus_balance += allowed_bonus
            self._daily_bonus_used += allowed_bonus
            return allowed_bonus
        else:
            self._bonus_balance += bonus
            self._daily_bonus_used += bonus
            return bonus

    def withdraw(self, amount):
        if amount <= 0:
            raise ValueError("Сумма должна быть положительной!")
        if amount > self._balance:
            raise ValueError("Недостаточно средств!")
        self._balance -= amount
        return amount

    def use_bonus(self):
        if self._bonus_balance <= 0:
            raise ValueError("Нет бонусов!")
        self._balance += self._bonus_balance
        result = self._bonus_balance
        self._bonus_balance = 0
        return result

    def get_balance(self):
        return self._balance

    def get_bonus_balance(self):
        return self._bonus_balance


# ========== КЛАСС ДЛЯ ИСТОРИИ ==========
class History:
    def __init__(self):
        self._records = []

    def add(self, operation, details):
        timestamp = datetime.now().strftime("%d.%m.%Y %H:%M:%S")
        self._records.append(f"[{timestamp}] {operation}: {details}")

    def get_last(self, n=10):
        return self._records[-n:] if self._records else []

    def __len__(self):
        return len(self._records)


# ========== КЛАСС ПОЛЬЗОВАТЕЛЯ ==========
class User:
    def __init__(self, name, email, phone):
        self.name = name
        self.email = email
        self.phone = phone
        self.created_at = datetime.now()


# ========== ОСНОВНОЙ КЛАСС ==========
class BankAccount:
    def __init__(self, name, email, phone, account_type, initial_balance=0):
        self.user = User(name, email, phone)
        self._account_type = account_type
        self._balance = Balance(initial_balance)
        self._history = History()

        self._history.add("СИСТЕМА",
                          f"Создан {self._account_type.get_name()} счёт. Баланс: {initial_balance} руб.")
        print(f"🏦 Создан {self._account_type.get_name()} счёт для {self.user.name}")

    def deposit(self, amount):
        try:
            bonus_percent = self._account_type.get_bonus_percent()
            bonus = self._balance.deposit(amount, bonus_percent)
            self._history.add("ПОПОЛНЕНИЕ", f"{amount} руб. (бонус: {bonus:.2f} руб.)")
            print(f"✅ Пополнено {amount} руб.")
            print(f"🎁 Начислено бонусов: {bonus:.2f} руб. ({bonus_percent * 100}%)")
        except ValueError as e:
            print(f"❌ Ошибка: {e}")

    def withdraw(self, amount):
        try:
            withdrawn = self._balance.withdraw(amount)
            self._history.add("СНЯТИЕ", f"{withdrawn} руб.")
            print(f"✅ Снято {withdrawn} руб.")
        except ValueError as e:
            print(f"❌ Ошибка: {e}")

    def use_bonus(self):
        try:
            bonus = self._balance.use_bonus()
            self._history.add("БОНУСЫ", f"Использовано {bonus:.2f} руб.")
            print(f"✅ Бонусы зачислены! +{bonus:.2f} руб.")
        except ValueError as e:
            print(f"❌ {e}")

    def show_balance(self):
        print(f"\n💰 Баланс ({self._account_type.get_name()}): {self._balance.get_balance():.2f} руб.")
        print(f"🎁 Бонусный счёт: {self._balance.get_bonus_balance():.2f} руб.")

    def show_history(self):
        records = self._history.get_last()
        if not records:
            print("📭 История пуста")
            return
        print(f"\n📜 ПОСЛЕДНИЕ ОПЕРАЦИИ ({self.user.name}):")
        print("-" * 50)
        for record in records:
            print(record)
        print("-" * 50)

    def __str__(self):
        return (f"🏦 Счёт: {self.user.name} ({self._account_type.get_name()})\n"
                f"💰 Баланс: {self._balance.get_balance():.2f} руб.\n"
                f"🎁 Бонусы: {self._balance.get_bonus_balance():.2f} руб.")


# Демонстрация
print("🏦 БАНК С SOLID (Принципы O и L)")
print("=" * 50)

regular = BankAccount("Алиса", "alice@mail.com", "+7 999 111-22-33", RegularAccount(), 5000)
gold = BankAccount("Борис", "boris@mail.com", "+7 999 444-55-66", GoldAccount(), 10000)
vip = BankAccount("Илья", 'ila@mail.com', "+7 999 456-65-65", VipAccount(),3000)
print("\n--- Обычный счёт (Алиса) ---")
regular.deposit(1000)
regular.show_balance()

print("\n--- Золотой счёт (Борис) ---")
gold.deposit(1000)
gold.show_balance()

print("\n" + "=" * 50)
print(regular)
print(gold)

vip.deposit(5000)
vip.show_balance()