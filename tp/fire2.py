import fire
from typing import Text

def add(x: int, y: int) -> int:
    return x + y

def multiply(x: int, y: int) -> int:
    return x * y

if __name__ == '__main__':
    fire.Fire({
        'add': add,
        'multiply': multiply,
        })