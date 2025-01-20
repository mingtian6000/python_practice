import time
from airbus.decorators import timeit

@timeit
def test_timeit():
    for i in range(5):
        time.sleep(1)
test_timeit()