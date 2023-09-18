import copy
import random
import math
import numpy as np

from yenanode import UCTNODE 

class Player:
    def __init__(self, name, hero, decklist):
        self.name = name
        self.type = None
        self.health = 30
        self.mana = 0
        self.maxmana = 0
        self.weapon = None
        self.opponent = None
        self.drawdamage = 1

        self.hero = hero
        self.drawlist = []
        self.decklist = copy.deepcopy(decklist) 
        self.fieldlist = []
        self.order = None

        self.attackable_turnend = 0         # attackable minion 있는 상태에서 turn end
        self.nonattackable_turnend = 0      # attackable minion 없는 상태에서 turn end

        self.shuffle = True

class Humanplayer(Player):
    def __init__(self, name, hero, decklist):
        super().__init__(name, hero, decklist)
        self.type = "Human"
    
    def getaction(self, b, player, legalactionlist):
        # 원래 만들었던 것처럼 자유로운 선택을 할지, 보기를 주고 고르도록할지 고민중이다. 전자가 좀 더 재미있을 듯
        print("Your legal action = ",legalactionlist)
        print("Choose your action index. < turn end > = -1, < playcard > = 0, < attack > = 1")
        while(True):                                # action 정하기
            index = input()
            if(index in ["-1", "0", "1"]):
                break
            else:                                   # while cycle
                print("You can't do that action. Choose your action index. turn end = -1, playcard = 0, attack = 1")

        if(index == "-1"):
            print("Your choice is < turn end >.")
            return [-1]

        elif(index == "0"):
            print("Your choice is < play card >.")
            cardactionlist = []                     # action[0]==0인 것들
            cardindexlist = []                      # action[0]==0인 것들의 action[1]을 모아둔 list
            for cardaction in legalactionlist:      # legalactionlist 중 원소[0]이 0인 것을 cardactionlist에 추가
                if(cardaction[0]==0):
                    cardactionlist.append(cardaction)
                    cardindexlist.append(str(cardaction[1]))        #str로 저장

            if(len(cardactionlist)!=0):             # 낼 수 있는 card가 있으면 진행 : legalactionlist의 원소[0]이 0인 것이 있으면 가능
                print("Choose your card index to play. If you want to return action choice, choose r.")

                while(True):
                    cardindex = input()
                    if(cardindex in cardindexlist): # index check
                        print("Your choice is <", player.drawlist[int(cardindex)].name, ">.")
                        return [0, int(cardindex)]
                    elif(cardindex in ["r", "R"]):  # return to getaction
                        print("Return action choice.")
                        print()
                        return self.getaction(b, player, legalactionlist)
                    else:                           # while cycle
                        print("You can't do that action. Choose your card index to play. If you want to return action choice, choose r.")
            else:                                   # 낼 수 있는 card가 없으면 낼 수 있는 card 없다고 하고 getaction 다시 실행
                print("You don't have a card to play.")
                print()
                return self.getaction(b, player, legalactionlist)
            
        elif(index == "1"):
            print("Your choice is < attack >.")
            minionindexlist = []
            attackableminionlist = []
            for minion in player.fieldlist:
                minionindexlist.append(str(minion.fieldindex))  #field에 존재하는 minionlist(str로 저장)

                if(minion.attackable):
                    attackableminionlist.append(minion)         # attackable까지 만족하는 list
            
            if(len(attackableminionlist)!=0):                 # minion이 있으면 진행
                print("Choose your minion index. If you want to return action choice, choose r.")
                while(True):
                    minionindex = input()
                    if(minionindex in minionindexlist): # minionindex check
                        print("Your choice is <", player.fieldlist[int(minionindex)].name, ">.")
                        if(player.fieldlist[int(minionindex)].attackable):
                            break
                        else:
                            print("Your choice minion can't attack. Choose your minion index. If you want to return action choice, choose r.")
                    elif(minionindex in ["r", "R"]):    # return to getaction
                        print("Return action choice.")
                        print()
                        return self.getaction(b, player, legalactionlist)
                    else:
                        print("You can't do that action. Choose your minion index. If you want to return action choice, choose r.")
                
                # minion 결정 후 target 결정 시작
                print("Choose your target index. opposite hero = -1." )
                targetindexlist = ["-1"]
                for target in player.opponent.fieldlist:
                    targetindexlist.append(str(target.fieldindex))         # opponent field에 존재하는 minionindexlist(str로저장)
                while(True):
                    targetindex = input()
                    if(targetindex in targetindexlist): # targetindex check
                        if(targetindex == "-1"):        # attack hero
                            print("Your target is <", player.opponent.name, ">")
                            return [1, int(minionindex), -1]
                        else:                           # attack minion
                            print("Your target is <", player.opponent.fieldlist[int(targetindex)].name, ">")
                            return [1, int(minionindex), int(targetindex)]
                    elif(targetindex in ["r", "R"]):    # return to getaction
                        print("Return action choice.")
                        print()
                        return self.getaction(b, player, legalactionlist)
                    else:                               # wrong target
                        print("You can't attack that. Choose your target index. opposite hero = -1. If you want to return action choice, choose r.")


            else:
                print("You don't have a minion to attack.")
                print()
                return self.getaction(b, player, legalactionlist)

class Randomplayer(Player):
    def __init__(self, name, hero, decklist):
        super().__init__(name, hero, decklist)
        self.type = "Random"
    
    def getaction(self, b, player, legalactionlist):
        return random.choice(legalactionlist)

class MCTSplayer_new(Player):
    def __init__(self, name, hero, decklist, num_iter, Cp):
        super().__init__(name, hero, decklist)
        self.type = "MCTS"
        self.num_iter = num_iter
        self.Cp = 2.0/math.sqrt(2.0)    #original 2.0/math.sqrt(2.0)
        self.Cp = Cp
    
    def getaction(self, b, player, legalactionlist):
        if(len(legalactionlist)==1):            #action이 turn end밖에 없으면 바로 turn end 실행
            return legalactionlist[0]
        else:
            return self.UCTSEARCH(b)

    def UCTSEARCH(self, b):
        if(self.opponent.type == "Human"):
            print()
            print()
            print(self.name, "is thinking", "----------------------------------------------------------------------------------------------------")

        root = UCTNODE(b, None, None)                           #preaction = None, parent = None
        for i in range(self.num_iter): 
            v_last = self.TREEPOLICY(root)                      #iter defaultpolicy 진행할 node 정하기
            reward = self.DEFAULTPOLICY(v_last.b)               #iter defailtpolicy 진행
            # reward = random.randint(1, 2)
            self.BACKUP(v_last,reward)                          #iter backpropagation 진행

        
        if(self.opponent.type == "Human"):
            print(self.name, "come up with something", "----------------------------------------------------------------------------------------------------")
        # print("root child node =", root.children)
        # root.print_tree()
        return self.BESTCHILD(root,0).action                  #승률만 따져서 bestchild선택하고 action return



    def TREEPOLICY(self,v):
        while(v.is_terminal==False):
            if(v.is_expanded==False):
                return self.EXPAND(v)
            else:
                v=self.BESTCHILD(v,self.Cp)
        return v

    def EXPAND(self, v):                            #add_child할 때마다 action 1회 수행
        # print("Hello")
        action = random.choice(v.untried_action())
        return v.add_child(action)

    def BESTCHILD(self,v,coef):
        value_list=[]
        for i in range(len(v.children)):
            value = v.children[i].Q/v.children[i].N + coef*math.sqrt(2*math.log(v.N)/v.children[i].N)
            value_list.append(value)
        return v.children[np.argmax(value_list)]

    def DEFAULTPOLICY(self, c):
        b = copy.deepcopy(c)
        b.inDEFAULTPOLICY = True
        # print("Yena is thinking################################")
        while(True):
            if(b.turn_color):                                      #turn_color=True, p1.order=True, black 차례(선공차례)
                legalactionlist = b.getlegalaction(b.p1)
                action = random.choice(legalactionlist)
                b.doaction(b.p1, action)
                if(b.p1.health>0 and b.p2.health>0):      #doaciton 사망시 check
                    pass
                else:
                    break  
            else:                                                       #turn_color=False, p2.order=False, white 차례(선공차례)
                legalactionlist = b.getlegalaction(b.p2)
                action = random.choice(legalactionlist)
                b.doaction(b.p2, action)
                if(b.p1.health>0 and b.p2.health>0):      #doaciton 사망시 check
                    pass
                else:
                    break
        # print("Yena is endnding################################")
        return b.end()


    def BACKUP(self, v, reward):
        # reward, p1.order, MCTS player의 order
        # reward = player.order = 1
        if(reward==self.order): #player 승리
            while(v!=None):
                v.N = v.N + 1
                v.Q = v.Q + 1
                v = v.parent
        else:                   #2player 패배
            while(v!=None):
                v.N = v.N + 1
                v.Q = v.Q - 1
                v = v.parent




# Yena = MCTSplayer("Yena", "Mage", card.Classic_Neutral, 10)
# Yuri = Randomplayer("Yuri", "Mage", card.Classic_Neutral)
# stoneboard.Board
# b = stoneboard.Board(Yena, Yuri)
# # Yena.UCTSEARCH(b)