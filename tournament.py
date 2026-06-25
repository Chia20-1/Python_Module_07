from typing import TypeAlias
from ex0.creature import Creature
from ex0 import AquaFactory, FlameFactory, CreatureFactory
from ex1 import HealingCreatureFactory, TransformCreatureFactory
from ex2 import (
    BattleError,
    BattleStrategy,
    NormalStrategy,
    AggressiveStrategy,
    DefensiveStrategy,
)


Opponent: TypeAlias = tuple[CreatureFactory, BattleStrategy]
Combatant: TypeAlias = tuple[Creature, BattleStrategy]


def battle(opponents: list[Opponent]) -> None:
    print("*** Tournament ***")
    print(f"{len(opponents)} opponents involved.\n")

    combatants: list[Combatant] = [
        (factory.create_base(), strategy)
        for factory, strategy in opponents
    ]
    try:
        for first_index in range(len(combatants)):
            for second_index in range(first_index + 1, len(combatants)):
                creature_one, strategy_one = combatants[first_index]
                creature_two, strategy_two = combatants[second_index]
                print(creature_one.describe())
                print(" vs.")
                print(creature_two.describe())
                print(" now fight!")
                strategy_one.act(creature_one)
                strategy_two.act(creature_two)
    except BattleError as e:
        print("BattleError, aborting tournament: ", e)


if __name__ == "__main__":
    aqua_factory = AquaFactory()
    flame_factory = FlameFactory()
    healing_factory = HealingCreatureFactory()
    transform_factory = TransformCreatureFactory()

    normal = NormalStrategy()
    aggressive = AggressiveStrategy()
    defensive = DefensiveStrategy()

    basic_opponents = [(flame_factory, normal), (healing_factory, defensive)]
    error_opponents = [
        (flame_factory, aggressive),
        (healing_factory, defensive),
    ]
    multiple_opponents = [
        (aqua_factory, normal),
        (healing_factory, defensive),
        (transform_factory, aggressive),
    ]

    print("Tournament 0 (basic)")
    print("[ (Flameling+Normal), (Healing+Defensive) ]")
    battle(basic_opponents)
    print()
    print("Tournament 1 (error)")
    print("[ (Flameling+Aggressive), (Healing+Defensive) ]")
    battle(error_opponents)
    print()
    print("Tournament 2 (multiple)")
    print("[ (Aquabub+Normal), (Healing+Defensive), (Transform+Aggressive) ]")
    battle(multiple_opponents)
    print()
