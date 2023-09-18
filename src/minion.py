class Minion:
    def __init__(self, card, player):
        self.card = card
        self.name = card.name
        self.cost = card.cost
        self.type = card.type
        self.attack = card.attack
        self.health = card.health
        self.attackable = False
        self.master = player
        self.fieldindex = None      #같은 minion이 한 field에 동시에 있을 수 있기 때문에 dead발생시 스스로 index를 갖고 있어야한다.


    def minioninfo(self):
        if(self.attackable):
            return self.name + " [" + str(self.attack) + "/" + str(self.health) + "] | attackable"
        else:
            return self.name + " [" + str(self.attack) + "/" + str(self.health) + "] | nonattackable"
