# Exercise 2 - Phase 2: Complete the Strategy Actions

Phase 1 answered this question:

> Is this creature compatible with this strategy?

Phase 2 answers the next question:

> What should the compatible creature do, and what happens if the combination
> is invalid?

This phase changes `ex2/strategies.py`.

## Required Action Sequences

| Strategy | Required sequence |
| --- | --- |
| `NormalStrategy` | attack |
| `AggressiveStrategy` | transform, attack, revert |
| `DefensiveStrategy` | attack, heal |

The order matters. A transforming creature must transform before attacking so
that its boosted attack is used. It must then revert so that its state does not
leak into a later battle.

## Phase 2 Code

Use the following structure in `ex2/strategies.py`:

```python
from .battle_strategy import BattleStrategy
from .errors import InvalidCreature
from ex0.creature import Creature
from ex1.heal_capability import HealCapability
from ex1.transform_capability import TransformCapability


class NormalStrategy(BattleStrategy):
    def is_valid(self, creature: Creature) -> bool:
        return isinstance(creature, Creature)

    def act(self, creature: Creature) -> None:
        if not self.is_valid(creature):
            creature_name = getattr(
                creature,
                "name",
                type(creature).__name__,
            )
            raise InvalidCreature(
                f"Invalid Creature '{creature_name}' "
                "for this normal strategy"
            )

        print(creature.attack())


class AggressiveStrategy(BattleStrategy):
    def is_valid(self, creature: Creature) -> bool:
        return (
            isinstance(creature, Creature)
            and isinstance(creature, TransformCapability)
        )

    def act(self, creature: Creature) -> None:
        if not self.is_valid(creature):
            creature_name = getattr(
                creature,
                "name",
                type(creature).__name__,
            )
            raise InvalidCreature(
                f"Invalid Creature '{creature_name}' "
                "for this aggressive strategy"
            )

        assert isinstance(creature, TransformCapability)
        print(creature.transform())
        print(creature.attack())
        print(creature.revert())


class DefensiveStrategy(BattleStrategy):
    def is_valid(self, creature: Creature) -> bool:
        return (
            isinstance(creature, Creature)
            and isinstance(creature, HealCapability)
        )

    def act(self, creature: Creature) -> None:
        if not self.is_valid(creature):
            creature_name = getattr(
                creature,
                "name",
                type(creature).__name__,
            )
            raise InvalidCreature(
                f"Invalid Creature '{creature_name}' "
                "for this defensive strategy"
            )

        assert isinstance(creature, HealCapability)
        print(creature.attack())
        print(creature.heal("itself"))
```

## The Guard-Clause Pattern

Each `act` method starts with a guard clause:

```python
if not self.is_valid(creature):
    raise InvalidCreature(...)
```

A guard clause deals with an invalid case immediately. Once execution passes
that block, the rest of the method can focus on the valid action sequence.

This is easier to read than deeply nesting the successful behavior:

```python
if self.is_valid(creature):
    ...
else:
    ...
```

The method's story becomes:

1. Reject an invalid combination.
2. Perform the valid behavior.

## Why `getattr` Is Used in the Error Path

Normally, a creature has a `name` attribute:

```python
creature.name
```

However, error-handling code should avoid creating a second error while trying
to describe the first one. `getattr` supplies a fallback:

```python
creature_name = getattr(
    creature,
    "name",
    type(creature).__name__,
)
```

This means:

- use `creature.name` when it exists;
- otherwise, use the object's class name.

For a normal creature, the message can mention `Flameling`. For an unexpected
string, it can still mention `str` instead of crashing with another
`AttributeError`.

## Why the `assert` Is Present

The method has already performed runtime validation:

```python
if not self.is_valid(creature):
    raise InvalidCreature(...)
```

You know that a valid aggressive creature has `TransformCapability`, but a
static type checker does not automatically understand the custom logic hidden
inside `is_valid`.

This line makes the capability explicit:

```python
assert isinstance(creature, TransformCapability)
```

It serves two purposes:

1. It documents the assumption required by the remaining code.
2. It narrows the type so tools such as `mypy` know that `transform` and
   `revert` are available.

The assertion is not replacing your error handling. The guard clause has
already rejected invalid input.

The defensive strategy uses the same idea for `HealCapability`.

## Why Every Returned String Is Printed

The creature methods return descriptions:

```python
creature.attack()
creature.transform()
creature.revert()
creature.heal("itself")
```

Returning a string does not display it. The strategy must print each returned
message:

```python
print(creature.attack())
```

Without `print`, the action might change state, but the tournament output would
not show the action.

## State and the Aggressive Strategy

The transforming creatures keep this state:

```python
self.is_transformed
```

Their attack result depends on that value. Therefore, this order is essential:

```text
transform -> transformed state becomes True
attack    -> boosted attack is selected
revert    -> transformed state becomes False
```

If `attack` happens before `transform`, the ordinary attack is used. If
`revert` is forgotten, the creature incorrectly starts its next battle already
transformed.

## Phase 2 Checks

Test these situations:

1. A plain creature with `NormalStrategy` attacks once.
2. A transforming creature with `AggressiveStrategy` transforms, performs its
   boosted attack, and reverts.
3. A healing creature with `DefensiveStrategy` attacks and then heals.
4. A plain creature with `AggressiveStrategy` raises `InvalidCreature`.
5. A plain creature with `DefensiveStrategy` raises `InvalidCreature`.
6. A transforming creature is no longer transformed after `act` finishes.

Do not build the tournament loop yet. Phase 2 is complete when each strategy
works correctly by itself.
