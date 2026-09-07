def main() -> None:
    print("Welcome to Fantasy Hunter")
    print("This game is still in development, but plan to release soon!")
    print(
        "This game is a text-based adventure game that mimics Fantasy adventure stories,\nyou will face monsters, have turn-based fights, you can explore the vast world of magic,\nlearn new skills, and more!"
    )
    print("Made by Syntax-Overlord")


class Entity:

    def __init__(
        self,
        strength: float = 0,
        dexterity: float = 0,
        constitution: float = 0,
        intelligence: float = 0,
        wisdom: float = 0,
        charisma: float = 0,
    ) -> None:
        self.strength: float = strength
        self.dexterity: float = dexterity
        self.constitution: float = constitution
        self.intelligence: float = intelligence
        self.wisdom: float = wisdom
        self.charisma: float = charisma
        return
