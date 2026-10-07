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
