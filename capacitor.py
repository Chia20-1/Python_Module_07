from ex1.factories import HealingCreatureFactory, TransformCreatureFactory


def test_healing_factory() -> None:
    print("Testing Creature with healing capability")
    print(" base:")
    healing_factory = HealingCreatureFactory()
    base = healing_factory.create_base()
    evolved = healing_factory.create_evolved()
    print(base.describe())
    print(base.attack())
    print(base.heal("itself"))
    print(" evolved:")
    print(evolved.describe())
    print(evolved.attack())
    print(evolved.heal("itself and others"))


def test_transform_factory() -> None:
    print("Testing Creature with transform capability")
    print(" base:")
    transform_factory = TransformCreatureFactory()
    base = transform_factory.create_base()
    evolved = transform_factory.create_evolved()
    print(base.describe())
    print(base.attack())
    print(base.transform())
    print(base.attack())
    print(base.revert())
    print(" evolved:")
    print(evolved.describe())
    print(evolved.attack())
    print(evolved.transform())
    print(evolved.attack())
    print(evolved.revert())


if __name__ == "__main__":
    test_healing_factory()
    print()
    test_transform_factory()
