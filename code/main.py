from typing import Counter
from raid import Boss, Raid, SimulationPlate
import numpy as np
import matplotlib.pyplot as plt
from util import Counter

if __name__ == "__main__":
    # boss vectors
    no_fit_count = Counter("Boss has done no fitting")
    defense_fit = Counter("Boss has fitted its defense")
    defense_attack = Counter("Boss has fitted its attack and defense")
    n_sphere = Counter("Boss has fitted defense and attack using n-sphere sampling")
    for i in range(10):
        boss_attack_vector = np.random.rand(1,8)
        boss_defense_vector = np.random.rand(1,8)
        sire_denathrius = Boss(boss_health=10**5, boss_attack=boss_attack_vector, boss_defense=boss_defense_vector)

        meta_vectors_attack = []
        meta_vectors_defense = []
        for _ in range(100):
            a = np.random.rand(1,8)
            a[0,2] += 10 # creates a bias in the vector hence a "meta"
            a[0,0] += 5
            meta_vectors_attack.append(a)
            d = np.random.rand(1,8)
            d[0,1] += 10
            d[0,2] += 5
            meta_vectors_defense.append(d)
        meta_raids = [Raid(raid_health=10**5, raid_attack=attack, raid_defense=defense) for attack, defense in zip(meta_vectors_attack, meta_vectors_defense)]
        
        non_meta_attack_vectors = [np.random.rand(1,8) for _ in range(100)]
        non_meta_defense_vectors = [np.random.rand(1,8) for _ in range(100)]
        non_meta_raids = [Raid(raid_health=10**5, raid_attack=attack, raid_defense=defense) for attack, defense in zip(non_meta_attack_vectors, non_meta_defense_vectors)]
        all_raids = meta_raids + non_meta_raids
        # print("------------------------")
        fight_set = SimulationPlate(all_raids, sire_denathrius)
        no_fit_count.add(fight_set.fight())
        # print("Fight #1. Defense fitted, No attack fitting")
        sire_denathrius.boss_defense = fight_set.KNN_defense()
        defense_fit.add(fight_set.fight())
        # print("Fight #2. Attack vector fitting")
        sire_denathrius.boss_attack, attack_model = fight_set.KNN_attack()
        defense_attack.add(fight_set.fight())
        # print("Fight #3. Attack vector sampled from n-sphere")
        sire_denathrius.boss_attack = np.abs(fight_set.n_sphere_sample(sire_denathrius.boss_attack, attack_model))
        n_sphere.add(fight_set.fight())
    
    print(no_fit_count)
    print(defense_fit)
    print(defense_attack)
    print(n_sphere)
