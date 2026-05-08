from datetime import datetime


def get_current_time():
    """Возвращает текущее время в красивом формате"""
    now = datetime.now()
    return now.strftime("%H:%M:%S")


def add_transaction(history, operation, amount):
    """Добавляет запись об операции в историю"""
    time_str = get_current_time()
    history.append(f"[{time_str}] {operation}: {amount} руб.")
    print(f"✅ Запись добавлена: {operation}")


def show_history(history):
    """Показывает всю историю операций"""
    if not history:
        print("📭 История пуста")
        return

    print("\n📜 ИСТОРИЯ ОПЕРАЦИЙ:")
    print("-" * 40)
    for record in history:
        print(record)
    print("-" * 40)


def get_date_only():
    now = datetime.now()
    return now.strftime("%d.%m.%Y")


# Тестируем
history = []

print("🏦 Демонстрация банковской истории")
print(f"Текущее время: {get_current_time()}")
print(f"Текущяя дата: {get_date_only()}")

while True:
    print("\n1 - Пополнить")
    print("2 - Снять")
    print("3 - Показать историю")
    print("4 - Выйти")

    choice = input("Выберите действие: ")

    if choice == "1":
        amount = int(input("Сумма пополнения: "))
        add_transaction(history, "ПОПОЛНЕНИЕ", amount)
    elif choice == "2":
        amount = int(input("Сумма снятия: "))
        add_transaction(history, "СНЯТИЕ", amount)
    elif choice == "3":
        show_history(history)
    elif choice == "4":
        print("👋 До свидания!")
        break
    else:
        print("❌ Неверный выбор!")