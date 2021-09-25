from raid import Boss, Raid, SimulationPlate
import numpy as np

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
    new_boss_vec = fight_set.KNN()
    print(new_boss_vec)