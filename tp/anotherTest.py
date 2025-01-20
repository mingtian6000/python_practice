import time
from airbus.decorators import progressbar
@progressbar
def dummy_loop():
    total = 20
    yield total
    for i in range(1, total + 1):
        yield i
        time.sleep(1)
    return "done"
print(dummy_loop())