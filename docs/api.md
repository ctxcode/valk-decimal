
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

## Errors for 'main'

```js
// Thrown when a value cannot become a `Decimal`, or a `Decimal` cannot become another type.
+ error Error (syntax, range) payload { message: String }
```

## Enums for 'main'

```js
// How a result drops the digits that do not fit: in `round`, `div_round`, `sqrt` and `to_fixed`.
+ enum Rounding { half_even, half_up, half_down, down, up, floor, ceiling }
```

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
