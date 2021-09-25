import numpy as np
import random
import math
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA


class Boss:
    def __init__(self, bs_name, bs_health, boss_attack, armour, attack_vector, defense_vector):
        self.boss_name = bs_name
        self.boss_health = bs_health
        self.boss_dps = boss_attack
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
    def __init__(self, raid_health, raid_attack, raid_defense):
        """
        Class that represents the collection of players seeking to kill the boss
        raid_health:int some number representing the total health of the entire raid
        raid_attack:vector a vector where each element of the vector represents the raids power in a certain 'power'
        raid_defense:vector a vector of the raid and its resistivity to certain types of damage

        """
        self.raid_health = raid_health
        self.raid_attack = raid_attack
        self.raid_defense = raid_defense
        self.set_raid_attack()
        self.set_raid_defense()
    
    def set_raid_attack(self):
        """sets a hidden class attribute that are the normed version of the attack vector"""
        self.normed_attack_vector = self.raid_attack / np.linalg.norm(self.raid_attack)
    
    def set_raid_defense(self):
        """sets a hidden class attribute that are the normed version of the defense vector"""
        self.normed_defense_vector = self.raid_defense / np.linalg.norm(self.raid_defense)
    
    @property
    def get_raid_attack(self):
        return self.normed_attack_vector[0]
    
    @property
    def get_raid_defense(self):
        return self.normed_defense_vector[0]



class SimulationPlate:
    def __init__(self, list_of_raids:list, boss) -> None:
        self.list_of_raids = list_of_raids
        self.boss = boss
        self.raid_attack_vectors = np.squeeze(np.stack([np.asarray(raid.normed_attack_vector) for raid in self.list_of_raids], axis=0))
        self.raid_defense_vectors = np.squeeze(np.stack([np.asarray(raid.normed_defense_vector) for raid in self.list_of_raids], axis=0))
    
    def fight(self):
        '''
        TODO: TRIPP
        This function will be used to simulate a fight
            use being: we want to see the boss win after it optimizes
        
        SPEC:
        The boss must fight each raid of the list_of_raids
            The boss and raid must deal damage that is the difference between the attack vector minus the defense vector IF the attacking vector is a higher value
                EX. If the bosses attacking vector is [5,10,15] the raid defense vector is [7, 9, 13] then the total damage will be 0 + 1 + 2 = 3 total damage
            The boss will attack the raid and see how many "turns" it takes to kill the raid-- the fight will restart and then the raid will attack and see how many turns it takes to kill the boss
            The opponent with the few amount of turns to kill the other player will "win" the fight
        '''

        boss_health_tape = []
        raid_health_tape = []

        boss_full_health = self.boss.boss_health

        boss_true_damage = [self.boss.boss_dps * a for a in self.boss.attack_vector]
        boss_true_defense = [self.boss.boss_armour * b for b in self.boss.defense_vector]

        for raid in self.list_of_raids:
           raid_true_defense = [raid.raid_defense * c for c in raid.normed_defense_vector]
           while raid.raid_health > 0:
               damage_spread = []
               for resistance, dam in zip(raid_true_defense, boss_true_damage):
                  taken_damage = dam - resistance
                  if taken_damage > 0:
                      damage_spread.append(taken_damage)
               damage = sum(damage_spread)
               raid_health_tape.append(raid.raid_health - damage)

        for raid in self.list_of_raids:
            raid_true_attack = [raid.raid_attack * d for d in raid.normed_attack_vector]
            while self.boss.boss_health > 0:
                raid_damage_spread = []
                for resistance, dam in zip(boss_true_defense, raid_true_attack):
                    boss_taken_damage = dam - resistance
                    if boss_taken_damage > 0:
                        raid_damage_spread.append(boss_taken_damage)
                dams = sum(raid_damage_spread)
                boss_health_tape.append(self.boss.boss_health - dams)
            self.boss.boss_health = boss_full_health
        pass
    
    def KNN(self):
        '''
        TODO: RACE
        Implement KNN to the attack and defense vectors for the boss
            1. Mark Regions
            2. Find Centroid of most populated region
        Good reference: https://www.askpython.com/python/examples/plot-k-means-clusters-python
        '''
        # pca = PCA(2)
        # pca_attack = pca.fit_transform(self.raid_attack_vectors)
        attack_fitter = KMeans(n_clusters=8, random_state=0, algorithm="elkan")
        attack_labels = attack_fitter.fit_predict(self.raid_attack_vectors)
        print("inertia", attack_fitter.inertia_)
        print("centers: ", attack_fitter.cluster_centers_)
        print("get params, ", attack_fitter.get_params())
        print("ATTACK LABELS", attack_labels)
        attack_centroids = attack_fitter.cluster_centers_
        all_labels = np.unique(attack_labels)
        (u, c) = np.unique(attack_labels, return_counts=True)
        print("all labels", all_labels)
        print("counts", np.asarray((u,c)).T )
        meta_cluster = np.argmax(np.max(np.asarray((u,c)).T, axis=1))
        print("centers: ", attack_fitter.cluster_centers_[meta_cluster])

 


        for i in all_labels:
            plt.scatter(self.raid_attack_vectors[attack_labels == i, 0], self.raid_attack_vectors[attack_labels == i, 1], label = i)
        plt.scatter(attack_centroids[:,0] , attack_centroids[:,1] , s = 80, color = 'k')
        plt.legend()
        plt.show()

    def vis_raid_attack_vectors(self):
        fig = plt.figure()
        ax = fig.add_subplot(projection="3d")
        for raid in self.list_of_raids:
            ax.scatter(raid.get_raid_attack()[0], raid.get_raid_attack()[1], raid.get_raid_attack()[2])
        plt.show()
    
    def vis_raid_defense_vectors(self):
        fig = plt.figure()
        ax = fig.add_subplot(projection="3d")
        for raid in self.list_of_raids:
            ax.scatter(raid.get_raid_defense()[0], raid.get_raid_defense()[1], raid.get_raid_defense()[2])
        plt.show()

if __name__ == "__main__":
    # boss vectors
    boss_attack_vector = np.random.rand(1,3)
    boss_defense_vector = np.random.rand(1,3)
    sire_denathrius = Boss("sire_denathrius", bs_health=10**6, boss_attack=10000, armour=10000, attack_vector=boss_attack_vector, defense_vector=boss_defense_vector)

    meta_vectors_attack = []
    meta_vectors_defense = []
    for _ in range(100):
        a = np.random.rand(1,3)
        a[0,2] += 10 # creates a bias in the vector hence a "meta"
        a[0,0] += 5
        meta_vectors_attack.append(a)
        d = np.random.rand(1,3)
        d[0,1] += 10
        d[0,2] += 5
        meta_vectors_defense.append(d)
    meta_raids = [Raid(raid_health=10**6, raid_attack=attack, raid_defense=defense) for attack, defense in zip(meta_vectors_attack, meta_vectors_defense)]
    
    non_meta_attack_vectors = [np.random.rand(1,3) for _ in range(120)]
    non_meta_defense_vectors = [np.random.rand(1,3) for _ in range(120)]
    non_meta_raids = [Raid(raid_health=10**6, raid_attack=attack, raid_defense=defense) for attack, defense in zip(non_meta_attack_vectors, non_meta_defense_vectors)]
    all_raids = meta_raids + non_meta_raids
    fight_set = SimulationPlate(all_raids, sire_denathrius)
    fight_set.KNN()
