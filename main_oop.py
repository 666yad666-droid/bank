# bank_oop.py — обновлённая версия с магическими методами

from datetime import datetime
import re


class BankAccount:
    """Класс банковского счёта с магическими методами"""

    bank_name = "Банк 'Ученик'"

    def __init__(self, owner, email, phone, initial_balance=0):
        self.owner = owner
        self.email = email
        self.phone = phone
        self.balance = initial_balance
        self.bonus_balance = 0
        self.history = []
        self.created_at = datetime.now()

        self._add_to_history("СИСТЕМА", f"Аккаунт создан. Баланс: {initial_balance} руб.")
        print(f"🏦 Создан счёт для {self.owner}")

    # ========== МАГИЧЕСКИЕ МЕТОДЫ ==========

    def __str__(self):
        """Красивое представление для пользователя"""
        return (f"🏦 Счёт: {self.owner}\n"
                f"💰 Баланс: {self.balance:.2f} руб.\n"
                f"🎁 Бонусы: {self.bonus_balance:.2f} руб.")

    def __repr__(self):
        """Техническое представление для разработчиков"""
        return f"BankAccount('{self.owner}', '{self.email}', '{self.phone}', {self.balance})"

    def __bool__(self):
        """Счёт считается истинным, если на нём есть деньги"""
        return self.balance > 0

    def __add__(self, other):
        """Сложение: account + account (сумма балансов)"""
        if isinstance(other, BankAccount):
            return self.balance + other.balance
        elif isinstance(other, (int, float)):
            return self.balance + other
        else:
            return NotImplemented

    def __eq__(self, other):
        """Сравнение по балансу"""
        if isinstance(other, BankAccount):
            return self.balance == other.balance
        return False

    def __lt__(self, other):
        """Меньше — по балансу"""
        if isinstance(other, BankAccount):
            return self.balance < other.balance
        return False

        # ========== ОСНОВНЫЕ МЕТОДЫ ==========

    def _add_to_history(self, operation, details):
        """Добавляет запись в историю"""
        timestamp = datetime.now().strftime("%d.%m.%Y %H:%M:%S")
        self.history.append(f"[{timestamp}] {operation}: {details}")

    def show_balance(self):
        """Показать баланс"""
        print(f"\n💰 Баланс {self.owner}: {self.balance:.2f} руб.")
        print(f"🎁 Бонусный счёт: {self.bonus_balance:.2f} руб.")

    def deposit(self, amount):
        """Пополнение счёта"""
        if amount <= 0:
            print("❌ Сумма должна быть положительной!")
            return

        self.balance += amount
        bonus = amount * 0.01
        self.bonus_balance += bonus
        self._add_to_history("ПОПОЛНЕНИЕ", f"{amount} руб. (бонус: {bonus:.2f} руб.)")
        print(f"✅ Пополнено {amount} руб.")
        print(f"🎁 Начислено бонусов: {bonus:.2f} руб.")

    def withdraw(self, amount):
        """Снятие денег"""
        if amount <= 0:
            print("❌ Сумма должна быть положительной!")
            return
        if amount > self.balance:
            print("❌ Недостаточно средств!")
            return

        self.balance -= amount
        self._add_to_history("СНЯТИЕ", f"{amount} руб.")
        print(f"✅ Снято {amount} руб.")

    def use_bonus(self):
        """Использовать бонусы"""
        if self.bonus_balance <= 0:
            print("🎁 У вас нет бонусов!")
            return

        self.balance += self.bonus_balance
        self._add_to_history("БОНУСЫ", f"Использовано {self.bonus_balance:.2f} бонусных рублей")
        print(f"✅ Бонусы зачислены! +{self.bonus_balance:.2f} руб.")
        self.bonus_balance = 0

    def transfer(self, other_account, amount):
        """Перевод на другой счёт"""
        if amount <= 0:
            print("❌ Сумма должна быть положительной!")
            return
        if amount > self.balance:
            print("❌ Недостаточно средств!")
            return

        self.balance -= amount
        other_account.balance += amount

        self._add_to_history("ПЕРЕВОД", f"{amount} руб. → {other_account.owner}")
        other_account._add_to_history("ПОЛУЧЕНИЕ", f"{amount} руб. от {self.owner}")

        print(f"✅ Переведено {amount} руб. пользователю {other_account.owner}")

    def show_history(self, last_n=10):
        """Показать последние N операций"""
        if not self.history:
            print("📭 История пуста")
            return

        print(f"\n📜 ПОСЛЕДНИЕ ОПЕРАЦИИ ({self.owner}):")
        print("-" * 50)
        for record in self.history[-last_n:]:
            print(record)
        print("-" * 50)

    def show_info(self):
        """Показать информацию об аккаунте"""
        print(f"\n📋 ИНФОРМАЦИЯ ОБ АККАУНТЕ")
        print(f"🏦 Банк: {self.bank_name}")
        print(f"👤 Владелец: {self.owner}")
        print(f"📧 Email: {self.email}")
        print(f"📱 Телефон: {self.phone}")
        print(f"💰 Баланс: {self.balance:.2f} руб.")
        print(f"🎁 Бонусы: {self.bonus_balance:.2f} руб.")
        print(f"📅 Дата создания: {self.created_at.strftime('%d.%m.%Y %H:%M:%S')}")
        print(f"📊 Всего операций: {len(self.history)}")


# Демонстрация работы
def main():
    print(f"🏦 Добро пожаловать в {BankAccount.bank_name}!")

    # Создаём счета
    alice = BankAccount("Алиса", "alice@mail.com", "+7 999 111-22-33", 5000)
    bob = BankAccount("Боб", "bob@mail.com", "+7 999 444-55-66", 3000)

    print("\n" + "=" * 50)
    print("🔮 ДЕМОНСТРАЦИЯ МАГИЧЕСКИХ МЕТОДОВ")
    print("=" * 50)

    # __str__ — красивое представление
    print("\n--- __str__ ---")
    print(alice)

    # __repr__ — техническое представление
    print("\n--- __repr__ ---")
    print(repr(alice))

    # __bool__ — проверка на наличие денег
    print("\n--- __bool__ ---")
    if alice:
        print(f"{alice.owner} — на счету есть деньги!")
    else:
        print(f"{alice.owner} — счёт пуст!")

    # __add__ — сложение балансов
    print("\n--- __add__ ---")
    print(f"Сумма балансов Алисы и Боба: {alice + bob} руб.")
    print(f"Баланс Алисы + 1000: {alice + 1000} руб.")

    # __eq__ и __lt__ — сравнение
    print("\n--- __eq__ и __lt__ ---")
    print(f"Баланс Алисы == Баланс Боба: {alice == bob}")
    print(f"Баланс Алисы < Баланс Боба: {alice < bob}")


if __name__ == "__main__":
    main()