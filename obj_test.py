from raid import Raid
import numpy as np


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
# meta_raids = [Raid(raid_health=10**6, raid_attack=attack, raid_defense=defense) for attack, defense in zip(meta_vectors_attack, meta_vectors_defense)]

non_meta_attack_vectors = [np.random.rand(1,3) for _ in range(120)]
non_meta_defense_vectors = [np.random.rand(1,3) for _ in range(120)]
# non_meta_raids = [Raid(raid_health=10**6, raid_attack=attack, raid_defense=defense) for attack, defense in zip(non_meta_attack_vectors, non_meta_defense_vectors)]
# all_raids = meta_raids + non_meta_raids
attack = non_meta_attack_vectors[0]
defense = non_meta_defense_vectors[0]
print(attack)
print(type(attack))
print(defense)
print(type(defense))
r1 = Raid(raid_health=10**6, raid_attack=attack, raid_defense=defense)
print("a", r1.raid_attack)
print("d", r1.raid_defense)
