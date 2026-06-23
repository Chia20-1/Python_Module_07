from ex0.creature_factory import CreatureFactory
from ex1.factories import HealingCreatureFactory


def test_healing_factory() -> None:
    print("Testing Creature with healing capability")
    print(" base:")
    healing_factory = HealingCreatureFactory()
    base = healing_factory.create_base()
    evolved = healing_factory.create_evolved()
    print(base.describe())
    print(base.attack())
    print(base.heal("itself"))
    print(evolved.describe())
    print(evolved.attack())
    print(evolved.heal("itself and others"))


if __name__ == "__main__":
    test_healing_factory()
    print()
