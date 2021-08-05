import numpy as np
import random
import math

class Boss:
    def __init__(self, bs_name, bs_health, boss_attack, armour, attack_vector, defense_vector):
        self.boss_name = bs_name
        self.boss_health = bs_health
        self.boss_attack = boss_attack
        self.boss_armour = armour
        self.initial_boss_defense_vector = attack_vector
        self.initial_boss_offense_vector = defense_vector
    
    def boss_attack(self):
        return
    
    def get_bs_health(self):
        return self.bs_health

    def bs_loose_health(self, damage):
        self.bs_health -= damage #fantastic code tripp
    
    def vector_set(self):
        return
    
    def boss_optimize(self, dataframe):
        pass


class Player:
    def __init__(self, pl_name, pl_health, pl_attack, pl_armour, attack_vector, defense_vector):
        self.player_name = pl_name
        self.player_health = pl_health
        self.player_attack = pl_attack
        self.player_armour = pl_armour
        self.initial_player_defense_vector = attack_vector
        self.initial_player_offense_vector = defense_vector
    
    def set_player_attack(self):
        l2 = math.sqrt(sum([stat**2 for stat in self.initial_player_offense_vector]))
        self.attack_vector = [power / l2 for power in self.initial_player_offense_vector]
    
    def set_player_defense(self):
        l2 = math.sqrt(sum([stat**2 for stat in self.initial_player_defense_vector]))
        self.defense_vector = [power / l2 for power in self.initial_player_defense_vector]
    
    def player_attack(self):
        return self.player_attack * self.attack_vector
    
    def player_defend(self):
        return self.player_armour * self.defense_vector
    
    def take_damage(self, damage):
        self.player_health -= damage


class Raid:
    def __init__(self, boss, players:list):
        self.boss = boss
        self.player_list = players
        self.party_size = len(players)
        self.player_party_total_health = sum([player.player_health for player in self.player_list])

    def fight(self):
        player_vector = np.add([player.player_attack() for player in self.player_list], axis=0)


    def make_fight(self):
        boss_damage_tape = []
        while self.player_party_total_health > 0:
            self.player_party_total_health -= abs(self.boss.boss_attack() - self.player.player_defend()) # block needs to be added here
            boss_damage_tape.append(self.player_party_total_health)
        player_damage_tape = []
        while self.boss.boss_health > 0:
            self.boss.boss_health -= sum([abs(player.player_attack() - self.boss.boss_armour()) for player in self.player_list]) # block needs to be added here






#     def __str__(self):
#         class_info = """
# This adventurer is a: {}
# HEALTH -----> {}
# {}/MISS -----> {} DMG / %{}
# {}/MISS -----> {} DMG / %{}
# DODGE CHANCE -----> %{}
#         """.format(self.pl_name, self.pl_health, self.pl_atk1_name, self.pl_atk1dmg, self.pl_atk1miss,
#                    self.pl_atk2_name, self.pl_atk2dmg, self.pl_atk2miss, self.pl_dodge)
#         return class_info


#     def get_atk1_name(self):
#         return self.pl_atk1_name

#     def get_atk2_name(self):
#         return self.pl_atk2_name

#     def get_pl_health(self):
#         return self.pl_health

#     def get_atk1_miss(self):
#         return self.pl_atk1miss

#     def get_atk2_miss(self):
#         return self.pl_atk2miss

#     def get_atk1_dmg(self):
#         return self.pl_atk1dmg

#     def get_atk2_dmg(self):
#         return self.pl_atk1dmg

#     def get_atk_sheet(self):
#         atk_sheet = """
# CURRENT HEALTH -----> {}
# {}/MISS -----> {} DMG / %{}
# {}/MISS -----> {} DMG / %{}
# BOSS HEALTH -----> {}
#         """.format(player.get_pl_health(), self.pl_atk1_name, self.pl_atk1dmg, self.pl_atk1miss, self.pl_atk2_name, self.pl_atk2dmg, self.pl_atk2miss, boss.get_bs_health())
#         return atk_sheet

#     def pl_lose_health(self, damage):
#         self.pl_health -= damage

#     def get_dodge_chance(self):
#         return self.pl_dodge

#     def pl_healed(self, healed):
#         self.pl_health += healed

#     def pl_get_name(self):
#         return self.pl_name



        


# def menu():

#     player = player_constructor("null", 0, 0, 0, 0, 0, 0, "null", "null") #blank to be reassigned

#     #Assigning Pre-made classes to variables
#     warrior = player_constructor("Warrior", 100, 50, 10, 100, 20, 2, "RAMPAGE", "SHIELD CRASH")
#     gunner = player_constructor("Gunner", 75, 20, 5, 30, 25, 5, "SHOOT", "ANNIHILATE")
#     ninja = player_constructor("Ninja", 65, 25, 3, 40, 13, 15, "STRIKE", "WEAK SPOT")

#     boss = Boss("JIM", 200, 15, 5, 35, 30)

#     selected = False

#     while selected == False:
#         choice = int(input("Select your class: (1)Warrior, (2)Gunner, (3)Ninja or (0)For more info "))
#         if choice == 1:
#             player = warrior
#             selected = True
#         if choice == 2:
#             player = gunner
#             selected = True
#         if choice == 3:
#             player = ninja
#             selected = True

#         if choice == 0:
#             player = warrior
#             print(player)
#             player = gunner
#             print(player)
#             player = ninja
#             print(player)

#     print()
#     print(f"You are playing as a: {player.pl_get_name()}")

#     print(f"As the {player.pl_get_name()} journeys through the dungeon, they encounter a big beast!")
#     print("Combat is initiated!")
#     print("The player goes first!")

#     turn_counter = 1
#     print(f"Turn {turn_counter}")

#     while True:
#         riposte_damage = random.randint(15,30)
#         turn_counter += 1
#         print(player.get_atk_sheet())
#         action = int(input(f"Which action do you want to take?: (1){player.get_atk1_name()} (2){player.get_atk2_name()} (3)HEAL "))
#         pl_chance = random.randint(1, 100)

#         if action == 1:
#             if pl_chance <= player.get_atk1_miss():
#                 print("Attack missed. Wait until next turn to take another action.")
#             else:
#                 print(f"You hit the boss with {player.get_atk1_name()} and deal {player.get_atk1_dmg()} DMG to the boss")
#                 boss.bs_loose_health(player.get_atk1_dmg())
#         if action == 2:
#             if pl_chance <= player.get_atk1_miss():
#                 print("Attack missed. Wait until next turn to take another action.")
#             else:
#                 print(f"You hit the boss with {player.get_atk2_name()} and deal {player.get_atk2_dmg()} DMG to the boss ")
#                 boss.bs_loose_health(player.get_atk2_dmg())
#         if action == 3:
#             heal_val = random.randint(5,20)
#             print(f"You have healed for {heal_val} HEALTH")
#             player.pl_healed(heal_val)
#             print(player.get_pl_health())

#         if boss.get_bs_health() <= 0:
#             break

#         print()
#         print("Bosses turn: ")

#         bs_choice_chance = random.randint(1,2)
#         bs_miss_chance = random.randint(1,100)

#         if bs_choice_chance == 1:
#             if bs_miss_chance <= (boss.bs_get_atk1_miss() + player.get_dodge_chance()):
#                 print("The boss misses their attack.")
#                 print(f"You riposte! You deal {riposte_damage} DMG back!")
#                 boss.bs_loose_health(riposte_damage)
#             else:
#                 print(f"The boss hits you dealing {boss.bs_get_atk1_dmg()} DMG")
#                 player.pl_lose_health(boss.bs_get_atk1_dmg())

#         if bs_choice_chance == 2:
#             if bs_miss_chance <= (boss.bs_get_atk2_miss() + player.get_dodge_chance()):
#                 print("The boss misses their attack.")
#                 print(f"You riposte! You deal {riposte_damage} DMG back!")
#                 boss.bs_loose_health(riposte_damage)
#             else:
#                 print(f"The boss hits you dealing {boss.bs_get_atk2_dmg()} DMG")
#                 player.pl_lose_health(boss.bs_get_atk2_dmg())

#             if player.get_pl_health() <= 0:
#                 print(f"Oh no! {boss.bs_get_name()} has defeated you! Try again:")
#                 quit()

#             print(f"Turn {turn_counter}")

#     print(f"Congratulations you have defeated {boss.bs_get_name()}!")




