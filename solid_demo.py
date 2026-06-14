# solid_demo.py — демонстрация принципа S (Single Responsibility)

from datetime import datetime
import re


# ========== КЛАСС ДЛЯ ХРАНЕНИЯ ДАННЫХ ПОЛЬЗОВАТЕЛЯ ==========
class User:
    """Отвечает только за данные пользователя"""

    def __init__(self, name, email, phone):
        self.name = name
        self.email = email
        self.phone = phone
        self.created_at = datetime.now()


# ========== КЛАСС ДЛЯ РАБОТЫ С БАЛАНСОМ И БОНУСАМИ ==========
class Balance:
    """
    Отвечает только за баланс и бонусы

    🔒 _balance и _bonus_balance:
    Подчёркивание в начале говорит: "Это защищённая переменная.
    Не трогай её напрямую извне, используй методы класса".
    Это договорённость между программистами, а не строгое правило.
    """

    def __init__(self, initial_balance=0):
        self._balance = initial_balance  # основной счёт
        self._bonus_balance = 0  # бонусный счёт
        self._daily_bonus_used = 0.0  # сколько бонусов начислили сегодня
        self._last_bonus_date = datetime.now().date()  # дата последнего начисления

    def _reset_daily_bonus_if_needed(self):
        """
        ВНУТРЕННИЙ метод (начинается с _)
        Проверяет, не наступил ли новый день.
        Если наступил — обнуляет счётчик бонусов за день.
        """
        today = datetime.now().date()  # сегодняшняя дата (без времени)
        if today != self._last_bonus_date:  # если сегодня не равно "дню последнего бонуса"
            self._daily_bonus_used = 0.0  # обнуляем использованные бонусы
            self._last_bonus_date = today  # запоминаем, что сегодня уже проверили

    def deposit(self, amount):
        """
        Пополнение счёта с начислением бонусов (1% от суммы).
        Бонус за день не может превышать 500 руб. (защита от накрутки).

        ЛОГИКА:
        1. Проверяем, не наступил ли новый день (обнуляем счётчик при необходимости)
        2. Считаем бонус: amount * 0.01
        3. Проверяем: если сегодня уже начислили 450 руб. и хотим начислить 100 руб. (всего 550),
           то начисляем только 50 руб. (оставшиеся до лимита 500)
        4. Если лимит не превышен — начисляем полный бонус
        """
        if amount <= 0:
            raise ValueError("Сумма должна быть положительной!")

        self._balance += amount  # добавляем деньги на основной счёт

        # Шаг 1: считаем, сколько бонусов положено (1% от суммы)
        bonus = amount * 0.01

        # Шаг 2: проверяем, не наступил ли новый день (обнуляем счётчик)
        self._reset_daily_bonus_if_needed()

        # Шаг 3: проверяем, не превысим ли лимит 500 руб. в день
        if self._daily_bonus_used + bonus > 500:
            # Пример: уже начислили 450 руб., хотим начислить 100 руб.
            # 450 + 100 = 550 > 500 → ограничиваем
            # allowed_bonus = 500 - 450 = 50 руб.
            allowed_bonus = max(0, 500 - self._daily_bonus_used)
            self._bonus_balance += allowed_bonus
            self._daily_bonus_used += allowed_bonus
            print(f"⚠️ Бонус ограничен: {bonus:.2f} → {allowed_bonus:.2f} руб. (лимит 500 руб./день)")
            return allowed_bonus
        else:
            # Лимит не превышен — начисляем полный бонус
            self._bonus_balance += bonus
            self._daily_bonus_used += bonus
            return bonus

    def withdraw(self, amount):
        """Снятие денег"""
        if amount <= 0:
            raise ValueError("Сумма должна быть положительной!")
        if amount > self._balance:
            raise ValueError("Недостаточно средств!")
        self._balance -= amount
        return amount

    def use_bonus(self):
        """Использовать бонусы — переводит бонусы на основной счёт"""
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


# ========== КЛАСС ДЛЯ ИСТОРИИ ОПЕРАЦИЙ ==========
class History:
    """
    Отвечает только за хранение истории

    🔒 _records: защищённый список записей.
    Внешний код не должен напрямую добавлять записи в _records,
    только через метод add(). Это гарантирует правильный формат записей.
    """

    def __init__(self):
        self._records = []

    def add(self, operation, details):
        """Добавляет запись с автоматической временной меткой"""
        timestamp = datetime.now().strftime("%d.%m.%Y %H:%M:%S")
        self._records.append(f"[{timestamp}] {operation}: {details}")

    def get_last(self, n=10):
        """Возвращает последние N записей"""
        return self._records[-n:] if self._records else []

    def __len__(self):
        return len(self._records)


# ========== ОСНОВНОЙ КЛАСС (СВЯЗЫВАЕТ ВСЁ ВМЕСТЕ) ==========
class BankAccount:
    """
    Класс банковского счёта — связывает User, Balance, History.
    Сам не занимается ни балансом, ни историей — только координирует их работу.
    """

    def __init__(self, name, email, phone, initial_balance=0):
        self.user = User(name, email, phone)
        self._balance = Balance(initial_balance)  # 🔒 делегируем работу другому классу
        self._history = History()

        self._history.add("СИСТЕМА", f"Аккаунт создан. Баланс: {initial_balance} руб.")
        print(f"🏦 Создан счёт для {self.user.name}")

    def deposit(self, amount):
        """Пополнение — делегируем Balance"""
        try:
            bonus = self._balance.deposit(amount)
            self._history.add("ПОПОЛНЕНИЕ", f"{amount} руб. (бонус: {bonus:.2f} руб.)")
            print(f"✅ Пополнено {amount} руб.")
            print(f"🎁 Начислено бонусов: {bonus:.2f} руб.")
        except ValueError as e:
            print(f"❌ Ошибка: {e}")

    def withdraw(self, amount):
        """Снятие — делегируем Balance"""
        try:
            withdrawn = self._balance.withdraw(amount)
            self._history.add("СНЯТИЕ", f"{withdrawn} руб.")
            print(f"✅ Снято {withdrawn} руб.")
        except ValueError as e:
            print(f"❌ Ошибка: {e}")

    def use_bonus(self):
        """Использовать бонусы — делегируем Balance"""
        try:
            bonus = self._balance.use_bonus()
            self._history.add("БОНУСЫ", f"Использовано {bonus:.2f} руб.")
            print(f"✅ Бонусы зачислены! +{bonus:.2f} руб.")
        except ValueError as e:
            print(f"❌ {e}")

    def show_balance(self):
        print(f"\n💰 Баланс {self.user.name}: {self._balance.get_balance():.2f} руб.")
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
        return (f"🏦 Счёт: {self.user.name}\n"
                f"💰 Баланс: {self._balance.get_balance():.2f} руб.\n"
                f"🎁 Бонусы: {self._balance.get_bonus_balance():.2f} руб.")


# Демонстрация
print("🏦 БАНК С SOLID (Принцип S - Single Responsibility)")
print("=" * 50)

account = BankAccount("Алиса", "alice@mail.com", "+7 999 111-22-33", 5000)
account.show_balance()

print("\n--- Пополнения (проверка лимита бонусов) ---")
print("Пополняем на 10 000 руб. → бонус 100 руб.")
account.deposit(10000)  # 10000 руб. → бонус 100 руб.

print("\nПополняем ещё на 30 000 руб. → бонус 300 руб. (итого 400 за день)")
account.deposit(30000)  # 30000 руб. → бонус 300 руб.

print("\nПополняем ещё на 20 000 руб. → бонус должен быть 200 руб., но осталось только 100 до лимита")
account.deposit(20000)  # 20000 руб. → бонус ограничен до 100 руб.