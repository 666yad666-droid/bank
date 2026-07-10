# ========== БАЗОВЫЕ КЛАССЫ ДЛЯ ДЕМОНСТРАЦИИ MRO ==========

class A:
    def __init__(self):
        print("A.__init__")

    def method(self):
        print("A.method")


class B(A):
    def __init__(self):
        print("B.__init__")
        super().__init__()

    def method(self):
        print("B.method")
        super().method()


class C(A):
    def __init__(self):
        print("C.__init__")
        super().__init__()

    def method(self):
        print("C.method")
        super().method()


class D(B, C):
    def __init__(self):
        print("D.__init__")
        super().__init__()

    def method(self):
        print("D.method")
        super().method()



# ========== ДЕМОНСТРАЦИЯ ==========

print("🏦 ДЕМОНСТРАЦИЯ MRO И super()")
print("=" * 50)

# 1. Демонстрация MRO на простых классах
print("\n--- MRO класса D(B, C) ---")
print(f"MRO: {[cls.__name__ for cls in D.__mro__]}")
print("\n--- Вызов метода method() у D ---")
d = D()
d.method()
