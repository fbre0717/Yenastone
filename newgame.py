import random
import math

import player
import card
import stoneboard

class game:
    def __init__(self,p1,p2, mode, viewmode):
        self.mode = mode
        self.viewmode = viewmode
        self.b = stoneboard.Board(p1, p2, self.mode, self.viewmode)
        
            
    def play3(self):
        self.b.start()
        if(self.b.turn_color):                                          #turn_color=True, p1.order=True, black 차례(선공차례)
            self.b.resource(self.b.p1)                                  #draw 사망시 check
        else:                                                           #turn_color=False, p2.order=False, white 차례(선공차례)
            self.b.resource(self.b.p2) 
        while(True):
            if(self.b.turn_color):                                      #turn_color=True, p1.order=True, black 차례(선공차례)
                if(self.b.p1.type == "Human" or self.b.p2.type == "Human" or self.viewmode):     # Human이 있다면 b.info() 실행
                    self.b.info()
                legalactionlist = self.b.getlegalaction(self.b.p1)
                action = self.b.p1.getaction(self.b, self.b.p1, legalactionlist)
                self.b.infodoaction(self.b.p1, action)                  #info->printaction->doaction
                if(self.b.p1.health>0 and self.b.p2.health>0):          #doaciton 사망시 check
                    pass
                else:
                    break  
            else:                                                       #turn_color=False, p2.order=False, white 차례(선공차례)
                if(self.b.p1.type == "Human" or self.b.p2.type == "Human" or self.viewmode):     # Human이 있다면 b.info() 실행
                    self.b.info()
                legalactionlist = self.b.getlegalaction(self.b.p2)
                action = self.b.p2.getaction(self.b, self.b.p2, legalactionlist)
                self.b.infodoaction(self.b.p2, action)
                if(self.b.p1.health>0 and self.b.p2.health>0):          #doaciton 사망시 check
                    pass
                else:
                    break
        return self.b.end()

    def testend(self):
        if(self.b.p1.health>0 and self.b.p2.health>0):
            pass
        else:
            return self.b.end()


class match:
    def __init__(self, p1, p2, n, mode, viewmode): 
        self.p1 = p1 
        self.p2 = p2 
        self.n = n 
        self.p1_win = 0
        self.p2_win = 0
        self.mode = mode      
        self.viewmode = viewmode
        self.totalaction = 0
        self.totalturn = 0
        self.p1total_attackable_turnend = 0
        self.p2total_attackable_turnend = 0
        self.p1total_nonattackable_turnend = 0
        self.p2total_nonattackable_turnend = 0

    def run(self):

        for i in range(self.n): 
            print() 
            print("Game ID = ",i+1)
            # first assign 
            if(self.mode == 0):         #0 순서 random change
                if(random.choice([True,False])):
                    g = game(self.p1, self.p2, self.mode, self.viewmode)               
                    print("first=",self.p1.name, " second=",self.p2.name)
                    result = g.play3()
                    if(result==1):
                        self.p1_win+=1
                        print("Winner =",self.p1.name, "last turn =", g.b.turn_num, "last action num =", g.b.action_num)
                    elif(result==2):
                        self.p2_win+=1
                        print("Winner =",self.p2.name, "last turn =", g.b.turn_num, "last action num =", g.b.action_num)

                    self.p1total_attackable_turnend = self.p1total_attackable_turnend + g.b.p1.attackable_turnend
                    self.p2total_attackable_turnend = self.p2total_attackable_turnend + g.b.p2.attackable_turnend
                    self.p1total_nonattackable_turnend = self.p1total_nonattackable_turnend + g.b.p1.nonattackable_turnend
                    self.p2total_nonattackable_turnend = self.p2total_nonattackable_turnend + g.b.p2.nonattackable_turnend

                else :
                    g = game(self.p2,self.p1, self.mode, self.viewmode)
                    print("first=",self.p2.name," second=",self.p1.name) 
                    result = g.play3()
                    if(result==1):
                        self.p2_win+=1
                        print("Winner =",self.p2.name, "last turn =", g.b.turn_num, "last action num =", g.b.action_num)
                    elif(result==2):
                        self.p1_win+=1
                        print("Winner =",self.p1.name, "last turn =", g.b.turn_num, "last action num =", g.b.action_num) 

                    self.p1total_attackable_turnend = self.p1total_attackable_turnend + g.b.p2.attackable_turnend
                    self.p2total_attackable_turnend = self.p2total_attackable_turnend + g.b.p1.attackable_turnend
                    self.p1total_nonattackable_turnend = self.p1total_nonattackable_turnend + g.b.p2.nonattackable_turnend
                    self.p2total_nonattackable_turnend = self.p2total_nonattackable_turnend + g.b.p1.nonattackable_turnend

            elif(self.mode == 1 or self.mode == 2):       #1 순서 고정
                g = game(self.p1, self.p2, self.mode, self.viewmode)               
                print("first=",self.p1.name, " second=",self.p2.name)
                result = g.play3()
                if(result==1):
                    self.p1_win+=1
                    print("Winner =",self.p1.name, "last turn =", g.b.turn_num, "last action num =", g.b.action_num)
                elif(result==2):
                    self.p2_win+=1
                    print("Winner =",self.p2.name, "last turn =", g.b.turn_num, "last action num =", g.b.action_num)

            if(g.b.p1.type == "Human" or g.b.p2.type == "Human" or self.viewmode):     # Human이 있다면 b.info() 실행
                print()
                print()
                g.b.info()

            self.totalturn = self.totalturn + g.b.turn_num
            self.totalaction = self.totalaction + g.b.action_num
        
        # total report
        print() 
        print(self.p1.name, " WIN = ", self.p1_win, " ",(self.p1_win/self.n)*100,"%")
        print(self.p2.name, " WIN = ", self.p2_win, " ",(self.p2_win/self.n)*100,"%")
        print()
        print("average turn =", self.totalturn/self.n, "average action(depth) =", self.totalaction/self.n)
        print()
        print("mode =", self.mode, "match =", self.n)
        print()
        if(self.p1.type == "MCTS"):
            print("p1 =", self.p1.name , "coef =", round(self.p1.Cp, 2), "iterator =", self.p1.num_iter, "nonattackable_turnend = ", self.p1total_nonattackable_turnend, "attackable_turnend =", self.p1total_attackable_turnend)
        if(self.p2.type == "MCTS"):
            print("p2 =", self.p2.name , "coef =", round(self.p2.Cp, 2), "iterator =", self.p2.num_iter, "nonattackable_turnend = ", self.p2total_nonattackable_turnend, "attackable_turnend =", self.p2total_attackable_turnend)


class MCTSmatch(match):
    def __init__(self, p1, p2, p1C, p1I, p2C, p2I, n, mode, viewmode):
        super().__init__(p1, p2, n, mode, viewmode)
        if(p1 == None):
            p1name = "p1_"+str(p1C)+"_"+str(p1I)
            self.p1 = player.MCTSplayer_new(p1name, "Mage", card.Classic_Neutral, p1I, p1C*math.sqrt(2.0))
        if(p2 == None):
            p2name = "p2_"+str(p2C)+"_"+str(p2I)
            self.p2 = player.MCTSplayer_new(p2name, "Mage", card.Classic_Neutral, p2I, p2C*math.sqrt(2.0))


# viewmode=True player가 human이 아니여도 모든 과정이 다 보인다

# mode
    # 0 순서 random change 
    # 1 순서 고정  
    # 2 순서 고정 및 동전한닢

# 변수 설명 m = MCTSmatch(p1, p2, p1C, p1I, p2C, p2I, n, mode, viewmode)

# Random player
Random = player.Randomplayer("Random", "Mage", card.Classic_Neutral)


if __name__ == '__main__':
    print("Do you want to play?")
    ans = input()
    if(ans in ["y", "Y", "yes", "Yes", "YES"]):
        # 직접 1판 play하고 싶은 경우
        print("Please enter your name.")
        username = input()
        user = player.Humanplayer(username, "Mage", card.Classic_Neutral)
        print("Please enter AI value(iteration = integer number).(Higher values mean higher intelligence, but also a longer time for the AI to act.)")

        iter = int(input())
        yena = player.MCTSplayer_new("Yena" + str(iter), "Mage", card.Classic_Neutral, iter, 4.0/math.sqrt(2.0))

        # 게임시작
        m = match(yena, user, 1, 0, True)
    else:
        # coef과 iter를 알기위한 실험용
        print("Please enter first AI's coefficient and iteration.")
        firCoef, firIter = map(int, input().split())
        print("Please enter second AI's coefficient and iteration.")
        secCoef, secIter = map(int, input().split())
        print("Please enter number of game.")
        gameNumber = int(input())
        
        # 게임시작
        m = MCTSmatch(None, None, firCoef, firIter, secCoef, secIter, gameNumber, 0, False)

    m.run()
