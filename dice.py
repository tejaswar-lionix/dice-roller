#!/usr/bin/env python3
"""Parse and roll dice expressions like 2d6+3."""
import random
import re

PATTERN = re.compile(
    r"^(?P<count>\d*)d(?P<sides>\d+)(?P<modifier>[+-]\d+)?$",
    re.IGNORECASE,
)
KEEP_PATTERN = re.compile(
    r"^(?P<count>\d*)d(?P<sides>\d+)(?P<mode>kh|kl)(?P<keep>\d+)(?P<modifier>[+-]\d+)?$",
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


def parse_keep(expression):
    match = KEEP_PATTERN.match(expression.strip())
    if not match:
        return None
    count = int(match.group("count") or 1)
    sides = int(match.group("sides"))
    modifier = int(match.group("modifier") or 0)
    mode = match.group("mode").lower()
    keep_count = int(match.group("keep"))
    if not 1 <= count <= 100:
        raise ValueError("count must be between 1 and 100")
    if not 2 <= sides <= 1000:
        raise ValueError("sides must be between 2 and 1000")
    if not 1 <= keep_count <= count:
        raise ValueError("keep count must be between 1 and count")
    return count, sides, modifier, mode, keep_count


def roll(expression, rng=None):
    rng = rng or random.Random()
    keep = parse_keep(expression)
    if keep:
        count, sides, modifier, mode, keep_count = keep
        rolls = [rng.randint(1, sides) for _ in range(count)]
        ordered = sorted(rolls, reverse=(mode == "kh"))
        kept = ordered[:keep_count]
        return {
            "expression": expression,
            "rolls": rolls,
            "modifier": modifier,
            "total": sum(kept) + modifier,
            "kept": kept,
        }
    count, sides, modifier = parse(expression)
    rolls = [rng.randint(1, sides) for _ in range(count)]
    return {
        "expression": expression,
        "rolls": rolls,
        "modifier": modifier,
        "total": sum(rolls) + modifier,
    }


def _roll_advantage(sides, rng, choose):
    if not 2 <= sides <= 1000:
        raise ValueError("sides must be between 2 and 1000")
    rng = rng or random.Random()
    rolls = [rng.randint(1, sides) for _ in range(2)]
    kept = choose(rolls)
    return {"rolls": rolls, "kept": kept, "total": kept}


def roll_advantage(sides=20, rng=None):
    """Roll two dice and keep the higher result."""
    return _roll_advantage(sides, rng, max)


def roll_disadvantage(sides=20, rng=None):
    """Roll two dice and keep the lower result."""
    return _roll_advantage(sides, rng, min)


def roll_many(expression, times, rng=None):
    """Roll an expression repeatedly and return totals plus simple statistics."""
    if times < 1:
        raise ValueError("times must be at least 1")
    rng = rng or random.Random()
    totals = [roll(expression, rng)["total"] for _ in range(times)]
    return {
        "totals": totals,
        "minimum": min(totals),
        "maximum": max(totals),
        "average": round(sum(totals) / len(totals), 2),
    }
