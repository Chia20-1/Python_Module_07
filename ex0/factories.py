from .creature import Creature
from .creature_factory import CreatureFactory
from .creatures import Flameling, Aquabub, Pyrodon, Torragon


class FlameFactory(CreatureFactory):
    def create_base(self) -> Creature:
        return Flameling("Fire")

    def create_evolved(self) -> Creature:
        return Pyrodon("Fire/Flying")


class AquaFactory(CreatureFactory):
    def create_base(self) -> Creature:
        return Aquabub("Water")

    def create_evolved(self) -> Creature:
        return Torragon("Water")
