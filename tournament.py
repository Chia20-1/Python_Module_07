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

opponent: TypeAlias = tuple[CreatureFactory, BattleStrategy]
combatant: TypeAlias = tuple[Creature, BattleStrategy]

def battle(opponents: list[tuple[CreatureFactory, BattleStrategy]]) -> None:
    pass

if __name__ == "__main__":
    aqua_factory = AquaFactory()
    flame_factory = FlameFactory()
    healing_factory = HealingCreatureFactory()
    transform_factory = TransformCreatureFactory()

    normal = NormalStrategy()
    aggressive = AggressiveStrategy()
    defensive = DefensiveStrategy()
