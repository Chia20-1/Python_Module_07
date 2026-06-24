from ex0 import AquaFactory, FlameFactory
from ex1 import HealingCreatureFactory, TransformCreatureFactory
from ex2 import NormalStrategy, AggressiveStrategy, DefensiveStrategy
from ex2 import InvalidCreature


if __name__ == "__main__":
    aqua_factory = AquaFactory()
    flame_factory = FlameFactory()
    healing_factory = HealingCreatureFactory()
    transform_factory = TransformCreatureFactory()

    normal = NormalStrategy()
    aggressive = AggressiveStrategy()
    defensive = DefensiveStrategy()

    magikarp: str = "Magikarp"
    print("Extra Test Invalid Creature Instance")
    try:
        normal.act(magikarp)
    except InvalidCreature as e:
        print(e)

    normal_creature = AquaFactory().create_base()
    healing_creature = HealingCreatureFactory().create_base()
    transforming_creature = TransformCreatureFactory().create_base()

    creatures = [
        normal_creature,
        healing_creature,
        transforming_creature,
    ]

    for creature in creatures:
        print(creature.__class__.__name__)
        print("Normal:", normal.is_valid(creature))
        print("Aggressive:", aggressive.is_valid(creature))
        print("Defensive:", defensive.is_valid(creature))
