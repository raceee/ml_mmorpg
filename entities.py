class BaseUnitClass:
    def __init__(self, health, dps, dps_type, defense_spread):
        self.health = health
        self.dps = dps
        self.dps_spread = dps_type
        self.defense_spread = defense_spread
        #FIRE           HOLY        PHYSICAL        NATURE/ELEMENTAL
        #WATER/ICE      SHADOW      RANGE           ARCANE

    def attack(self):
        pass

    def defend(self):
        pass


