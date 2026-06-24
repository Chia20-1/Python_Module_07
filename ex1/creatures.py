from ex0.creature import Creature
from .heal_capability import HealCapability
from .transform_capability import TransformCapability


class Sproutling(Creature, HealCapability):
    def __init__(self, attribute: str) -> None:
        super().__init__(attribute)

    def attack(self) -> str:
        name = self.name.capitalize()
        return f"{name} uses Vine Whip!"

    def heal(self, target: str) -> str:
        name = self.name.capitalize()
        return f"{name} heals {target} for a small amount."


class Bloomelle(Creature, HealCapability):
    def __init__(self, attribute: str) -> None:
        super().__init__(attribute)

    def attack(self) -> str:
        name = self.name.capitalize()
        return f"{name} uses Petal Dance!"

    def heal(self, target: str) -> str:
        name = self.name.capitalize()
        return f"{name} heals {target} for a large amount."


class Shiftling(Creature, TransformCapability):
    def __init__(self, attribute: str) -> None:
        Creature.__init__(self, attribute)
        TransformCapability.__init__(self)

    def attack(self) -> str:
        name = self.name.capitalize()
        if self.is_transformed is False:
            return f"{name} attacks normally."
        else:
            return f"{name} performs a boosted strike!"

    def transform(self) -> str:
        name = self.name.capitalize()
        self.is_transformed = True
        return f"{name} shifts into a sharper form!"

    def revert(self) -> str:
        name = self.name.capitalize()
        self.is_transformed = False
        return f"{name} returns to normal."


class Morphagon(Creature, TransformCapability):
    def __init__(self, attribute: str) -> None:
        Creature.__init__(self, attribute)
        TransformCapability.__init__(self)

    def attack(self) -> str:
        name = self.name.capitalize()
        if self.is_transformed is False:
            return f"{name} attacks normally."
        else:
            return f"{name} unleashes a devastating morph strike!"

    def transform(self) -> str:
        name = self.name.capitalize()
        self.is_transformed = True
        return f"{name} morphs into a dragonic battle form!"

    def revert(self) -> str:
        name = self.name.capitalize()
        self.is_transformed = False
        return f"{name} stabilizes its form."
