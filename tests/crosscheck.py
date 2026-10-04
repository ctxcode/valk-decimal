#!/usr/bin/env python3
"""Writes tests/python-samples.txt: random operations and the answers of Python's decimal module.

One case per line, tab separated: the operation, its arguments, and the expected result.
tests/crosscheck.valk runs every line. Run this again after changing it:

    python3 tests/crosscheck.py
"""

import decimal
import math
import os
import random
from decimal import Decimal
from fractions import Fraction

HERE = os.path.dirname(os.path.abspath(__file__))
COUNT = int(os.environ.get("COUNT", "800"))

EXACT = decimal.Context(prec=decimal.MAX_PREC, Emax=decimal.MAX_EMAX, Emin=decimal.MIN_EMIN, traps=[])
DIVISION = decimal.Context(prec=28, rounding=decimal.ROUND_HALF_EVEN, Emax=decimal.MAX_EMAX,
                           Emin=decimal.MIN_EMIN, traps=[])

MODES = {
    "half_even": decimal.ROUND_HALF_EVEN,
    "half_up": decimal.ROUND_HALF_UP,
    "half_down": decimal.ROUND_HALF_DOWN,
    "down": decimal.ROUND_DOWN,
    "up": decimal.ROUND_UP,
    "floor": decimal.ROUND_FLOOR,
    "ceiling": decimal.ROUND_CEILING,
}

# Coefficients around the edges of a u64 and of a 1e9 limb
EDGES = [
    0, 1, 5, 9, 10, 999_999_999, 1_000_000_000, 1_000_000_001, 10**18 - 1, 10**18,
    10**19 - 1, 10**19, 2**63 - 1, 2**63, 2**64 - 1, 2**64, 2**64 + 1, 10**27 - 1, 10**27, 10**36,
]


def text(d):
    """Plain notation, without a sign on zero."""
    s = format(d, "f")
    if d == 0 and s.startswith("-"):
        s = s[1:]
    return s


def random_coefficient(rng):
    r = rng.random()
    if r < 0.08:
        return rng.choice(EDGES) + rng.randint(-2, 2) * (rng.random() < 0.5)
    if r < 0.5:
        digits = rng.randint(1, 12)
    elif r < 0.85:
        digits = rng.randint(1, 22)
    else:
        digits = rng.randint(18, 60)
    value = rng.randint(0, 10**digits - 1)
    if rng.random() < 0.15:
        value *= 10 ** rng.randint(1, 6)
    return value


def random_decimal(rng, max_scale=20):
    c = abs(random_coefficient(rng))
    r = rng.random()
    if r < 0.1:
        scale = rng.randint(-6, -1)
    elif r < 0.6:
        scale = rng.randint(0, 4)
    else:
        scale = rng.randint(0, max_scale)
    sign = 1 if rng.random() < 0.4 else 0
    return Decimal((sign, tuple(int(ch) for ch in str(c)), -scale))


def scale_of(d):
    return -d.as_tuple().exponent


def write_input(rng, d):
    """Text for `d` the way a person or database might write it, read back as the same value."""
    s = str(d)  # may use an exponent: 1.2E+5, 1E-7
    if "E" in s or rng.random() < 0.7:
        return s
    t = d.as_tuple()
    digits = "".join(str(x) for x in t.digits)
    return ("-" if t.sign else "") + digits + "e" + str(t.exponent)


def div_round(a, b, scale, mode):
    # Round once: ROUND_05UP keeps enough of the quotient for the second rounding to be exact
    digits = a.adjusted() - b.adjusted() + 2 + scale + 5
    ctx = decimal.Context(prec=max(digits, 5), rounding=decimal.ROUND_05UP, Emax=decimal.MAX_EMAX,
                          Emin=decimal.MIN_EMIN, traps=[])
    q = ctx.divide(a, b)
    return q.quantize(Decimal((0, (1,), -scale)), rounding=MODES[mode], context=EXACT)


def sqrt_round(a, scale, mode):
    # Exact rationals and an integer root: no decimal arithmetic at all
    t = a.as_tuple()
    c = int("".join(str(x) for x in t.digits))
    m = Fraction(c) * Fraction(10) ** (2 * scale + t.exponent)
    q = math.isqrt(math.floor(m))
    if q * q == m:
        cls = 0
    else:
        half = (2 * q + 1) ** 2
        cls = 1 if 4 * m < half else (2 if 4 * m == half else 3)
    up = {
        "half_even": cls == 3 or (cls == 2 and q % 2 == 1),
        "half_up": cls >= 2,
        "half_down": cls == 3,
        "down": False,
        "up": cls > 0,
        "floor": False,
        "ceiling": cls > 0,
    }[mode]
    if up:
        q += 1
    return Decimal((0, tuple(int(ch) for ch in str(q)), -scale))


def trim(d):
    if d.as_tuple().exponent >= 0:
        return d
    n = d.normalize(EXACT)
    if n.as_tuple().exponent > 0:
        n = n.quantize(Decimal(1), context=EXACT)
    return n


def main():
    rng = random.Random(int(os.environ.get("SEED", "20261004")))
    lines = []

    def emit(*parts):
        lines.append("\t".join(str(p) for p in parts))

    for _ in range(COUNT):
        d = random_decimal(rng)
        emit("parse", write_input(rng, d), text(d))
    for bad in ["", "-", "+", ".", "e5", "1e", "1e+", "1.2.3", "1,5", " 1", "1 ", "--1", "0x10",
                "NaN", "Infinity", "1e1000001", "1_000", "١"]:
        emit("parse_error", bad)

    for op in ("add", "sub", "mul", "cmp"):
        for _ in range(COUNT):
            a = random_decimal(rng)
            b = random_decimal(rng)
            if rng.random() < 0.1:
                b = a
            if op == "add":
                emit(op, str(a), str(b), text(EXACT.add(a, b)))
            elif op == "sub":
                emit(op, str(a), str(b), text(EXACT.subtract(a, b)))
            elif op == "mul":
                emit(op, str(a), str(b), text(EXACT.multiply(a, b)))
            else:
                emit(op, str(a), str(b), (a > b) - (a < b))

    for _ in range(COUNT):
        a = random_decimal(rng)
        b = random_decimal(rng)
        if b == 0:
            b = Decimal(7)
        emit("div", str(a), str(b), text(DIVISION.divide(a, b)))

    for _ in range(COUNT):
        a = random_decimal(rng)
        b = random_decimal(rng)
        if b == 0:
            b = Decimal(3)
        scale = rng.randint(-3, 12)
        mode = rng.choice(list(MODES))
        emit("div_round", str(a), str(b), scale, mode, text(div_round(a, b, scale, mode)))

    for _ in range(COUNT):
        a = random_decimal(rng)
        scale = rng.randint(-3, 14)
        mode = rng.choice(list(MODES))
        if rng.random() < 0.3:
            # Ties: a 5 right after the kept digits
            cut = a.quantize(Decimal((0, (1,), -scale)), rounding=decimal.ROUND_DOWN, context=EXACT)
            a = EXACT.add(cut, Decimal((a.as_tuple().sign, (5,), -scale - 1)))
        emit("round", str(a), scale, mode, text(a.quantize(Decimal((0, (1,), -scale)), rounding=MODES[mode],
                                                            context=EXACT)))
        cut = a if scale >= scale_of(a) else a.quantize(Decimal((0, (1,), -scale)),
                                                          rounding=decimal.ROUND_DOWN, context=EXACT)
        emit("truncate", str(a), scale, text(cut))
        emit("trim", str(a), text(trim(a)))

    for _ in range(COUNT // 2):
        a = random_decimal(rng, 6)
        if rng.random() < 0.7:
            a = Decimal((rng.randint(0, 1), tuple(int(ch) for ch in str(rng.randint(0, 99999))), -rng.randint(0, 4)))
        if a == 0:
            a = Decimal("-0.5")
        n = rng.randint(0, 12)
        emit("pow", str(a), n, text(EXACT.power(a, n)))
    for _ in range(COUNT // 4):
        a = random_decimal(rng, 4)
        if a == 0:
            a = Decimal("1.5")
        n = rng.randint(1, 6)
        # 1 / a**n: Python's own power is not always correctly rounded near a tie
        emit("pow", str(a), -n, text(DIVISION.divide(Decimal(1), EXACT.power(a, n))))

    for _ in range(COUNT):
        a = abs(random_decimal(rng))
        scale = rng.randint(0, 30)
        mode = rng.choice(list(MODES))
        if rng.random() < 0.2:
            a = EXACT.multiply(a, a)
        emit("sqrt", str(a), scale, mode, text(sqrt_round(a, scale, mode)))

    for _ in range(COUNT):
        a = random_decimal(rng)
        i = int(a)
        emit("to_int", str(a), i if -2**63 <= i < 2**63 else "range")
        emit("to_float", str(a), repr(float(a)))

    for _ in range(COUNT):
        r = rng.random()
        if r < 0.3:
            f = rng.uniform(-1e6, 1e6)
        elif r < 0.5:
            f = round(rng.uniform(-1e4, 1e4), rng.randint(0, 4))
        else:
            f = math.ldexp(rng.random(), rng.randint(-1070, 1020)) * rng.choice([1, -1])
        emit("from_float", repr(f), text(Decimal(repr(f))))

    for _ in range(COUNT):
        a = random_decimal(rng)
        # The same number written another way: more zeros, or an exponent
        zeros = rng.randint(0, 25)
        b = a.quantize(Decimal((0, (1,), -(scale_of(a) + zeros))), context=EXACT)
        if rng.random() < 0.3:
            b = a.normalize(EXACT)
        emit("same", str(a), str(b))

    with open(os.path.join(HERE, "python-samples.txt"), "w", encoding="utf-8") as f:
        f.write("# Generated by tests/crosscheck.py from Python's decimal module; do not edit.\n")
        f.write("\n".join(lines) + "\n")


if __name__ == "__main__":
    main()
