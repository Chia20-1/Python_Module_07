from .battle_strategy import BattleStrategy
from .errors import InvalidCreature, BattleError
from ex0.creature import Creature
from ex1.heal_capability import HealCapability
from ex1.transform_capability import TransformCapability


class NormalStrategy(BattleStrategy):
    def is_valid(self, creature: Creature) -> bool:
        return isinstance(creature, Creature)

    def act(self, creature: Creature) -> None:
        strat_name = self.__class__.__name__
        if self.is_valid(creature):
            print(creature.attack())
        else:
            raise InvalidCreature(
                f"{strat_name} requires a Creature instance, "
                f"got {type(creature).__name__}"
            )


class AggressiveStrategy(BattleStrategy):
    def is_valid(self, creature: Creature) -> bool:
        return (
            isinstance(creature, Creature)
            and isinstance(creature, TransformCapability)
        )

    def act(self, creature: Creature) -> None:
        pass


class DefensiveStrategy(BattleStrategy):
    def is_valid(self, creature: Creature) -> bool:
        return (
            isinstance(creature, Creature)
            and isinstance(creature, HealCapability)
        )

    def act(self, creature: Creature) -> None:
        pass
