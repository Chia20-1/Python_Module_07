from .creature import Creature


class Flameling(Creature):
    def __init__(self, attribute: str) -> None:
        super().__init__(attribute)

    def attack(self) -> str:
        name = self.name.capitalize()
        return f"{name} uses Ember!"


class Pyrodon(Creature):
    def __init__(self, attribute: str) -> None:
        super().__init__(attribute)

    def attack(self) -> str:
        name = self.name.capitalize()
        return f"{name} uses Flamethrower!"


class Aquabub(Creature):
    def __init__(self, attribute: str) -> None:
        super().__init__(attribute)

    def attack(self) -> str:
        name = self.name.capitalize()
        return f"{name} uses Water Gun!"


class Torragon(Creature):
    def __init__(self, attribute: str) -> None:
        super().__init__(attribute)

    def attack(self) -> str:
        name = self.name.capitalize()
        return f"{name} uses Hydro Pump!"
