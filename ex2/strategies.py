from .battle_strategy import BattleStrategy
from .errors import BattleError
from ex0.creature import Creature
from ex1.heal_capability import HealCapability
from ex1.transform_capability import TransformCapability


class NormalStrategy(BattleStrategy):
    def is_valid(self, creature: Creature) -> bool:
        return isinstance(creature, Creature)

    def act(self, creature: Creature) -> None:
        strat_name = self.__class__.__name__
        if not self.is_valid(creature):
            raise BattleError(
                f"{strat_name} requires a Creature instance, "
                f"got {type(creature).__name__}"
            )
        print(creature.attack())


class AggressiveStrategy(BattleStrategy):
    def is_valid(self, creature: Creature) -> bool:
        return (
            isinstance(creature, Creature)
            and isinstance(creature, TransformCapability)
        )

    def act(self, creature: Creature) -> None:
        if not self.is_valid(creature):
            raise BattleError(
                f'Invalid Creature "{creature.__class__.__name__}" '
                f"for this aggressive strategy."
            )
        assert isinstance(creature, TransformCapability)
        print(creature.transform())
        print(creature.attack())
        print(creature.revert())


class DefensiveStrategy(BattleStrategy):
    def is_valid(self, creature: Creature) -> bool:
        return (
            isinstance(creature, Creature)
            and isinstance(creature, HealCapability)
        )

    def act(self, creature: Creature) -> None:
        if not self.is_valid(creature):
            raise BattleError(
                f'Invalid Creature "{creature.__class__.__name__}" '
                f"for this defensive strategy."
            )
        assert isinstance(creature, HealCapability)
        print(creature.attack())
        print(creature.heal())
