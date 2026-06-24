# Exercise 2 - Phase 6: Final Verification

Phase 6 does not add another feature. It checks correctness, typing, style,
package structure, and your understanding of the design.

## 1. Run the Tournament

From the repository root, run:

```text
python tournament.py
```

Check behavior rather than comparing only punctuation or blank lines.

The important results are:

- the basic tournament has two opponents and one valid fight;
- the error tournament reports the incompatible aggressive strategy and
  aborts gracefully;
- the multiple tournament has three opponents and three unique fights;
- healing happens after attacking;
- transformation happens before attacking;
- reversion happens after the transformed attack.

## 2. Check the Number of Fights

Use this formula:

```text
number of fights = n * (n - 1) / 2
```

Expected values:

| Opponents | Expected fights |
| ---: | ---: |
| 0 | 0 |
| 1 | 0 |
| 2 | 1 |
| 3 | 3 |
| 4 | 6 |

For the required three-opponent scenario, seeing anything other than three
fights indicates a pairing-loop error.

Common pairing mistakes include:

- letting an opponent fight itself;
- running both `A vs B` and `B vs A`;
- skipping the final pair.

## 3. Check Every Strategy Combination

The expected validation matrix is:

| Creature kind | Normal | Aggressive | Defensive |
| --- | ---: | ---: | ---: |
| Plain creature | `True` | `False` | `False` |
| Healing creature | `True` | `False` | `True` |
| Transforming creature | `True` | `True` | `False` |

Also verify that calling `act` for each false specialized combination raises
the dedicated exception instead of producing `AttributeError`.

An `AttributeError` usually means the strategy called a capability method
without validating the capability first.

## 4. Check Transforming State

After aggressive strategy finishes, verify:

```python
transforming_creature.is_transformed is False
```

This matters because the same opponent can participate in several fights. If
the creature remains transformed, later fights begin in the wrong state.

The strategy should preserve this invariant:

```text
before act:  normal state
after act:   normal state
```

The temporary transformed state exists only inside the action sequence.

## 5. Run Style Checking

Run:

```text
python -m flake8 ex2 tournament.py
```

Pay particular attention to:

- unused imports;
- lines longer than the configured limit;
- tabs instead of spaces;
- missing blank lines;
- trailing whitespace.

Likely cleanup points from the earlier version are:

- remove the unused `BattleError` import from `strategies.py`;
- use spaces in `ex2/__init__.py`;
- remove factories or variables that the final scenarios do not use.

`flake8` is a development tool, not a library used by the submitted program.
If the command is unavailable, install it in your development environment
before the final check.

## 6. Run Type Checking

Run:

```text
python -m mypy ex2 tournament.py
```

Check especially:

- every method has a complete parameter and return annotation;
- `is_valid` always returns `bool`;
- specialized capability methods are called only after type narrowing;
- opponent collections use `CreatureFactory` and `BattleStrategy`;
- no string is passed where a `Creature` is required.

Remove the temporary call that passes `"Magikarp"` to `act`. It tests runtime
defensiveness, but it intentionally violates the declared parameter type and
does not represent the subject's required invalid combination.

## 7. Check Package Imports

This package-level import should work:

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

Also confirm:

- `ex2/__init__.py` exists;
- `InvalidCreature` inherits from `BattleError`;
- all three strategies inherit from `BattleStrategy`;
- earlier packages expose factories rather than concrete creatures.

## 8. Check Repository Cleanliness

Generated Python cache directories should not be submitted:

```text
__pycache__/
*.pyc
```

Inspect your Git status before submission and ensure only intended source and
documentation files are included.

Do not delete or overwrite unrelated work merely to make the status empty.
Review each changed file and keep changes you understand.

## 9. Understand the Three Patterns

You may be asked to explain the design during evaluation.

### Abstract Factory

`CreatureFactory` creates related creature objects without making the caller
depend on concrete creature classes.

Memory hook:

```text
The factory decides what object is created.
```

### Capabilities Through Multiple Inheritance

`HealCapability` and `TransformCapability` describe optional behavior that can
be added to suitable creatures.

Memory hook:

```text
The capability describes what extra actions an object supports.
```

### Strategy

`BattleStrategy` packages different battle action sequences behind the same
`act` interface.

Memory hook:

```text
The strategy decides how the object behaves in battle.
```

Together:

```text
Factory  -> creates a creature
Capability -> tells what the creature can do
Strategy -> chooses how those abilities are used
Tournament -> coordinates opponents without knowing concrete details
```

## 10. Questions You Should Be Able to Answer

1. Why does `AggressiveStrategy` check `TransformCapability` instead of
   checking for `Shiftling`?
2. Why does `DefensiveStrategy` heal after attacking?
3. Why must aggressive strategy call `revert`?
4. Why is an opponent represented by a factory-strategy tuple?
5. How does the nested loop prevent duplicate fights?
6. Why can the tournament call `act` without knowing the concrete strategy?
7. Why does `InvalidCreature` inherit from `BattleError`?
8. Why should the invalid scenario use a real creature with an incompatible
   strategy instead of a string?

If you can explain those answers in your own words, you understand the design
rather than only having code that produces the expected output.

## Final Checklist

- [ ] All three `is_valid` methods return only `True` or `False`.
- [ ] All three `act` methods implement the correct sequence.
- [ ] Invalid combinations raise `InvalidCreature`.
- [ ] `InvalidCreature` inherits from `BattleError`.
- [ ] `ex2` exports its public strategy and exception classes.
- [ ] The tournament accepts factory-strategy tuples.
- [ ] Every unique opponent pair fights exactly once.
- [ ] Invalid tournaments abort without an unhandled traceback.
- [ ] A later tournament can run after an earlier tournament error.
- [ ] `flake8` reports no errors.
- [ ] `mypy` reports no errors.
- [ ] No concrete creature is imported into the tournament.
- [ ] No generated cache files are included in the submission.
- [ ] You can explain the abstract factory, capability, and strategy roles.
