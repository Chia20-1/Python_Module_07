from ex0.creature import Creature
from ex0.creature_factory import CreatureFactory
from .creatures import Sproutling, Bloomelle


class HealingCreatureFactory(CreatureFactory):
    def create_base(self) -> Creature:
        return Sproutling("Grass")

    def create_evolved(self) -> Creature:
        return Bloomelle("Grass/Fairy")
