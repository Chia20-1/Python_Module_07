# Exercise 2 - Phase 5: Add the Tournament Scenarios

Phase 5 connects the tournament function to concrete factories and strategies.
The subject demonstrates three useful cases:

1. a valid basic tournament;
2. a tournament with an invalid combination;
3. a valid tournament with three opponents and all strategy types.

## Complete `tournament.py`

This version combines the Phase 4 function with the Phase 5 scenarios:

```python
from ex0 import AquaFactory, FlameFactory
from ex0.creature import Creature
from ex0.creature_factory import CreatureFactory
from ex1 import HealingCreatureFactory, TransformCreatureFactory
from ex2 import (
    AggressiveStrategy,
    BattleError,
    BattleStrategy,
    DefensiveStrategy,
    NormalStrategy,
)


Opponent = tuple[CreatureFactory, BattleStrategy]
Combatant = tuple[Creature, BattleStrategy]


def battle(opponents: list[Opponent]) -> None:
    print("*** Tournament ***")
    print(f"{len(opponents)} opponents involved")

    combatants: list[Combatant] = [
        (factory.create_base(), strategy)
        for factory, strategy in opponents
    ]

    try:
        for first_index in range(len(combatants)):
            for second_index in range(
                first_index + 1,
                len(combatants),
            ):
                first_creature, first_strategy = combatants[first_index]
                second_creature, second_strategy = combatants[second_index]

                print("* Battle *")
                print(first_creature.describe())
                print(" vs.")
                print(second_creature.describe())
                print(" now fight!")

                first_strategy.act(first_creature)
                second_strategy.act(second_creature)
    except BattleError as error:
        print(f"Battle error, aborting tournament: {error}")


if __name__ == "__main__":
    aqua_factory = AquaFactory()
    flame_factory = FlameFactory()
    healing_factory = HealingCreatureFactory()
    transform_factory = TransformCreatureFactory()

    normal_strategy = NormalStrategy()
    aggressive_strategy = AggressiveStrategy()
    defensive_strategy = DefensiveStrategy()

    basic_opponents: list[Opponent] = [
        (flame_factory, normal_strategy),
        (healing_factory, defensive_strategy),
    ]

    error_opponents: list[Opponent] = [
        (flame_factory, aggressive_strategy),
        (healing_factory, defensive_strategy),
    ]

    multiple_opponents: list[Opponent] = [
        (aqua_factory, normal_strategy),
        (healing_factory, defensive_strategy),
        (transform_factory, aggressive_strategy),
    ]

    print("Tournament 0 (basic)")
    battle(basic_opponents)

    print()
    print("Tournament 1 (error)")
    battle(error_opponents)

    print()
    print("Tournament 2 (multiple)")
    battle(multiple_opponents)
```

## Scenario 1: Basic Valid Tournament

The first tournament associates:

```text
Flame factory + normal strategy
Healing factory + defensive strategy
```

Both combinations are valid:

- the flame factory creates a normal `Creature`, which normal strategy accepts;
- the healing factory creates a creature with `HealCapability`, which defensive
  strategy accepts.

With two opponents, the tournament should produce one fight.

## Scenario 2: Intentional Error

The second tournament associates:

```text
Flame factory + aggressive strategy
```

The factory creates a plain fire creature without `TransformCapability`.
Therefore:

```python
aggressive_strategy.is_valid(flame_creature)
```

is false, and `act` raises `InvalidCreature`.

This scenario is more relevant than passing a string to `act`. The subject asks
you to handle an invalid creature-strategy combination, and this uses a real
creature with an incompatible strategy.

It also respects the `Creature` type annotation. A test such as:

```python
normal_strategy.act("Magikarp")
```

deliberately passes the wrong type and is expected to cause a `mypy` error.
Remove that temporary test from the final tournament.

## Scenario 3: Multiple Opponents

The final tournament associates:

```text
plain water creature       + normal strategy
healing creature           + defensive strategy
transforming creature      + aggressive strategy
```

All three strategy behaviors are exercised.

Three opponents create three unique fights:

```text
water vs healing
water vs transforming
healing vs transforming
```

Each opponent fights every other opponent once.

## Why Strategy Objects Can Be Reused

The strategies in this design do not store per-creature battle state. They
receive a creature through `act` and tell that creature what to do.

Therefore, one `NormalStrategy` object can be reused in multiple opponent
lists:

```python
normal_strategy = NormalStrategy()
```

The transforming state belongs to the creature, not the strategy. The
aggressive strategy also returns the creature to its normal state after every
action sequence.

## Why the `if __name__` Guard Matters

This block:

```python
if __name__ == "__main__":
```

means the scenarios run when you execute:

```text
python tournament.py
```

They do not run automatically if another file imports the `battle` function.
That makes `tournament.py` usable both as a script and as an importable module.

## Phase 5 Checks

Run the script and verify:

- Tournament 0 completes normally.
- Tournament 1 prints a clear error and does not show a traceback.
- Tournament 2 still runs after Tournament 1 is aborted.
- Tournament 2 contains exactly three battles.
- normal strategy attacks once per fight;
- defensive strategy attacks and heals;
- aggressive strategy transforms, uses the transformed attack, and reverts;
- every creature was produced by a factory;
- no concrete creature class is imported into `tournament.py`.
