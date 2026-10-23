# valk-decimal

Decimal numbers of any size for [Valk](https://valk-lang.dev): exact sums of money, database
`NUMERIC` values, and division with the rounding you choose. Purely written in Valk.

Requires Valk 0.8.0 or newer.

## Install

```
vman install github.com/ctxcode/valk-decimal
```

## Example

```rust
use decimal

let price = decimal.parse("19.99") ! panic("Not a number")
let total = price * 3 + decimal.parse("4.95") !! // 64.92
let vat = (total * decimal.from_int(21, 2)).round(2) // 13.63
println("Total: %{total + vat}")                   // Total: 78.55

decimal.parse("0.1") !! + decimal.parse("0.2") !! == decimal.parse("0.3") !! // true
```

A `Decimal` is a whole number and a scale, the number of digits after the point: `19.99` is 1999
with scale 2. It is a struct, so it is copied by value, and one of up to 19 digits needs no
allocation. Longer ones keep their digits in an array and have no size limit.

- `decimal.parse(text)` reads `12.50`, `-0.001`, `+7`, `.5` and exponents such as `1.5e-3`, and
  keeps the digits as written: `12.50` has scale 2.
- `decimal.from_int(1999, 2)` is `19.99`, `decimal.from_uint(n)` takes a `u64`, and
  `decimal.from_float(0.1)` gives the shortest decimal that reads back as the float, `0.1`.
- `to_string()` writes every decimal and never an exponent (`1E+3` is written `1000`); a
  `Decimal` converts to `String` wherever one is expected. `to_fixed(2)` writes exactly two
  decimals, `to_int()` cuts the decimals off, `to_float()` gives the nearest float.

## Arithmetic

`+`, `-` and `*` are exact, with a `Decimal` or an `int` on the right. A sum has the larger scale
of the two (`1.50 + 1` is `2.50`) and a product the sum of both (`1.5 * 1.25` is `1.875`).

Division needs a limit. `a / b` follows Python's `decimal` module: the exact quotient when it has
at most 28 significant digits (`1 / 4` is `0.25`), and otherwise rounded to 28 (`1 / 3` is
`0.3333333333333333333333333333`). For money, give the scale and the rounding:

```rust
let share = total.div_round(decimal.from_int(7), 2)                 // 9.27
let rounded_up = total.div_round(decimal.from_int(7), 2, .ceiling)  // 9.28
```

Dividing by zero panics, as it does for integers.

`round(scale, mode)` gives exactly `scale` decimals, padding with zeros when there are fewer,
`truncate(scale)` cuts off what is past `scale`, and `trim()` drops the zeros at the end of the
decimals. `pow(n)` takes an integer exponent and is exact for a positive one, and
`sqrt(scale, mode)` gives a square root with `scale` decimals. `abs()`, `neg()`, `sign()`,
`is_zero()` and `is_negative()` do what they say.

## Rounding

`decimal.Rounding` names the ways to drop digits; `half_even` is the default everywhere.

| Mode | `2.345` to 2 decimals | `-2.345` to 2 decimals |
|---|---|---|
| `half_even` (banker's) | `2.34` | `-2.34` |
| `half_up` | `2.35` | `-2.35` |
| `half_down` | `2.34` | `-2.34` |
| `down` (toward zero) | `2.34` | `-2.34` |
| `up` (away from zero) | `2.35` | `-2.35` |
| `floor` | `2.34` | `-2.35` |
| `ceiling` | `2.35` | `-2.34` |

## Comparing and map keys

Values compare by number, whatever their scales: `1.0 == 1.00`, and `<`, `>`, `compare(other)`
and `Array.sort()` work. Equal values hash equal, so a `Decimal` is a `HashMap` key where `1.0`
and `1.00` find the same entry.

## JSON

`valk.json` writes a `Decimal` as a string, which keeps every digit, and reads one from a string
or a number:

```rust
class Line {
    product: String
    price: decimal.Decimal
}

json.encode(Line { product: "Book", price: decimal.from_int(1299, 2) })
// {"product":"Book","price":"12.99"}
let line = json.decode_to[Line]("{\"product\":\"Pen\",\"price\":0.35}") ! panic("Invalid")
```

A JSON number reaches the `Decimal` through a float, so one with more than 15 significant digits
can lose some; send those as strings.

## Errors

`decimal.Error` with `syntax` (text that is not a number) or `range` (an exponent beyond a
million, a float that is NaN or infinite, a value too large for `to_int`, the square root of a
negative number), and a `message`.

## Benchmarks

One million operations on prices with 2 decimals and rates with 4, against Python 3.14's
`decimal` module (its C implementation, `libmpdec`), on an AMD Ryzen 5 7600X. The Python numbers
include about 28 ns of loop overhead per operation. `make bench` runs both.

| Operation | valk-decimal | Python `decimal` |
|---|---|---|
| add | 7 ns | 70 ns |
| mul | 10 ns | 90 ns |
| `/` (28 digits) | 80 ns | 120 ns |
| `div_round` to 2 decimals / `/` + `quantize` | 11 ns | 200 ns |
| parse | 15 ns | 110 ns |
| to_string | 35 ns | 87 ns |
| add, 30 digits | 50 ns | 70 ns |
| mul, 30 digits | 77 ns | 96 ns |
| `/`, 30 digits | 260 ns | 128 ns |

Values beyond 19 digits keep their digits in an array, which costs an allocation per result.

## Not supported

NaN, infinities and negative zero (a negative result that rounds to zero is `0`); a context with
traps, flags or another precision for `/`; remainder and integer division; exponential,
logarithmic and other functions beyond `pow` and `sqrt`; thousands separators and spaces in
`parse`.

## Development

`make test` runs the suite, `make example` runs the example, `make lint` checks the sources,
`make docs` regenerates the API documentation and `make bench` runs the benchmarks.
`python3 tests/crosscheck.py` regenerates `tests/python-samples.txt`, about 12,000 random
operations answered by Python's `decimal` module; `COUNT=15000 SEED=2 python3 tests/crosscheck.py`
makes a larger set with other numbers.
