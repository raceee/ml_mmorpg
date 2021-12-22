from raid import Boss, Raid, SimulationPlate
import numpy as np

if __name__ == "__main__":
    # boss vectors
    boss_attack_vector = np.random.rand(1,8)
    boss_defense_vector = np.random.rand(1,8)
    sire_denathrius = Boss(boss_health=10**4, boss_attack=boss_attack_vector, boss_defense=boss_defense_vector)

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
    meta_raids = [Raid(raid_health=10**6, raid_attack=attack, raid_defense=defense) for attack, defense in zip(meta_vectors_attack, meta_vectors_defense)]
    
    non_meta_attack_vectors = [np.random.rand(1,8) for _ in range(100)]
    non_meta_defense_vectors = [np.random.rand(1,8) for _ in range(100)]
    non_meta_raids = [Raid(raid_health=10**4, raid_attack=attack, raid_defense=defense) for attack, defense in zip(non_meta_attack_vectors, non_meta_defense_vectors)]
    all_raids = meta_raids + non_meta_raids
    fight_set = SimulationPlate(all_raids, sire_denathrius)
    fight_set.fight()
    print("Fight #1. No attack fitting")
    sire_denathrius.boss_defense = fight_set.KNN_defense()
    fight_set.fight()
    print("Fight #2. Attack vector fitting")
    sire_denathrius.boss_attack, attack_model = fight_set.KNN_attack()
    fight_set.fight()
    print("Fight #3. Attack vector sampled from n-sphere")
    sire_denathrius.boss_attack = fight_set.n_sphere_sample(sire_denathrius.boss_attack, attack_model)
    
