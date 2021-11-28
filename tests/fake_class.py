class Money:
    value: int

    def __init__(self, value: int):
        self.value = value

    def __add__(self, other):
        return Money(self.value + other.value)
