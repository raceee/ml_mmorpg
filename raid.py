import numpy as np
import math
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans


class Boss:
    def __init__(self, boss_health, boss_attack, boss_defense, dps=1000, armour=1000):
        self.health = boss_health
        self.dps = dps
        self.armour = armour
        self.boss_attack = self.set_boss_attack(boss_attack)
        self.boss_defense = self.set_boss_defense(boss_defense)

    def set_boss_attack(self, attack):
        a = attack / np.sum(attack)
        return a * self.dps

    def set_boss_defense(self, defense):
        d = defense / np.sum(defense)
        return d * self.armour

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
    def __init__(self, raid_health, raid_attack, raid_defense, dps=1000, armour=1000):
        """
        Class that represents the collection of players seeking to kill the boss
        raid_health:int some number representing the total health of the entire raid
        raid_attack:vector a vector where each element of the vector represents the raids power in a certain 'power'
        raid_defense:vector a vector of the raid and its resistivity to certain types of damage

        """
        self.raid_health = raid_health
        self.dps = dps
        self.armour = armour
        self.raid_attack = self.set_raid_attack(raid_attack)
        self.raid_defense = self.set_raid_defense(raid_defense)

    
    def set_raid_attack(self, attack_vec):
        """sets a hidden class attribute that are the normed version of the attack vector"""
        a = attack_vec / np.sum(attack_vec)
        return a * self.dps

    
    def set_raid_defense(self, defense_vec):
        """sets a hidden class attribute that are the normed version of the defense vector"""
        d = defense_vec / np.sum(defense_vec)
        return d * self.armour



class SimulationPlate:
    def __init__(self, list_of_raids:list, boss) -> None:
        self.list_of_raids = list_of_raids
        self.boss = boss
    
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
        allraid_lifespan = []
        boss_lifespan = []
        for raid in self.list_of_raids:
            raidhp = raid.raid_health
            raid_health_tape = [] # tracks how many "turns" it took for the boss to kill specific raid
            boss_health_tape = []
            # Boss attacks
            while raidhp > 0:
                total_damage = raid.raid_defense - self.boss.boss_attack
                total_damage = np.sum(total_damage, where=total_damage<0)
                if total_damage < 0:
                    raid_health_tape.append(total_damage)
                    raidhp += total_damage
            print("raid killed")
            allraid_lifespan.append(len(raid_health_tape))
            bosshp = self.boss.health
            # Raid attacks
            while bosshp > 0:
                # print(self.boss.boss_defense)
                # print(raid.raid_attack)
                total_damage = self.boss.boss_defense - raid.raid_attack
                # print(total_damage)
                total_damage = np.sum(total_damage, where=total_damage<0)
                if total_damage < 0:
                    boss_health_tape.append(total_damage)
                    bosshp += total_damage
            print("boss killed")
            boss_lifespan.append(len(boss_health_tape))
        print("raid_lifespan: ", allraid_lifespan)
        print("boss_lifespan: ", boss_lifespan)
                # for resistance, dam in zip(raid.raid_defense, self.boss.boss_attack):
                #     taken_damage = dam - resistance
                #     lost_hp = sum([loss for loss in taken_damage if loss > 0])
                #     print('lost_hp', lost_hp)
                #     if lost_hp > 0:
                #         damage_spread.append(lost_hp)
                # damage = sum(damage_spread)
                # raid_health_tape.append(raid.raid_health - damage)
                # print("Raid Health Tape: ", raid_health_tape, len(raid_health_tape))

        # for raid in self.list_of_raids:
        #     raid_true_attack = [raid.raid_attack * d for d in raid.normed_attack_vector]
        #     while self.boss.boss_health > 0:
        #         raid_damage_spread = []
        #         for resistance, dam in zip(boss_true_defense, raid_true_attack):
        #             boss_taken_damage = dam - resistance
        #             if boss_taken_damage > 0:
        #                 raid_damage_spread.append(boss_taken_damage)
        #         dams = sum(raid_damage_spread)
        #         boss_health_tape.append(self.boss.boss_health - dams)
        #         print("Boss Health Tape: ", boss_health_tape, len(boss_health_tape))
        #     self.boss.boss_health = boss_full_health
        # pass
    
    def KNN(self):
        '''
        returns: vector of the meta -- to be used in setting the appropriate boss vectors
        Notes: the center is chosen by finding the minimum "concentration" future proofing. 
        Some clusters may have more elements but high concentration comparitively
        '''
        attack_fitter = KMeans(n_clusters=8, random_state=0, algorithm="elkan")
        attack_labels = attack_fitter.fit_predict(self.raid_attack_vectors)
        (u, c) = np.unique(attack_labels, return_counts=True)
        counts = np.asarray((u,c)).T
        concentration = []
        for label in np.unique(attack_labels):
            total_err = 0
            for vec, l in zip(self.raid_attack_vectors, attack_labels):
                if label == l:
                    total_err += np.linalg.norm(attack_fitter.cluster_centers_[l] - vec) ** 2
            class_avg_error = total_err / counts[label][1]
            concentration.append(class_avg_error)
        # vis used to confirm vectors
        # for i in all_labels:
        #     plt.scatter(self.raid_attack_vectors[attack_labels == i, 0], self.raid_attack_vectors[attack_labels == i, 1], label = i)
        # plt.scatter(attack_centroids[:,0] , attack_centroids[:,1] , s = 80, color = 'k')
        # plt.legend()  
        # plt.show()
        return attack_fitter.cluster_centers_[np.argmin(concentration)]

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