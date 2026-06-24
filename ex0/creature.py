from abc import ABC, abstractmethod


class Creature(ABC):
    def __init__(self, attribute: str) -> None:
        self.name = self.__class__.__name__
        self.attribute = attribute

    @abstractmethod
    def attack(self) -> str:
        pass

    def describe(self) -> str:
        name = self.name.capitalize()
        return f"{name} is a {self.attribute} type Creature"
