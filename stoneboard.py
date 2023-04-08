import copy
import random
import card

import minion

class Board:
    def __init__(self, player1, player2, mode, viewmode):
        self.mode = mode
        self.viewmode = viewmode

        self.p1 = copy.deepcopy(player1)
        self.p2 = copy.deepcopy(player2)

        self.p1.opponent = self.p2
        self.p2.opponent = self.p1

        self.p1.order = 1
        self.p2.order = 2

        self.turn_num = 0
        self.action_num = 0                     # nextturn을 고르는 것도 action에 포함, 즉 이 게임에서는 action_num가 전체 turn의 역할을 한다.(game length)
        self.turn_color = False

        self.inDEFAULTPOLICY = False

    def info(self):#UI
        print()
        print()        
        if(self.turn_color):
            print("<<<<<", self.p1.name, ">>>>>")
        else:
            print("<<<<<", self.p2.name, ">>>>>")
        print("Turn :", self.turn_num)
        print("Action :", self.action_num)

        self.drawinfo(self.p2.drawlist, self.p2)
        print(self.p2.name, "Healht =", self.p2.health, "| Mana =", self.p2.mana, "| Weapon =", self.p2.weapon)
        print(self.p2.name, "Minion ↓ ")
        self.fieldinfo(self.p2.fieldlist, self.p2)
        print("####################################################################################################")
        self.fieldinfo(self.p1.fieldlist, self.p1)
        print(self.p1.name, "Minion ↑ ")
        print(self.p1.name, "Healht =", self.p1.health, "| Mana =", self.p1.mana, "| Weapon =", self.p1.weapon)
        self.drawinfo(self.p1.drawlist, self.p1)

    def drawinfo(self, drawlist, player):#drawcard UI
        print("--------------------------------------------------")
        print(player.name, "Drawlist")
        for i in range(len(drawlist)):
            print(str(i) + ". " + drawlist[i].cardinfo())
        print("--------------------------------------------------")

    def fieldinfo(self, fieldlist, player):
        print("--------------------------------------------------")
        print(player.name, "Fieldlist")
        for i in range(len(fieldlist)):
            print(str(i) + ". " + fieldlist[i].minioninfo())
        print("--------------------------------------------------")   

    def start(self):
        if(self.p1.shuffle):
            random.shuffle(self.p1.decklist)
        if(self.p2.shuffle):
            random.shuffle(self.p2.decklist)
        self.mulligan(self.p1, 3)
        self.mulligan(self.p2, 4)

        if(self.mode==2):               # the coin 추가 모드
            self.p2.drawlist.append(card.GAME_005)

        self.turn_num = self.turn_num + 1
        self.turn_color = not self.turn_color

    def mulligan(self, player, index):
        for i in range(index):
            player.drawlist.append(player.decklist[0])
            player.decklist.remove(player.decklist[0])

    def resource(self, player):                                 #마나, 카드뽑기, 미니언 공격가능여부=True
        if(len(player.decklist)!=0):                            #decklist가 0이 아니라면 draw
            if(len(player.drawlist)==10):                       #drawlist=10이면 카드는 타게된다.
                drawcard = player.decklist[0]
                player.decklist.remove(drawcard)
            else:
                drawcard = player.decklist[0]
                player.drawlist.append(drawcard)
                player.decklist.remove(drawcard)
        else:                                                   #decklist가 0이라면 damage
            player.health = player.health - player.drawdamage
            player.drawdamage = player.drawdamage + 1

        if(player.maxmana!=10):                                 #최대 마나 증가 및 마나 초기화
            player.maxmana = player.maxmana +1
        player.mana = player.maxmana

        for minion in player.fieldlist:                         #미니언 공격가능여부=True
            minion.attackable = True

    def infodoaction(self, player, action):
        self.action_num = self.action_num + 1   # nextturn을 고르는 것도 action에 포함
        # print("infodoaction",action)                           # printaction이 잘 작동하는지 확인용
        if(player.opponent.type == "Human" or self.viewmode):
            self.printaction(player, action)
        
        if(player.opponent.type == "Human" or player.type == "Human"):
            print("If you want to next, press enter key")
            key = input()
        self.doaction(player, action)

        # 이 때 getaction으로 각 player가 진행할 action을 정해오면 action함수에서는 그 것을 시행하는 역할을 할 것이다.
        # 그렇다면 action은 크게 3가지인데, 턴을 종료하거나, 카드를 내거나, 미니언을 이용하여 공격을 하는 것이다.
        # 1st action = turn end         [-1]
        # 2nd action = draw card        [0, cardindex]
        # 3rd action = attack target    [1, minionindex, targetindex]   # hero's targetindex = -1
 
    def doaction(self, player, action):
        if(action[0]==-1):                                                                  #turn end, nextturn, resource
            self.nextturn()
            self.resource(player.opponent)
        elif(action[0]==0):                                                                 #play card
            cardindex = action[1]                   
            # print("cardindex =", cardindex)         #주석
            # print("drawlist = ", player.drawlist)   #주석
            if(player.drawlist[cardindex].type == "Minion"):                                #사용하려는 카드가 Minion인 경우
                self.playcardminion(player, player.drawlist[cardindex])
            elif(player.drawlist[cardindex].type == "Spell"):                               #사용하려는 카드가 Spell인 경우
                self.playcardspell(player, player.drawlist[cardindex])
            elif(player.drawlist[cardindex].type == "Weapon"):                              #사용하려는 카드가 Weapon인 경우
                pass
            player.mana = player.mana - player.drawlist[cardindex].cost                     #사용한 마나 삭제
            del player.drawlist[cardindex]                                                  #사용한 카드 삭제 
        elif(action[0]==1):                                                                 #attack target
            attackerindex = action[1]
            attacker = player.fieldlist[attackerindex]

            targetindex = action[2]
            if(targetindex==-1):        #hero를 공격
                player.opponent.health = player.opponent.health - attacker.attack
                attacker.attackable = False
            else:                       #minion을 공격
                target = player.opponent.fieldlist[targetindex]
                attacker.attackable = False                                                 #m1의 공격가능여부=false
                self.combatminiontominion(attacker, target)                                 #minion1과 minion2의 전투

                #사후처리. 죽은애들때문에 fieldindex가 당겨졌을테니 fieldindex를 update해주어야한다.
                for i in range(len(attacker.master.fieldlist)):
                    attacker.master.fieldlist[i].fieldindex = i
                for i in range(len(target.master.fieldlist)):
                    target.master.fieldlist[i].fieldindex = i

    def printaction(self, player, action):
        if(action[0]==-1):
            print(player.name, "action =", "turn end")
        elif(action[0]==0):
            print(player.name, "action =", "draw", player.drawlist[action[1]].name)
        elif(action[0]==1):
            # print("attackerlist =", player.fieldlist)
            # print("targetminionlist =", player.opponent.fieldlist)

            if(action[2]==-1):#attack to hero
                print(player.name, "action =", "attack", player.fieldlist[action[1]].name, "to hero")
            else:
                print(player.name, "action =", "attack", player.fieldlist[action[1]].name, "to", player.opponent.fieldlist[action[2]].name)


    def getlegalaction(self, player):
        legalactionlist = []
        # 1. draw가능한 cardindex 구하기
        for cardindex in range(len(player.drawlist)):                       # drawlist의 개수
            if(player.drawlist[cardindex].cost <= player.mana):             # draw 가능한 card
                legalactionlist.append([0, cardindex])                      # [0, index]를 추가
        for minionindex in range(len(player.fieldlist)):                    # fieldlist의 개수
            if(player.fieldlist[minionindex].attackable):                   # attackable minion
                #not exist taunt
                legalactionlist.append([1, minionindex, -1])                # [1, minionindex, -1]을 추가 = attack hero
                for targetindex in range(len(player.opponent.fieldlist)):
                    legalactionlist.append([1, minionindex, targetindex])   # [1, minionindex, targetindex]을 추가
        legalactionlist.append([-1])                                        # [-1]을 추가 = turn end
        return legalactionlist

    def clear(self, player):
        # 각 minion의 index update?
        pass

    def nextturn(self):
        if(self.inDEFAULTPOLICY):       #MCTS iter 내부면 실행X
            pass
        else:
            if(self.turn_color):
                if(self.p1.type == "MCTS"):
                    self.checkattackable(self.p1)
            else:
                if(self.p2.type == "MCTS"):
                    self.checkattackable(self.p2)


        self.turn_num = self.turn_num + 1
        self.turn_color = not self.turn_color

    def end(self):
        if(self.p1.health<=0):      #2가 승리
            return 2
        elif(self.p2.health<=0):    #1이 승리
            return 1

    def playcardminion(self, player, card):
        player.fieldlist.append(minion.Minion(card, player))
        index = len(player.fieldlist)-1
        player.fieldlist[len(player.fieldlist)-1].fieldindex = len(player.fieldlist)-1      #minion의 field index 저장 ==>minion의 dead발생시 update해주어야한다.

        if(player.fieldlist[index].card.text!=None):                            # text가 None이 아니고
            if("Charge" in player.fieldlist[index].card.text):                  # text안에 charge가 있으면
                player.fieldlist[len(player.fieldlist)-1].attackable = True     # Charge True

    def playcardspell(self, player, card):                                      # 일단 동전한닢만 구현
        player.mana = player.mana + 1

    def combatminiontominion(self, minion1, minion2):
        dead1 = False
        dead2 = False
        if(minion1.health <= minion2.attack):   #2의 공격을 맞아 1이 사망
            dead1 = True                   #1이 사망
        else:
            minion1.health = minion1.health - minion2.attack
            
        if(minion2.health <= minion1.attack):   #1의 공격을 맞아 2이 사망
            dead2 = True                   #2이 사망
        else:
            minion2.health = minion2.health - minion1.attack

        if(dead1 and dead2):                    #minion1,2 사망     #죽음의메아리 발동
            del minion1.master.fieldlist[minion1.fieldindex]
            del minion2.master.fieldlist[minion2.fieldindex]
        elif(dead1 and not dead2):              #minion1 사망       #죽음의메아리 발동
            del minion1.master.fieldlist[minion1.fieldindex]
        elif(not dead1 and dead2):              #minion2 사망       #죽음의메아리 발동
            del minion2.master.fieldlist[minion2.fieldindex]
        elif(not dead1 and not dead2):
            pass

    def checkattackable(self, player):      # nextturn()에서 실행
        if(len(player.fieldlist)!=0):       # field에 minion이 있다면
            isattackable = False
            for i in player.fieldlist:
                if(i.attackable):           # attaackable
                    isattackable = True
                    break  
                else:
                    pass
                    
            if(isattackable):
                player.attackable_turnend = player.attackable_turnend + 1
                # print("attackable_turnend =", player.attackable_turnend)
                # self.info()
            else:
                player.nonattackable_turnend = player.nonattackable_turnend + 1
                # print("nonattackable_turnend =", player.nonattackable_turnend)
            

# Yena = player.Player("Yena", "Mage", card.Classic_Neutral, True)
# Yuri = player.Player("Yuri", "Mage", card.Classic_Neutral, True)

# b = board(Yena, Yuri)
# b.start()
# b.info()
