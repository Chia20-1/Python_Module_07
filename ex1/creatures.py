from ex0.creature import Creature
from .heal_capability import HealCapability
from .transform_capability import TransformCapability


class Sproutling(Creature, HealCapability):
    def __init__(self, attribute: str) -> None:
        super().__init__(attribute)

    def attack(self) -> str:
        name = self.name.capitalize()
        return f"{name} uses Vine Whip!"

    def heal(self, target: str) -> None:
        name = self.name.capitalize()
        return f"{name} heals {target} for a small amount."


class Bloomelle(Creature, HealCapability):
    def __init__(self, attribute: str) -> None:
        super().__init__(attribute)

    def attack(self) -> str:
        name = self.name.capitalize()
        return f"{name} uses Petal Dance!"

    def heal(self, target: str) -> None:
        name = self.name.capitalize()
        return f"{name} heals {target} for a large amount."


class Shiftling(Creature, TransformCapability):
    def __init__(self, attribute: str) -> None:
        super().__init__(attribute)

    def attack(self) -> str:
        name = self.name.capitalize()


class Morphagon(Creature, TransformCapability):
    def __init__(self, attribute: str) -> None:
        super().__init__(attribute)

    def attack(self) -> str:
        name = self.name.capitalize()
