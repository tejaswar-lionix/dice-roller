#!/usr/bin/env python3
"""Parse and roll dice expressions like 2d6+3."""
import random
import re

PATTERN = re.compile(
    r"^(?P<count>\d*)d(?P<sides>\d+)(?P<modifier>[+-]\d+)?$",
    re.IGNORECASE,
)


def parse(expression):
    match = PATTERN.match(expression.strip())
    if not match:
        raise ValueError("invalid dice expression")
    count = int(match.group("count") or 1)
    sides = int(match.group("sides"))
    modifier = int(match.group("modifier") or 0)
    if not 1 <= count <= 100:
        raise ValueError("count must be between 1 and 100")
    if not 2 <= sides <= 1000:
        raise ValueError("sides must be between 2 and 1000")
    return count, sides, modifier


def roll(expression, rng=None):
    rng = rng or random.Random()
    count, sides, modifier = parse(expression)
    rolls = [rng.randint(1, sides) for _ in range(count)]
    return {
        "expression": expression,
        "rolls": rolls,
        "modifier": modifier,
        "total": sum(rolls) + modifier,
    }
