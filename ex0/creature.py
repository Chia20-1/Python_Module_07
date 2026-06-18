from abc import ABC, abstractmethod


class Creature(ABC):
    def __init__(self, attribute) -> None:
        self.name = self.__class__.__name__
        self.attribute = attribute

    @abstractmethod
    def attack(self) -> str:
        pass

    def describe(self) -> str:
        name = self.name.capitalize()
        attr = self.attribute.capitalize()
        return f"{name} is a {attr} type Creature"
