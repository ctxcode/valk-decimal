
# Documentation

Namespaces: [main](#main)

---

# main

## Aliases for 'main'

```js
// Significant digits of a quotient from `/`.
+ value DIV_PRECISION (28)
// The largest exponent `parse` accepts, either way: `1e1000000` reads, `1e1000001` does not.
+ value MAX_EXPONENT (1_000_000)
```

### DIV_PRECISION

Significant digits of a quotient from `/`.

### MAX_EXPONENT

The largest exponent `parse` accepts, either way: `1e1000000` reads, `1e1000001` does not.

## Errors for 'main'

```js
// Thrown when a value cannot become a `Decimal`, or a `Decimal` cannot become another type.
+ error Error (syntax, range) payload { message: String }
```

### Error

Thrown when a value cannot become a `Decimal`, or a `Decimal` cannot become another type.

- `syntax`: the text is not a decimal number.
- `range`: the number does not fit: an exponent beyond a million, a float that is NaN or
  infinite, or a value outside the integer range in `to_int`.

## Enums for 'main'

```js
// How a result drops the digits that do not fit: in `round`, `div_round`, `sqrt` and `to_fixed`.
+ enum Rounding { half_even, half_up, half_down, down, up, floor, ceiling }
```

### Rounding

How a result drops the digits that do not fit: in `round`, `div_round`, `sqrt` and `to_fixed`.

- `half_even`: to the nearest, a tie to the even neighbour (banker's rounding).
- `half_up`: to the nearest, a tie away from zero.
- `half_down`: to the nearest, a tie toward zero.
- `down`: toward zero.
- `up`: away from zero.
- `floor`: toward negative infinity.
- `ceiling`: toward positive infinity.

## Functions for 'main'

```js
// Returns the shortest decimal that reads back as `value`: `from_float(0.1)` is `0.1`, not the `0.1000000000000000055511151231257827` the float holds exactly.
+ fn from_float(value: f64) Decimal !Error
// Returns `value` divided by 10 to the power `scale`: `from_int(1999, 2)` is `19.99`.
+ fn from_int(value: int, scale: i32 (0)) Decimal
// Returns `value` as an unsigned integer divided by 10 to the power `scale`.
+ fn from_uint(value: u64, scale: i32 (0)) Decimal
// Reads a decimal from text: `"12.50"`, `"-0.001"`, `"+7"`, `".5"`, `"1.5e-3"`, `"2E6"`.
+ fn parse(text: String) Decimal !Error
```

### from_float

Returns the shortest decimal that reads back as `value`: `from_float(0.1)` is `0.1`, not
the `0.1000000000000000055511151231257827` the float holds exactly.

Throws `range` for NaN and the infinities.

### from_int

Returns `value` divided by 10 to the power `scale`: `from_int(1999, 2)` is `19.99`.

### from_uint

Returns `value` as an unsigned integer divided by 10 to the power `scale`.

### parse

Reads a decimal from text: `"12.50"`, `"-0.001"`, `"+7"`, `".5"`, `"1.5e-3"`, `"2E6"`.

The value keeps the digits as written, so `"12.50"` has scale 2. No spaces, no thousands
separators. Throws `syntax` for anything else, and `range` for an exponent beyond
`MAX_EXPONENT`.

## Classes for 'main'

```js
// A decimal number of any size: a whole number of any length and a scale, the number of digits after the point.
+ struct Decimal {
    // The number of digits after the point. Negative for a value such as `1E+3` (`1000` with scale -3), which only `/` and `parse` make.
    ~+ scale: i32

    // Returns the value without its sign.
    + fn abs() Decimal
    // Returns `this + other`; backs `a + b`. Exact, with the larger scale of the two.
    + fn add(other: Decimal) Decimal
    // Returns `this + other`; backs `a + 5`.
    + fn add_int(other: int) Decimal
    // Returns -1, 0 or 1 when this value is below, equal to or above `other`.
    + fn compare(other: Decimal) int
    // Returns `this / other`; backs `a / b`.
    + fn div(other: Decimal) Decimal
    // Returns `this / other`; backs `a / 3`. See `div`.
    + fn div_int(other: int) Decimal
    // Returns `this / other` with `scale` decimals, rounded by `mode`.
    + fn div_round(other: Decimal, scale: i32, mode: Rounding (Rounding.half_even)) Decimal
    // Returns whether both are the same number, whatever their scales; backs `==`.
    + fn equals(other: Decimal) bool
    // Reads a Decimal from a JSON string or number, for valk.json's `to_type` and `decode_to`.
    + static fn from_json_value_auto[X](value: X) Decimal !LookupError
    // Backs `>`.
    + fn gt(other: Decimal) bool
    // Returns a hash that is the same for equal values, `1.0` and `1.00` too; backs map keys.
    + fn hash() uint
    // Returns true when the value is below zero.
    + fn is_negative() bool
    // Returns true for zero, at any scale.
    + fn is_zero() bool
    // Backs `<`.
    + fn lt(other: Decimal) bool
    // Returns `this * other`; backs `a * b`. Exact: the scale is the sum of both scales.
    + fn mul(other: Decimal) Decimal
    // Returns `this * other`; backs `a * 3`.
    + fn mul_int(other: int) Decimal
    // Returns the value with the opposite sign.
    + fn neg() Decimal
    // Returns this value to the power `exponent`.
    + fn pow(exponent: int) Decimal
    // Returns the value with exactly `scale` decimals: rounded by `mode` when it has more, padded with zeros when it has fewer.
    + fn round(scale: i32 (0), mode: Rounding (Rounding.half_even)) Decimal
    // Returns -1, 0 or 1 for a value below, at or above zero.
    + fn sign() int
    // Returns the square root with `scale` decimals, rounded by `mode`.
    + fn sqrt(scale: i32, mode: Rounding (Rounding.half_even)) Decimal !Error
    // Returns `this - other`; backs `a - b`. Exact, with the larger scale of the two.
    + fn sub(other: Decimal) Decimal
    // Returns `this - other`; backs `a - 5`.
    + fn sub_int(other: int) Decimal
    // Returns the value as text with exactly `decimals` decimals, rounded by `mode`: `to_fixed(2)` gives `19.99`, `3.00` or `0.10`.
    + fn to_fixed(decimals: uint, mode: Rounding (Rounding.half_even)) String
    // Returns the nearest float.
    + fn to_float() f64
    // Returns the whole part as an integer, the decimals cut off: `-12.9` gives `-12`.
    + fn to_int() int !Error
    // Returns `to_string()`: valk.json writes a Decimal as a JSON string, which keeps every digit.
    + fn to_json_string() String
    // Returns the value as text with all its decimals: `12.50`, `-0.001`, `1000`.
    + fn to_string() String
    // Writes `to_string()` to `out` and returns the bytes written.
    + fn to_string_into(out: Writer) uint !io:IoError
    // Returns the value without the zeros at the end of its decimals: `1.500` gives `1.5`, `2.00` gives `2`. Whole numbers are not changed.
    + fn trim() Decimal
    // Returns the value with at most `scale` decimals, the rest cut off (rounded toward zero).
    + fn truncate(scale: i32 (0)) Decimal
}
```

### Decimal

A decimal number of any size: a whole number of any length and a scale, the number of digits
after the point.

`1.50` has the coefficient 150 and the scale 2. Adding, subtracting and multiplying are
exact, and keep the scale: `1.50 + 1` is `2.50`, `1.5 * 1.25` is `1.875`. Dividing needs a
limit: `a / b` gives the exact quotient when it has at most 28 significant digits and
rounds to 28 otherwise, while `a.div_round(b, 2)` gives it with two decimals.

A struct: a value up to 20 digits takes no allocation, longer ones keep their digits in an
array. Values compare by number, so `1.0 == 1.00`, and equal values hash equal for map keys.
The zero value of the struct is `0`.

#### scale

The number of digits after the point. Negative for a value such as `1E+3` (`1000` with
scale -3), which only `/` and `parse` make.

#### abs

Returns the value without its sign.

#### add

Returns `this + other`; backs `a + b`. Exact, with the larger scale of the two.

#### add_int

Returns `this + other`; backs `a + 5`.

#### compare

Returns -1, 0 or 1 when this value is below, equal to or above `other`.

#### div

Returns `this / other`; backs `a / b`.

The quotient is exact when it has at most 28 significant digits, with as few decimals as
the scales allow (`1 / 4` is `0.25`, `1.00 / 2` is `0.50`); otherwise it is rounded
`half_even` to 28 significant digits (`1 / 3` is `0.3333333333333333333333333333`). These
are the rules of Python's `decimal` module. Use `div_round` for a quotient with a fixed
number of decimals. Dividing by zero panics, as it does for integers.

#### div_int

Returns `this / other`; backs `a / 3`. See `div`.

#### div_round

Returns `this / other` with `scale` decimals, rounded by `mode`.

`decimal.parse("10").div_round(decimal.parse("3"), 2)` is `3.33`. Dividing by zero panics.

#### equals

Returns whether both are the same number, whatever their scales; backs `==`.

#### from_json_value_auto

Reads a Decimal from a JSON string or number, for valk.json's `to_type` and `decode_to`.

A JSON number arrives as an `int` or a float, so one with more than 15 significant digits
can lose some on the way; send those as strings. Throws `.missing` for any other value.

#### gt

Backs `>`.

#### hash

Returns a hash that is the same for equal values, `1.0` and `1.00` too; backs map keys.

#### is_negative

Returns true when the value is below zero.

#### is_zero

Returns true for zero, at any scale.

#### lt

Backs `<`.

#### mul

Returns `this * other`; backs `a * b`. Exact: the scale is the sum of both scales.

#### mul_int

Returns `this * other`; backs `a * 3`.

#### neg

Returns the value with the opposite sign.

#### pow

Returns this value to the power `exponent`.

A positive exponent is exact: `1.5` to the power 3 is `3.375`. A negative one divides 1 by the
power with `/`, so it rounds to 28 significant digits; zero to a negative power panics as
a division by zero. Any value to the power 0 is `1`.

#### round

Returns the value with exactly `scale` decimals: rounded by `mode` when it has more,
padded with zeros when it has fewer.

`2.345` rounds to `2.34` with `round(2)` (half_even) and to `2.35` with
`round(2, .half_up)`; `2.5` becomes `2.50`. A negative scale rounds to tens, hundreds, ...

#### sign

Returns -1, 0 or 1 for a value below, at or above zero.

#### sqrt

Returns the square root with `scale` decimals, rounded by `mode`.

Throws `range` for a negative value.

#### sub

Returns `this - other`; backs `a - b`. Exact, with the larger scale of the two.

#### sub_int

Returns `this - other`; backs `a - 5`.

#### to_fixed

Returns the value as text with exactly `decimals` decimals, rounded by `mode`:
`to_fixed(2)` gives `19.99`, `3.00` or `0.10`.

#### to_float

Returns the nearest float.

#### to_int

Returns the whole part as an integer, the decimals cut off: `-12.9` gives `-12`.

Throws `range` when it does not fit an `int`.

#### to_json_string

Returns `to_string()`: valk.json writes a Decimal as a JSON string, which keeps every
digit.

#### to_string

Returns the value as text with all its decimals: `12.50`, `-0.001`, `1000`.

Never an exponent: a value with a negative scale gets its zeros written out.

#### to_string_into

Writes `to_string()` to `out` and returns the bytes written.

A `ByteBuffer` is written directly; any other writer receives the text in one write.

#### trim

Returns the value without the zeros at the end of its decimals: `1.500` gives `1.5`,
`2.00` gives `2`. Whole numbers are not changed.

#### truncate

Returns the value with at most `scale` decimals, the rest cut off (rounded toward zero).

Unlike `round`, a value with fewer decimals is returned as it is.
