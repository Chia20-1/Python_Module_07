# Exercise 2 - Phase 1 Solution: Strategy Validation

Phase 1 is only about deciding whether a creature is compatible with a battle
strategy. It does not implement the actions performed by the aggressive or
defensive strategies yet.

## The Validation Rules

Each strategy has a different compatibility rule:

| Strategy | Valid object |
| --- | --- |
| `NormalStrategy` | Any `Creature` |
| `AggressiveStrategy` | A `Creature` with `TransformCapability` |
| `DefensiveStrategy` | A `Creature` with `HealCapability` |

The specialized strategies must check both requirements. For example, having a
method named `transform` is not enough: the object should be both a creature
and an instance of the capability abstraction.

## Code Changes

In `ex2/strategies.py`, import the two capability abstractions:

```python
from ex1.heal_capability import HealCapability
from ex1.transform_capability import TransformCapability
```

Then implement the three validation methods as follows:

```python
class NormalStrategy(BattleStrategy):
    def is_valid(self, creature: Creature) -> bool:
        return isinstance(creature, Creature)


class AggressiveStrategy(BattleStrategy):
    def is_valid(self, creature: Creature) -> bool:
        return (
            isinstance(creature, Creature)
            and isinstance(creature, TransformCapability)
        )


class DefensiveStrategy(BattleStrategy):
    def is_valid(self, creature: Creature) -> bool:
        return (
            isinstance(creature, Creature)
            and isinstance(creature, HealCapability)
        )
```

The existing `act` methods are not part of Phase 1, so leave their current work
for Phase 2.

## Why This Works

### `isinstance` Checks Inheritance

`isinstance(object, SomeClass)` asks whether an object was created from
`SomeClass` or from a class that inherits from it.

For example, `Shiftling` is declared with both parent classes:

```python
class Shiftling(Creature, TransformCapability):
```

Therefore, the same `Shiftling` object satisfies both checks:

```python
isinstance(shiftling, Creature)
isinstance(shiftling, TransformCapability)
```

That is multiple inheritance doing useful work: the creature has its normal
creature identity and an additional capability identity.

Similarly, `Sproutling` inherits from `Creature` and `HealCapability`, so it is
valid for the defensive strategy.

### Why the Checks Use `and`

The aggressive requirement means:

```text
The object is a Creature
AND
the object has TransformCapability
```

Both conditions must be true. If either condition is false, the complete
expression returns `False`.

Python evaluates `and` from left to right. If the first check is false, it does
not need to evaluate the second check. This behavior is called
short-circuiting.

### Why Every Path Now Returns a Boolean

The previous specialized methods had this shape:

```python
if not isinstance(creature, Creature):
    return False
```

If the creature passed that check, execution reached the end of the function
without a `return`. Python then returned `None` automatically.

The new version directly returns the result of a Boolean expression:

```python
return condition_one and condition_two
```

Both `isinstance` calls produce Boolean values, so the final result is always
exactly `True` or `False`.

## Expected Compatibility Table

Using the current creature families, the result should be:

| Creature kind | Normal | Aggressive | Defensive |
| --- | ---: | ---: | ---: |
| Plain creature from `ex0` | `True` | `False` | `False` |
| Healing creature from `ex1` | `True` | `False` | `True` |
| Transforming creature from `ex1` | `True` | `True` | `False` |
| Non-creature value | `False` | `False` | `False` |

This table is a useful mental test. Each specialized creature should be
accepted only by normal strategy and its own capability strategy.

## A Small Validation Test

After updating your code, you can temporarily use this test to inspect the
results:

```python
from ex0 import AquaFactory
from ex1 import HealingCreatureFactory, TransformCreatureFactory
from ex2.strategies import (
    AggressiveStrategy,
    DefensiveStrategy,
    NormalStrategy,
)


normal = NormalStrategy()
aggressive = AggressiveStrategy()
defensive = DefensiveStrategy()

plain_creature = AquaFactory().create_base()
healing_creature = HealingCreatureFactory().create_base()
transforming_creature = TransformCreatureFactory().create_base()

creatures = [
    plain_creature,
    healing_creature,
    transforming_creature,
]

for creature in creatures:
    print(creature.__class__.__name__)
    print("Normal:", normal.is_valid(creature))
    print("Aggressive:", aggressive.is_valid(creature))
    print("Defensive:", defensive.is_valid(creature))
```

Compare the results with the compatibility table rather than only checking
whether the program runs.

## Why Capability Classes Are Better Than Concrete Creature Checks

It would be possible to check individual concrete classes such as `Shiftling`
and `Morphagon`, but that would tightly connect the strategy to today's
creature list.

Checking `TransformCapability` instead means:

```text
Accept any present or future creature that promises transforming behavior.
```

If another transforming creature is added later, the aggressive strategy will
accept it without needing to be edited. This is the main design benefit of
programming against an abstraction.

The same principle applies to `HealCapability`: the defensive strategy cares
about what an object can do, not its exact concrete class name.

## Phase 1 Completion Checklist

- Import `HealCapability`.
- Import `TransformCapability`.
- Keep the normal strategy valid for every `Creature`.
- Require both `Creature` and `TransformCapability` for aggressive strategy.
- Require both `Creature` and `HealCapability` for defensive strategy.
- Ensure every `is_valid` call returns only `True` or `False`.
- Verify plain, healing, and transforming creatures against all three
  strategies.
- Leave action sequences and exceptions for Phase 2.
