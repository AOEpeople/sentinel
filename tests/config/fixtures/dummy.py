from typing import List


class Dummy:
    foo: str
    bar: int
    baz: List[str]

    def __init__(self, foo: str, bar: int, baz: List[str]):
        self.foo = foo
        self.bar = bar
        self.baz = baz
