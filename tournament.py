from ex0 import AquaFactory, FlameFactory
from ex1 import HealingCreatureFactory, TransformCreatureFactory
from ex2 import NormalStrategy
from ex2 import InvalidCreature


if __name__ == "__main__":
    aqua_factory = AquaFactory()
    flame_factory = FlameFactory()
    healing_factory = HealingCreatureFactory()
    transform_factory = TransformCreatureFactory()
    aqua_base = aqua_factory.create_base()
    aqua_evolved = aqua_factory.create_evolved()
    normal_strategy = NormalStrategy()
    magikarp: str = "Magikarp"
    print("Test Invalid Creature Instance")
    normal_strategy.act(aqua_base)
    try:
        normal_strategy.act(magikarp)
    except InvalidCreature as e:
        print(e)