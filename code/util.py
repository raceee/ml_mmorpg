class Counter:
    def __init__(self, name):
        self.boss_score = 0
        self.raid_score = 0
        self.name = name
    
    def add(self, tup):
        self.boss_score += tup[0]
        self.raid_score += tup[1]
    
    def __str__(self) -> str:
        string = "--------------------------\n"
        string = string + self.name + "\n\n" + "Boss Score: {}".format(self.boss_score) + "\nRaid Score: {}".format(self.raid_score)
        return string