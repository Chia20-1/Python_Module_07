# Exercise 2 - Phase 4: Build the Tournament Function

Phase 4 creates the single function that runs a tournament. It does not yet
define the three final scenarios; those are added in Phase 5.

## Model One Opponent

The subject defines an opponent as a tuple containing:

1. a `CreatureFactory`;
2. a `BattleStrategy`.

Create a type alias that expresses that structure:

```python
Opponent = tuple[CreatureFactory, BattleStrategy]
```

An opponent is not a creature object yet. The tournament asks the factory to
create that creature.

## Phase 4 Code

Start `tournament.py` with the types and the single tournament function:

```python
from ex0.creature import Creature
from ex0.creature_factory import CreatureFactory
from ex2 import BattleError, BattleStrategy


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
```

## Why There Are Two Tuple Types

Before creation, an opponent contains a factory:

```python
Opponent = tuple[CreatureFactory, BattleStrategy]
```

After creation, a combatant contains the actual creature:

```python
Combatant = tuple[Creature, BattleStrategy]
```

The strategy remains associated with the same opponent throughout the
tournament.

This transformation:

```python
(factory, strategy)
```

becomes:

```python
(factory.create_base(), strategy)
```

Keeping the creature and strategy together prevents them from becoming
misaligned when several opponents are involved.

## Why the Tournament Uses Factories

The caller supplies factories because the earlier exercises established the
abstract factory pattern. The tournament knows only that a
`CreatureFactory` can create a creature:

```python
factory.create_base()
```

It does not need to know whether the result is `Aquabub`, `Sproutling`, or
`Shiftling`.

That is the architectural chain across all three exercises:

```text
factory chooses the creature
strategy chooses the behavior
tournament coordinates the fights
```

Each part has one main responsibility.

## Generating Every Unique Pair Once

The nested loops use indexes:

```python
for first_index in range(len(combatants)):
    for second_index in range(first_index + 1, len(combatants)):
```

The second index starts one position after the first index. This prevents:

- a creature fighting itself;
- the same pair appearing in reverse order;
- duplicate fights.

For three opponents with indexes `0`, `1`, and `2`, the generated pairs are:

```text
(0, 1)
(0, 2)
(1, 2)
```

The loops do not generate:

```text
(0, 0)
(1, 0)
(2, 0)
(2, 1)
```

In general, `n` opponents produce:

```text
n * (n - 1) / 2
```

fights.

## Polymorphism Inside the Tournament

The tournament does not ask which concrete strategy it received:

```python
first_strategy.act(first_creature)
```

That one call can result in:

- a normal attack;
- a transform, attack, and revert sequence;
- an attack and heal sequence.

The tournament controls when a creature acts. The strategy controls how it
acts. This separation is the purpose of the strategy pattern.

Avoid logic like:

```python
if isinstance(strategy, AggressiveStrategy):
    ...
elif isinstance(strategy, DefensiveStrategy):
    ...
```

That would move strategy-specific knowledge back into the tournament and
defeat the pattern.

## Exception Boundary

Strategies raise `InvalidCreature` when a combination is unsuitable.
`InvalidCreature` inherits from `BattleError`, so the tournament can catch:

```python
except BattleError as error:
```

The tournament is the correct boundary for presenting a friendly failure
message because it coordinates the whole operation.

The exception stops the current tournament without producing an unhandled
traceback. The program can then continue to a later tournament scenario.

## Phase 4 Checks

Before adding final scenarios, confirm that:

- the function accepts `list[Opponent]`;
- every opponent contains a factory and a strategy;
- creatures are created through `create_base`;
- every unique pair fights exactly once;
- each creature acts through its associated strategy;
- no strategy-specific `if` chain exists in the tournament;
- `BattleError` is caught around the tournament fights;
- an invalid combination aborts gracefully.
