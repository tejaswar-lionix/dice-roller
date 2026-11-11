# dice-roller

Parse and roll dice expressions like 2d6+3.

## Usage

```bash
python3 -c "from dice import roll; print(roll('2d6+3'))"
```

## Features

- Parse expressions like d6, 2d20+3, and 1d8-1
- Injectable random source for deterministic tests
- Batch statistics with roll_many(expression, times, rng)

## Tests

```bash
python3 -m unittest -q
```

## License

MIT
