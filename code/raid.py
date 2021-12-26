import numpy as np
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
        '''Normalize boss attack dimension and multiply it by the dps of the boss'''
        a = attack / np.sum(attack)
        return a * self.dps

    def set_boss_defense(self, defense):
        d = defense / np.sum(defense)
        return d * self.armour


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
        Boss fights all raids combat is turn based. To see who wins we compare how many turns the opponents take to kill each other.
        If the raid kills the boss in 10 turns and the boss kills the raid in 15 turns then that is considered a win for the boss
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
            allraid_lifespan.append(len(raid_health_tape))
            bosshp = self.boss.health
            # Raid attacks
            while bosshp > 0:
                total_damage = self.boss.boss_defense - raid.raid_attack
                total_damage = np.sum(total_damage, where=total_damage<0)
                if total_damage < 0:
                    boss_health_tape.append(total_damage)
                    bosshp += total_damage
            boss_lifespan.append(len(boss_health_tape))
        boss_score = 0
        raid_score = 0
        for boss_tally, raid_tally in zip(boss_lifespan, allraid_lifespan):
            if boss_tally >= raid_tally:
                boss_score += 1
            else:
                raid_score += 1
        return boss_score, raid_score

    
    def KNN_defense(self):
        '''
        Fit defense vector the the community of raiders
        '''
        defense_fitter = KMeans(n_clusters=8, random_state=0, algorithm="elkan")
        all_attack_vecs = [raid.raid_attack for raid in self.list_of_raids]
        all_attack_vecs = np.squeeze(np.stack(all_attack_vecs, axis=0))
        attack_labels = defense_fitter.fit_predict(all_attack_vecs)
        (u, c) = np.unique(attack_labels, return_counts=True)
        counts = np.asarray((u,c)).T
        concentration = []
        for label in np.unique(attack_labels):
            total_err = 0
            for vec, l in zip(all_attack_vecs, attack_labels):
                if label == l:
                    total_err += np.linalg.norm(defense_fitter.cluster_centers_[l] - vec) ** 2
            class_avg_error = total_err / counts[label][1]
            concentration.append(class_avg_error)
        return defense_fitter.cluster_centers_[np.argmin(concentration)]
    
    def KNN_attack(self):
        '''
        Fit attack vector the the community of raiders
        '''
        attack_fitter = KMeans(n_clusters=8, random_state=0, algorithm="elkan")
        all_defense_vecs = [raid.raid_defense for raid in self.list_of_raids]
        all_defense_vecs = np.squeeze(np.stack(all_defense_vecs, axis=0))
        defense_labels = attack_fitter.fit_predict(all_defense_vecs)
        (u, c) = np.unique(defense_labels, return_counts=True)
        counts = np.asarray((u,c)).T
        concentration = []
        for label in np.unique(defense_labels):
            total_err = 0
            for vec, l in zip(all_defense_vecs, defense_labels):
                if label == l:
                    total_err += np.linalg.norm(attack_fitter.cluster_centers_[l] - vec) ** 2
            class_avg_error = total_err / counts[label][1]
            concentration.append(class_avg_error)

        return attack_fitter.cluster_centers_[np.argmin(concentration)], attack_fitter

    def n_sphere_sample(self, sphere_center, model):
        '''
        Fitted attack vectors seem to be too "meta specific" so we will use the attack vector and then radomly sample from the sphere of radius
        to find a somewhat random attack vector.
        '''
        radius = [np.linalg.norm(center - sphere_center) for center in model.cluster_centers_] # the second smallest radius
        radius.sort()
        radius = radius[2]
        rr = np.random.uniform(0, radius)
        thetas = np.random.randint(181, size=(1, model.cluster_centers_.shape[1] - 1))
        sphere_mat = np.zeros((thetas.shape[1],thetas.shape[1]))
        for i in range(sphere_mat.shape[0]):
            for j in range(sphere_mat.shape[1]):
                if j <= i:
                    sphere_mat[i,j] = thetas[0,j]

        sphere_diag = np.cos(sphere_mat.diagonal())
        sphere_lower = np.sin(np.tril(sphere_mat, k=-1))
        sphere_mat = np.triu(np.ones((sphere_diag.shape[0],sphere_diag.shape[0])),k=1) + sphere_lower + np.diag(np.full(sphere_diag.shape[0], sphere_diag))
        sphere_x = rr * np.cumprod(sphere_mat, axis=1)[:,sphere_diag.shape[0]-1]
        last_val = rr * np.cumprod(np.sin(thetas), axis=1)[0][sphere_x.shape[0]-1]
        sphere_x = np.append(sphere_x , last_val)
        return sphere_x + sphere_center

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