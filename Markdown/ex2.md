# Exercise 2 Review and Completion Roadmap

This review compares the current `ex2/` package and `tournament.py` with
Exercise 2 in `en.subject.pdf`.

## What Is Correct So Far

- `BattleStrategy` is an abstract class.
- `BattleStrategy` defines both required abstract methods: `is_valid` and
  `act`.
- The method annotations match their intended result types.
- `NormalStrategy` accepts actual `Creature` instances.
- `NormalStrategy.act` performs the creature's attack.
- `NormalStrategy.act` raises a dedicated exception for an invalid object and
  provides a clear message.
- A dedicated `InvalidCreature` exception exists.
- Exercise 2 reuses the creature and capability structure from Exercises 0
  and 1.

## Errors and Requirement Mismatches

### 1. The Specialized Validation Methods Do Not Always Return a Boolean

`AggressiveStrategy.is_valid` and `DefensiveStrategy.is_valid` return `False`
when the value is not a `Creature`, but they have no return value for an actual
`Creature`.

Their current result is therefore `None` for every real creature. This does not
match the declared `bool` return type or the exercise requirement.

### 2. The Specialized Strategies Do Not Check Capabilities Yet

The aggressive strategy must distinguish creatures with the required
transforming capability from ordinary creatures and healing creatures.

The defensive strategy must distinguish creatures with the required healing
capability from ordinary creatures and transforming creatures.

Validation should account for both parts of the requirement: the object must be
a creature and must have the capability required by that strategy.

### 3. Two Required Actions Are Still Empty

`AggressiveStrategy.act` and `DefensiveStrategy.act` currently contain only
`pass`, so neither strategy performs its required sequence of actions.

They also do not yet reject invalid creature-strategy combinations.

### 4. The Package Does Not Expose All Three Strategies

`ex2/__init__.py` currently exposes only `NormalStrategy`. The aggressive and
defensive strategies are not available through the `ex2` package interface,
which the tournament script will need.

### 5. Exception Responsibilities Are Not Clear Yet

`InvalidCreature` is used, but `BattleError` is currently unused. In addition,
`BattleError` is imported in `strategies.py` without being used, which is a
likely `flake8` error.

Before completing the tournament, decide which exception the strategies raise
and make sure the tournament catches that same exception. If both exception
classes remain, each should have a clear and distinct purpose.

### 6. The Current Invalid Test Conflicts With Its Type Annotation

The tournament passes a `str` to a method whose parameter is annotated as
`Creature`. Although the runtime exception test works, this is expected to
produce a `mypy` argument-type error.

The exercise's required invalid case is an incompatible combination of a real
creature and a strategy, so the final tournament should test that requirement
without contradicting the method's annotation.

### 7. `tournament.py` Does Not Implement the Required Tournament Yet

The current script:

- creates only the normal strategy;
- directly tests one creature instead of defining opponents;
- has no single battle function;
- has no list of factory-strategy tuples;
- does not make every opponent fight every other opponent once;
- does not use each opponent's associated strategy during a fight;
- does not handle an invalid creature-strategy tuple at the tournament level;
- does not demonstrate the basic, error, and multiple-opponent scenarios.

## Steps to Complete the Work

### Phase 1: Complete Strategy Validation

1. Review the capability abstractions from Exercise 1.
2. Define the exact acceptance rule for each of the three strategies.
3. Complete every branch of each `is_valid` method so it always returns either
   `True` or `False`.
4. Check each specialized strategy against:
   - a normal creature;
   - a healing creature;
   - a transforming creature;
   - a value that is not a creature.
5. Confirm that only the intended combinations are accepted.

### Phase 2: Complete Strategy Actions

1. Make each `act` method validate its creature before performing an action.
2. Raise the chosen dedicated exception when the combination is invalid.
3. Include the creature and strategy information in the error message so the
   failed combination is easy to identify.
4. For the aggressive strategy, perform the three actions in the order stated
   in the subject.
5. For the defensive strategy, perform the two actions in the order stated in
   the subject.
6. Make sure returned action messages are displayed by the strategy.
7. Verify that a transforming creature is back in its normal state after its
   strategy finishes.

### Phase 3: Finish the Package Interface

1. Decide which strategy and exception classes should be public.
2. Update the package exports so the tournament can import all required public
   classes from `ex2`.
3. Remove unused imports or connect them to their intended responsibility.
4. Confirm that concrete creatures are still obtained through their factories,
   rather than being exposed by the earlier exercise packages.

### Phase 4: Design the Single Tournament Function

1. Add type annotations for one opponent and for the collection of opponents.
2. Represent every opponent using the factory-strategy tuple required by the
   subject.
3. Define one battle function that receives the complete opponent collection.
4. Create the creature associated with each opponent through its factory.
5. Print the tournament heading and opponent count.
6. Generate each unique pair of opponents exactly once.
7. For every pair:
   - print the battle heading;
   - display both creature descriptions;
   - announce the fight;
   - invoke each creature's associated strategy.
8. Catch the dedicated strategy exception at the tournament boundary.
9. Print a clear tournament error and stop the current tournament gracefully
   when a combination is invalid.

### Phase 5: Build the Required Scenarios

1. Create all three strategy objects.
2. Create suitable factories from Exercises 0 and 1.
3. Add a basic two-opponent tournament with valid combinations.
4. Add a tournament containing one intentionally incompatible combination.
5. Add a three-opponent tournament that exercises normal, defensive, and
   aggressive behavior.
6. Confirm that three opponents produce three unique fights, not duplicate
   reversed fights or self-fights.

### Phase 6: Final Checks

1. Run `tournament.py` and compare the behavior and ordering with the subject.
2. Test every valid and invalid strategy-creature combination separately.
3. Confirm that invalid input is handled without an unhandled crash.
4. Run `flake8` over `ex2/` and `tournament.py`.
5. Run `mypy` over `ex2/` and `tournament.py`.
6. Check that all functions and methods have complete type annotations.
7. Check that the package contains its mandatory `__init__.py`.
8. Be prepared to explain how the strategy pattern keeps tournament logic
   independent from each creature's capability-specific behavior.

## Tooling Note

`flake8` and `mypy` are not installed in the current Python environment, so
they could not be executed during this review. The missing boolean return paths,
the incompatible `str` argument, and the unused `BattleError` import should be
checked first when those tools are available.
