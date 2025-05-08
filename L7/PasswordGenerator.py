import random
from string import ascii_letters, digits

class PasswordGenerator:
    _charset = ascii_letters + digits
    def __init__(self, length: int, count, charset = _charset,):
        self.length = length
        self.charset = charset
        self.count = count

    def __iter__(self):
        return self

    def __next__(self):
        if self.count:
            self.count -= 1
            return "".join(random.sample(self._charset, self.length))
        else:
            raise StopIteration


gen = PasswordGenerator(length=12, count=20)

for p in gen:
    print(p)