# dice-roller

Parse and roll dice expressions like 2d6+3.

## Usage

```bash
python3 -c "from dice import roll; print(roll('2d6+3'))"
python3 -c "from dice import roll; print(roll('4d6kh3'))"
python3 -c "from dice import roll_advantage; print(roll_advantage(20))"
python3 -c "from dice import sum_rolls; print(sum_rolls(['2d6+3', '1d8']))"
python3 -c "from dice import min_max; print(min_max('2d20+3'))"
```

## Features

- Parse expressions like d6, 2d20+3, and 1d8-1
- Keep/drop rolls like 4d6kh3 (keep highest 3) and 4d6kl1 (keep lowest 1)
- Injectable random source for deterministic tests
- Advantage/disadvantage with roll_advantage(sides, rng) and roll_disadvantage(sides, rng)
- Batch statistics with roll_many(expression, times, rng)
- Sum several expressions at once with sum_rolls(expressions, rng)
- Minimum and maximum totals with min_max(expression)

## Tests

```bash
python3 -m unittest -q
```

## Additional API

- `expected_value(expression)` returns the statistical mean total for a dice expression.

## License

MIT
