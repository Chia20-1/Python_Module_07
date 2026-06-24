# Exercise 2 - Phase 3: Finish the Package Interface

Phase 3 organizes `ex2` as a clean package. It defines which names callers may
import and gives the two exception classes distinct responsibilities.

## Recommended Exception Relationship

Use `BattleError` as the general error category and `InvalidCreature` as a more
specific battle error:

```python
class BattleError(Exception):
    pass


class InvalidCreature(BattleError):
    pass
```

Place this in `ex2/errors.py`.

The inheritance relationship means:

```text
InvalidCreature is a BattleError
```

Strategies can raise the precise `InvalidCreature` exception:

```python
raise InvalidCreature(...)
```

The tournament can catch the broader category:

```python
except BattleError as error:
```

This leaves room for more battle-related exceptions later without requiring
the tournament to add a separate `except` block for every subtype.

## Remove the Unused Import

After adopting that responsibility split, `strategies.py` only raises
`InvalidCreature`. Its local import should therefore be:

```python
from .errors import InvalidCreature
```

Do not import `BattleError` into that file unless the file actually uses it.
Unused imports are reported by `flake8`.

## Public Package Interface

Use `ex2/__init__.py` to expose the classes that the tournament needs:

```python
from .battle_strategy import BattleStrategy
from .errors import BattleError, InvalidCreature
from .strategies import (
    AggressiveStrategy,
    DefensiveStrategy,
    NormalStrategy,
)

__all__ = [
    "BattleStrategy",
    "BattleError",
    "InvalidCreature",
    "NormalStrategy",
    "AggressiveStrategy",
    "DefensiveStrategy",
]
```

The tournament can then use one clean package-level import:

```python
from ex2 import (
    AggressiveStrategy,
    BattleError,
    BattleStrategy,
    DefensiveStrategy,
    NormalStrategy,
)
```

## What `__init__.py` Does

A package's `__init__.py` acts like its front desk. The internal files may be
organized across several modules, while callers interact with a small,
intentional interface.

Without package exports, a caller might need to know the internal layout:

```python
from ex2.strategies import AggressiveStrategy
from ex2.errors import BattleError
from ex2.battle_strategy import BattleStrategy
```

With the exports, the caller only needs to know the package:

```python
from ex2 import AggressiveStrategy, BattleError, BattleStrategy
```

This reduces coupling. Internal files can be reorganized later with less impact
on client code.

## Why Export `BattleStrategy`

The tournament stores different concrete strategies in the same collection.
Their shared type is `BattleStrategy`:

```python
tuple[CreatureFactory, BattleStrategy]
```

Exporting the abstraction allows the tournament's type annotations to describe
all three concrete strategies with one type.

This is polymorphism:

```text
NormalStrategy      \
AggressiveStrategy   -> can all be treated as BattleStrategy
DefensiveStrategy   /
```

The tournament does not need separate code paths for each concrete strategy.
It only calls the common `act` method.

## What Should Not Be Exposed

Exercise 0 and Exercise 1 deliberately expose factories instead of concrete
creature classes. Keep using:

```python
from ex0 import AquaFactory, FlameFactory
from ex1 import HealingCreatureFactory, TransformCreatureFactory
```

The tournament should obtain creatures through those factories. It should not
import `Aquabub`, `Sproutling`, or `Shiftling` directly.

This preserves the abstract factory design from the earlier exercises.

## Formatting Detail

Use spaces for indentation in `__all__`:

```python
__all__ = [
    ...
]
```

Python accepts tabs in some contexts, but mixing tabs and spaces is fragile and
can trigger style warnings. The project requires `flake8`, so consistent
four-space indentation is the safer choice.

## Phase 3 Checks

After completing the package interface, this import should succeed:

```python
from ex2 import (
    AggressiveStrategy,
    BattleError,
    BattleStrategy,
    DefensiveStrategy,
    InvalidCreature,
    NormalStrategy,
)
```

Also check:

- `InvalidCreature` inherits from `BattleError`.
- `strategies.py` has no unused `BattleError` import.
- all three concrete strategies are exported;
- `BattleStrategy` is exported for type annotations;
- the package still has its mandatory `__init__.py`;
- the tournament does not import concrete creatures directly.
