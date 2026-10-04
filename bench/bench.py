#!/usr/bin/env python3
"""The same work as main.valk with Python's decimal module (the C implementation)."""

import decimal
import time
from decimal import Decimal


def values(count, seed, decimals):
    result = []
    x = seed
    for _ in range(count):
        x = (x * 6364136223846793005 + 1442695040888963407) % 2**64
        n = (x >> 33) % 10_000_000 + 1
        result.append(Decimal(n).scaleb(-decimals))
    return result


def report(name, start, ops):
    print("%s: %d ns/op" % (name, (time.perf_counter_ns() - start) // ops))


def main():
    n = 1_000_000
    a = values(1000, 1, 2)
    b = values(1000, 2, 4)
    texts = [str(v) for v in a]
    two = Decimal("0.01")

    start = time.perf_counter_ns()
    total = Decimal(0)
    for i in range(n):
        total = total + a[i % 1000]
    report("add", start, n)

    start = time.perf_counter_ns()
    for i in range(n):
        check = a[i % 1000] * b[i % 1000]
    report("mul", start, n)

    start = time.perf_counter_ns()
    for i in range(n):
        check = a[i % 1000] / b[i % 1000]
    report("div (28 digits)", start, n)

    start = time.perf_counter_ns()
    for i in range(n):
        check = (a[i % 1000] / b[i % 1000]).quantize(two)
    report("div + quantize (2 decimals)", start, n)

    start = time.perf_counter_ns()
    for i in range(n):
        check = Decimal(texts[i % 1000])
    report("parse", start, n)

    start = time.perf_counter_ns()
    length = 0
    for i in range(n):
        length += len(str(a[i % 1000]))
    report("to_string", start, n)

    # Enough precision to keep every digit of the sums and products
    decimal.getcontext().prec = 100
    big_a = [v * v * v for v in a]
    big_b = [v * v * 1000 + 1 for v in b]

    start = time.perf_counter_ns()
    big_sum = Decimal(0)
    for i in range(n):
        big_sum = big_sum + big_a[i % 1000]
    report("add (30 digits)", start, n)

    start = time.perf_counter_ns()
    for i in range(n):
        check = big_a[i % 1000] * big_b[i % 1000]
    report("mul (30 digits)", start, n)

    decimal.getcontext().prec = 28
    start = time.perf_counter_ns()
    for i in range(n):
        check = big_a[i % 1000] / big_b[i % 1000]
    report("div (30 digits)", start, n)
    print(big_sum, check)

    start = time.perf_counter_ns()
    for i in range(n):
        check = a[i % 1000]
    report("(empty loop)", start, n)
    print(decimal.__version__, total, check, length)


main()
