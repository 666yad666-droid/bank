counter = 0
def increment(counter):
    counter += 1
    print(f"теперь число {counter}")
    return counter


def decrement(counter):
    counter -= 1
    print(f"теперь число {counter}")
    return counter


def show(counter):
    print(f"число {counter}")


counter = increment(counter)
counter = increment(counter)
counter = increment(counter)
show(counter)
counter = decrement(counter)
show(counter)