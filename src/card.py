class Card:
    def __init__(self, name, cost, text):
        self.name = name
        self.cost = cost
        self.type = None
        self.text = text
        self.legendary = False
    
    def legendarible(self):
        self.legendary = True
    

class CardMinion(Card):
    def __init__(self, name, cost, attack, health, text):
        super().__init__(name, cost, text)
        self.type = "Minion"
        self.attack = attack
        self.health = health

    def cardinfo(self):
        if(self.text!=None):
            string = str(self.cost) + " cost " + self.type + " | " +  self.name + " [" + str(self.attack) + "/" + str(self.health) + "] " + "| " + self.text
        else:
            string = str(self.cost) + " cost " + self.type + " | " +  self.name + " [" + str(self.attack) + "/" + str(self.health) + "] " + "| "
        return string




class CardSpell(Card):
    def __init__(self, name, cost, target, text):
        super().__init__(name, cost, text)
        self.type = "Spell"
        self.target = target

    def cardinfo(self):
        if(self.text!=None):
            string = str(self.cost) + " cost " + self.type + " | " +  self.name + " | " + self.text
        else:
            string = str(self.cost) + " cost " + self.type + " | " +  self.name + " | "
        return string
    
    def operate(self, player):
        if(self.target):
            print("Choose target")
            #get target
            #operatespelltarget(target)
        else:
            operatespell()
    def operatespell():
        #각 spell마다 다르게 구현
        print()



class CardWeapon(Card):
    def __init__(self, name, cost, attack, durability, text):
        super().__init__(name, cost, text)
        self.type = "Weapon"
        self.attack = attack
        self.durability = durability
    def cardinfo(self):
        print(self.cost, "cost", self.type, "|",  self.name, "[", self.attack, self.durability, "]", "|", self.text)


GAME_005 = CardSpell("The Coin", 0, None, "Gain 1 Mana Crystal this turn only.")


CS2_118 = CardMinion("Magma Rager", 3, 5, 1, None)
CS2_119 = CardMinion("Oasis Snapjaw", 4, 2, 7, None)
CS2_120 = CardMinion("River Crocolisk", 2, 2, 3, None)
CS2_124 = CardMinion("Wolfrider", 3, 3, 1, "Charge")
CS2_131 = CardMinion("Stormwind Knight", 4, 2, 5, "Charge")
CS2_168 = CardMinion("Stonetusk Boar", 1, 1, 1, "Charge")
CS2_171 = CardMinion("Murloc Raider", 1, 2, 1, None)
CS2_172 = CardMinion("Bloodfen Raptor", 2, 3, 2, None)
CS2_173 = CardMinion("Bluegill Warrior", 2, 2, 1, "Charge")
CS2_182 = CardMinion("Chillwind Yeti", 4, 4, 5, None)
CS2_186 = CardMinion("War Golem", 7, 7, 7, None)
CS2_200 = CardMinion("Boulderfist Ogre", 6, 6, 7, None)
CS2_201 = CardMinion("Core Hound", 7, 9, 5, None)
CS2_213 = CardMinion("Reckless Rocketeer", 6, 5, 2, "Charge")
CS2_231 = CardMinion("Wisp", 0, 1, 1, None)

EX1_007 = CardMinion("Acolyte of Pain", 3, 1, 3, "Whenever this minion takes damage, draw a card.")
EX1_012 = CardMinion("Bloodmage Thalnos", 2, 1, 1, "Spell Damage +1 Deathrattle: Draw a card.")
EX1_012.legendarible()
EX1_015 = CardMinion("Novice Engineer", 2, 1, 1, "Battlecry: Draw a card.")
EX1_096 = CardMinion("Loot Hoarder", 2, 2, 1, "Deathrattle: Draw a card.")
EX1_561 = CardMinion("Alexstrasza", 9, 8, 8, "Battlecry: Set a hero's remaining Health to 15.")
EX1_561.legendarible()
EX1_559 = CardMinion("Archmage Antonidas", 7, 5, 7, "Whenever you cast a spell, add a 'Fireball' spell to your hand.")
EX1_559.legendarible()
NEW1_021 = CardMinion("Doomsayer", 2, 0, 7, "At the start of your turn, destroy ALL minions.")

CS2_023 = CardSpell("Arcane Intellect", 3, False, "Draw 2 cards.")
CS2_024 = CardSpell("Frostbolt", 2, False, "Deal 3 damage to a character and Freeze it.")
CS2_026 = CardSpell("Frost Nova", 3, False, "Freeze all enemy minions.")
CS2_027 = CardSpell("Mirror Image", 1, False, "Summon two 0/2 minions with Taunt.")
CS2_028 = CardSpell("Blizzard", 6, False, "Deal 2 damage to all enemy minions and Freeze them.")
CS2_029 = CardSpell("Fireball", 4, True, "Deal 6 damage.")
CS2_031 = CardSpell("Ice Lance", 1, True, "Freeze a character. If it was already Frozen, deal 4 damage instead.")
CS2_032 = CardSpell("Flamestrike", 7, False, "Deal 5 damage to all enemy minions.")
EX1_279 = CardSpell("Pyroblast", 10, True, "Deal 10 damage.")
EX1_289 = CardSpell("Ice Barrier", 3, False, "Secret: When your hero is attacked, gain 8 Armor.")
EX1_295 = CardSpell("Ice Block", 3, False, "Secret: When your hero takes fatal damage, prevent it and become Immune this turn.")



EX1_536 = CardWeapon("Eaglehorn Bow", 3, 3, 2, "Whenever a friendly Secret is revealed, gain +1 Durability.")



#Deck
Classic_Freeze_Mage = [CS2_031, CS2_031, CS2_027, CS2_027, EX1_012, NEW1_021, NEW1_021, CS2_024, CS2_024, EX1_096, EX1_096, EX1_015, EX1_007, EX1_007, CS2_023, CS2_023, CS2_026, CS2_026, EX1_289, EX1_289, EX1_295, EX1_295, CS2_029, CS2_029, CS2_028, CS2_028, EX1_559, CS2_032, EX1_561, EX1_279]
A = [CS2_118, CS2_119, CS2_120, CS2_124, CS2_131, CS2_168, CS2_171, CS2_172, CS2_173, CS2_182, CS2_186, CS2_200, CS2_201, CS2_213, CS2_231]
Classic_Neutral = A + A

