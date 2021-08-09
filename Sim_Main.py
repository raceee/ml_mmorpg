import numpy as np
import random
import math
import matplotlib.pyplot as plt

class Boss:
    def __init__(self, bs_name, bs_health, boss_attack, armour, attack_vector, defense_vector):
        self.boss_name = bs_name
        self.boss_health = bs_health
        self.boss_attack = boss_attack
        self.boss_armour = armour
        self.initial_boss_defense_vector = attack_vector
        self.initial_boss_offense_vector = defense_vector
    
    def set_boss_attack(self):
        l2 = math.sqrt(sum([stat**2 for stat in self.initial_boss_offense_vector]))
        self.attack_vector = [power / l2 for power in self.initial_boss_offense_vector]
    
    def set_boss_defense(self):
        l2 = math.sqrt(sum([stat**2 for stat in self.initial_boss_defense_vector]))
        self.defense_vector = [power / l2 for power in self.initial_boss_defense_vector]

    def boss_attack(self):
        return self.player_attack * self.attack_vector
    
    def boss_defend(self):
        return self.boss_armour * self.defense_vector
    
    def get_bs_health(self):
        return self.bs_health

    def bs_loose_health(self, damage):
        self.boss_health -= damage #fantastic code tripp
    
    def vector_set(self):
        return
    
    def boss_optimize(self, dataframe):
        pass


class Player:
    """
    Deprecated too much work, but useful to have for future testing
    Replaced with Raid for short term use
    """
    def __init__(self, pl_name, pl_health, pl_attack, pl_armour, attack_vector, defense_vector):
        self.player_name = pl_name
        self.player_health = pl_health
        self.player_attack = pl_attack
        self.player_armour = pl_armour
        self.initial_player_defense_vector = attack_vector
        self.initial_player_offense_vector = defense_vector
        self.is_dead = False

    def set_player_attack(self):
        l2 = math.sqrt(sum([stat**2 for stat in self.initial_player_offense_vector]))
        self.attack_vector = [power / l2 for power in self.initial_player_offense_vector]
    
    def set_player_defense(self):
        l2 = math.sqrt(sum([stat**2 for stat in self.initial_player_defense_vector]))
        self.defense_vector = [power / l2 for power in self.initial_player_defense_vector]
    
    def player_attack(self):
        if self.is_dead:
            return 0
        return self.player_attack * self.attack_vector
    
    def player_defend(self):
        if self.is_dead:
            return 0
        return self.player_armour * self.defense_vector
    
    def take_damage(self, damage):
        self.player_health -= damage


class Raid:
    def __init__(self, boss, raid_health, raid_attack, raid_defense):
        self.boss = boss
        self.raid_health = raid_health
        self.raid_attack = raid_attack
        self.raid_defense = raid_defense
        self.set_raid_attack()
        self.set_raid_defense()
    
    def set_raid_attack(self):
        self.normed_attack_vector = self.raid_attack / np.linalg.norm(self.raid_attack)
    
    def set_raid_defense(self):
        self.normed_defesnse_vector = self.raid_defense / np.linalg.norm(self.raid_defense)
    
    # @property
    def get_raid_attack(self):
        return self.normed_attack_vector
    
    @property
    def get_raid_defense(self):
        return self.normed_defesnse_vector


def vis_encounters(list_of_raids):
    return np.vstack([raid.get_raid_attack() for raid in list_of_raids])



if __name__ == "__main__":
    # boss vectors
    boss_attack_vector = np.random.rand(1,3)
    boss_defense_vector = np.random.rand(1,3)
    sire_denathrius = Boss("sire_denathrius", bs_health=10**6, boss_attack=10000, armour=10000, attack_vector=boss_attack_vector, defense_vector=boss_defense_vector)

    meta_vectors_attack = []
    meta_vectors_defense = []
    for _ in range(100):
        a = np.random.rand(1,3)
        a[0,2] += 1 # creates a bias in the vector hence a "meta"
        a[0,0] += 0.5
        meta_vectors_attack.append(a)
        d = np.random.rand(1,3)
        d[0,1] += 1
        d[0,2] += 0.5
        meta_vectors_defense.append(d)
    meta_raids = [Raid(sire_denathrius, raid_health=10**6, raid_attack=attack, raid_defense=defense) for attack, defense in zip(meta_vectors_attack, meta_vectors_defense)]
    
    non_meta_attack_vectors = [np.random.rand(1,3) for _ in range(120)]
    non_meta_defense_vectors = [np.random.rand(1,3) for _ in range(120)]
    non_meta_raids = [Raid(sire_denathrius, raid_health=10**6, raid_attack=attack, raid_defense=defense) for attack, defense in zip(non_meta_attack_vectors, non_meta_defense_vectors)]
    all_raids = meta_raids + non_meta_raids
    print(len(all_raids))
    vissy = vis_encounters(all_raids)
    fig = plt.figure()
    ax = fig.add_subplot(projection="3d")
    ax.scatter(vissy[:][0], vissy[:][1], vissy[:][2])
    plt.show()


