import copy 
# turn_color=True, p1.order=True, black의 차례(선공차례), game(p1,p2)가 시작한 이후로 p1.order=true, p2.order=false 
class UCTNODE():
    def __init__(self, b, action, parent):
        self.b = copy.deepcopy(b) 
        self.action = action        #node가 생성되게 된 action
        # self.color = color          #MCTS player가 p1인지 p2인지 알 수 있게 해주는 단서

        if(self.b.turn_color):      #turn_color==True면 p1차례.. 그러나 MCTS player가 p2라면?
            self.legalactionlist = self.b.getlegalaction(self.b.p1)
        else:
            self.legalactionlist = self.b.getlegalaction(self.b.p2)
        
        self.is_terminal = False 
        self.parent = parent 
        self.children = [] 
        self.Q = 0 
        self.N = 0 

        # terminal node check p1.health<=0 or p2.health<=0
        if(self.b.p1.health<=0 or self.b.p2.health<=0):     #체력이 0보다 작거나 같으면 terminal node
            self.is_terminal = True 

        self.is_expanded = False 

    def untried_action(self): 
        tried = [] 
        for c in self.children:
            tried.append(c.action)
        
        untried = []
        for m in self.legalactionlist:
            if m not in tried:
                untried.append(m) 
        
        return untried
    
    def add_child(self, action): 
        new_b = copy.deepcopy(self.b)

        new_b.inDEFAULTPOLICY = True

        if(action!=None):
            if(new_b.turn_color):
                new_b.doaction(new_b.p1, action)
            else:
                new_b.doaction(new_b.p2, action)

        new_b.inDEFAULTPOLICY = False

        child = UCTNODE(new_b, action, self)
        self.children.append(child)

        if(len(self.untried_action())==0):
            self.is_expanded=True 

        return child 



    """
    # def flip_color(self,color):
    #     if(color==config.black):
    #         return config.white 
    #     else: 
    #         return config.black 
    """
   
    def print_tree(self,Level=0):
        print()
        print("Level=",Level)
        # self.b.print() 
        Level = Level +1 
        for c in self.children:
            c.print_tree(Level) 
    