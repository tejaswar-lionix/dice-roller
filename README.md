# dice-roller

Parse and roll dice expressions like 2d6+3.

## Usage

```bash
python3 -c "from dice import roll; print(roll('2d6+3'))"
python3 -c "from dice import roll; print(roll('4d6kh3'))"
python3 -c "from dice import roll_advantage; print(roll_advantage(20))"
```

## Features

- Parse expressions like d6, 2d20+3, and 1d8-1
- Keep/drop rolls like 4d6kh3 (keep highest 3) and 4d6kl1 (keep lowest 1)
- Injectable random source for deterministic tests
- Advantage/disadvantage with roll_advantage(sides, rng) and roll_disadvantage(sides, rng)
- Batch statistics with roll_many(expression, times, rng)

## Tests

```bash
python3 -m unittest -q
```

## License

MIT
