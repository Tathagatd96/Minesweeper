# ==============================CS-199==================================
# FILE:			MyAI.py
#
# AUTHOR: 		Justin Chung
#
# DESCRIPTION:	This file contains the MyAI class. You will implement your
#				agent in this file. You will write the 'getAction' function,
#				the constructor, and any additional helper functions.
#
# NOTES: 		- MyAI inherits from the abstract AI class in AI.py.
#
#				- DO NOT MAKE CHANGES TO THIS FILE.
# ==============================CS-199==================================

from AI import AI
from Action import Action
import collections


class MyAI( AI ):
    
    def __init__(self, rowDimension, colDimension, totalMines, startX, startY):
        
        self.num_rows=rowDimension
        self.num_cols=colDimension
        self.mine_count=totalMines
        self.startX=startX
        self.startY=startY
        self.action_taken=[]    #Lists the [action,state(x,y),# Important pastpercept(hint of last action))]
        self.todo=collections.deque()
        self.toflag=collections.deque()
        self.curr_world=None
        self.counter=0
        
    def getAction(self, number: int) -> "Action Object":
        
        if self.mine_count==0:
            tile_left=self.tiles_left(self.action_taken)
            if tile_left:
                for pair in tile_left:
                    self.todo.append(pair)
            else:
                ##GAME OVER-WORLD COMPLETE
                return Action(AI.Action.LEAVE)
            self.add_stateSpace("U",self.todo[0][0],self.todo[0][1],number)
            temp_todo=collections.deque()
            temp_todo.append(self.todo[0])
            self.todo.popleft()
            return Action(AI.Action.UNCOVER,temp_todo[0][0],temp_todo[0][1])
        elif self.action_taken:
            curr_world=self.parseActionsForCurrWorld(self.action_taken)
            self.curr_world=curr_world
            lens=[8,3,5]
            #ad=[i for i in range(1,9)]
            if self.todo:
                self.add_stateSpace("U",self.todo[0][0],self.todo[0][1],number)
                temp_todo=collections.deque()
                temp_todo.append(self.todo[0])
                self.todo.popleft()
                return Action(AI.Action.UNCOVER,temp_todo[0][0],temp_todo[0][1])
            
            elif self.toflag:
                self.add_stateSpace("F",self.toflag[0][0],self.toflag[0][1],number)
                temp_toflag=collections.deque()
                temp_toflag.append(self.toflag[0])
                self.todo.popleft()
                self.mine_count-=1
                return Action(AI.Action.FLAG,temp_toflag[0][0],temp_toflag[0][1])
            elif number==0:
                tileX=self.action_taken[-1][1]
                tileY=self.action_taken[-1][2]
                neighbors_list=self.neighbors(tileX,tileY)
                if len(neighbors_list) in lens:
                    adjacents_left=self.adjacent_left(neighbors_list)
                    if adjacents_left:
                        for pair in adjacents_left:
                            self.todo.append(pair)
    
                        self.counter=len(self.todo)
                        self.add_stateSpace("U",self.todo[0][0],self.todo[0][1],number)
                        temp_todo=collections.deque()
                        temp_todo.append(self.todo[0])
                        self.todo.popleft()
                        return Action(AI.Action.UNCOVER,temp_todo[0][0],temp_todo[0][1])
                    
                    else:
                        for i in range(1,len(self.action_taken)):
                            if self.action_taken[i][3]==0:
                                tileX=self.action_taken[i-1][1]
                                tileY=self.action_taken[i-1][2]
                                neighbors_list=self.neighbors(tileX,tileY)
                                adjacents_left=self.adjacent_left(neighbors_list)
                                if adjacents_left:
                                    for pair in adjacents_left:
                                        self.todo.append(pair)
                                else:
                                    continue 
                                self.counter=len(self.todo)
                                self.add_stateSpace("U",self.todo[0][0],self.todo[0][1],number)
                                temp_todo=collections.deque()
                                temp_todo.append(self.todo[0])
                                self.todo.popleft()
                                return Action(AI.Action.UNCOVER,temp_todo[0][0],temp_todo[0][1])
                        
                            elif self.action_taken[i][3] in range(1,9):
                                tileX=self.action_taken[i-1][1]
                                tileY=self.action_taken[i-1][2]
                                neighbors_list=self.neighbors(tileX,tileY)
                                adjacents_left=self.adjacent_left(neighbors_list)
                                num_flags=self.num_flag_checker(neighbors_list)
                                if num_flags==self.action_taken[i][3]:
                                    if adjacents_left:
                                        for pair in adjacents_left:
                                            self.todo.append(pair);
                                        self.counter=len(self.todo)
                                        self.add_stateSpace("U",self.todo[0][0],self.todo[0][1],number)
                                        temp_todo=collections.deque()
                                        temp_todo.append(self.todo[0])
                                        self.todo.popleft()
                                        return Action(AI.Action.UNCOVER,temp_todo[0][0],temp_todo[0][1])
                                    else:
                                        continue
                                elif (num_flags+len(adjacents_left))==self.action_taken[i][3]:
                                    for pair in adjacents_left:
                                        self.toflag.append(pair)
                                    temp_toflag=collections.deque()
                                    temp_toflag.append(self.toflag[0])
                                    self.toflag.popleft()
                                    self.add_stateSpace("F",temp_toflag[0][0],temp_toflag[0][1],number)
                                    self.mine_count-=1
                                    return Action(AI.Action.FLAG,temp_toflag[0][0],temp_toflag[0][1])
                            #else:
                                #continue
                                #selective opening check-chnge else to elif
                            elif self.action_taken[i][3]==-1:
                                return Action(AI.Action.LEAVE)
                                #continue-Remove after minimal sub
                            else:
                                return Action(AI.Action.LEAVE)
                else:
                    return Action(AI.Action.LEAVE)
                    
            elif number in range(1,9):
                for i in range(1,self.counter):
                    if self.action_taken[-i][3]==0:
                        neighbors_list=self.neighbors(self.action_taken[-(i+1)][1],self.action_taken[-(i+1)][2])
                        adjacents_left=self.adjacent_left(neighbors_list)
                        if adjacents_left:
                            for pairs in neighbors_list:
                                self.todo.append(pairs)  
                            self.counter=len(self.todo)
                            temp_todo=collections.deque()
                            temp_todo.append(self.todo[0])
                            self.todo.popleft()
                            self.add_stateSpace("U",temp_todo[0][0],temp_todo[0][1],number)
                            return Action(AI.Action.UNCOVER,temp_todo[0][0],temp_todo[0][1])
                        else:
                            continue
                            #return Action(AI.Action.LEAVE)
                tileX=self.action_taken[-1][1]
                tileY=self.action_taken[-1][2]
                neighbors_list=self.neighbors(tileX,tileY)
                adjacents_left=self.adjacent_left(neighbors_list)
                if number==len(adjacents_left):
                    #bomb condition-check if its touching bombs 
                    num_flags=self.num_flag_checker(neighbors_list)
                    if(num_flags==0):
                        for pairs in adjacents_left:
                            self.toflag.append(pairs)
                        #Popping toflag
                        temp_toflag=collections.deque()
                        temp_toflag.append(self.toflag[0])
                        self.toflag.popleft()
                        self.add_stateSpace("F",temp_toflag[0][0],temp_toflag[0][1],number)
                        self.mine_count-=1
                        return Action(AI.Action.FLAG,temp_toflag[0][0],temp_toflag[0][1])
                    elif num_flags==number:
                        if adjacents_left:
                            for pair in adjacents_left:
                                self.todo.append(pair)
                        #check continue condition
                        self.counter=len(self.todo)
                        self.add_stateSpace("U",self.todo[0][0],self.todo[0][1],number)
                        temp_todo=collections.deque()
                        temp_todo.append(self.todo[0])
                        self.todo.popleft()
                        return Action(AI.Action.UNCOVER,temp_todo[0][0],temp_todo[0][1])
                    else:
                        for i in range(1,len(self.action_taken)):
                            if self.action_taken[i][3]==0:
                                tileX=self.action_taken[i-1][1]
                                tileY=self.action_taken[i-1][2]
                                neighbors_list=self.neighbors(tileX,tileY)
                                adjacents_left=self.adjacent_left(neighbors_list)
                                if adjacents_left:
                                    for pair in adjacents_left:
                                        self.todo.append(pair)
                                else:
                                    continue 
                                self.counter=len(self.todo)
                                self.add_stateSpace("U",self.todo[0][0],self.todo[0][1],number)
                                temp_todo=collections.deque()
                                temp_todo.append(self.todo[0])
                                self.todo.popleft()
                                return Action(AI.Action.UNCOVER,temp_todo[0][0],temp_todo[0][1])
                        
                            elif self.action_taken[i][3] in range(1,9):
                                tileX=self.action_taken[i-1][1]
                                tileY=self.action_taken[i-1][2]
                                neighbors_list=self.neighbors(tileX,tileY)
                                adjacents_left=self.adjacent_left(neighbors_list)
                                num_flags=self.num_flag_checker(neighbors_list)
                                if num_flags==self.action_taken[i][3]:
                                    if adjacents_left:
                                        for pair in adjacents_left:
                                            self.todo.append(pair);
                                        self.counter=len(self.todo)
                                        self.add_stateSpace("U",self.todo[0][0],self.todo[0][1],number)
                                        temp_todo=collections.deque()
                                        temp_todo.append(self.todo[0])
                                        self.todo.popleft()
                                        return Action(AI.Action.UNCOVER,temp_todo[0][0],temp_todo[0][1])
                                    else:
                                        continue
                                elif (num_flags+len(adjacents_left))==self.action_taken[i][3]:
                                    for pair in adjacents_left:
                                        self.toflag.append(pair)
                                    temp_toflag=collections.deque()
                                    temp_toflag.append(self.toflag[0])
                                    self.toflag.popleft()
                                    self.add_stateSpace("F",temp_toflag[0][0],temp_toflag[0][1],number)
                                    self.mine_count-=1
                                    return Action(AI.Action.FLAG,temp_toflag[0][0],temp_toflag[0][1])
                                else:
                                    return Action(AI.Action.LEAVE)
                else:
                    for i in range(1,len(self.action_taken)):
                        if self.action_taken[i][3]==0:
                            tileX=self.action_taken[i-1][1]
                            tileY=self.action_taken[i-1][2]
                            neighbors_list=self.neighbors(tileX,tileY)
                            adjacents_left=self.adjacent_left(neighbors_list)
                            if adjacents_left:
                                for pair in adjacents_left:
                                    self.todo.append(pair)
                            else:
                                continue 
                            self.counter=len(self.todo)
                            self.add_stateSpace("U",self.todo[0][0],self.todo[0][1],number)
                            temp_todo=collections.deque()
                            temp_todo.append(self.todo[0])
                            self.todo.popleft()
                            return Action(AI.Action.UNCOVER,temp_todo[0][0],temp_todo[0][1])
                        
                        elif self.action_taken[i][3] in range(1,9):
                            tileX=self.action_taken[i-1][1]
                            tileY=self.action_taken[i-1][2]
                            neighbors_list=self.neighbors(tileX,tileY)
                            adjacents_left=self.adjacent_left(neighbors_list)
                            num_flags=self.num_flag_checker(neighbors_list)
                            if num_flags==self.action_taken[i][3]:
                                if adjacents_left:
                                    for pair in adjacents_left:
                                        self.todo.append(pair);
                                    self.counter=len(self.todo)
                                    self.add_stateSpace("U",self.todo[0][0],self.todo[0][1],number)
                                    temp_todo=collections.deque()
                                    temp_todo.append(self.todo[0])
                                    self.todo.popleft()
                                    return Action(AI.Action.UNCOVER,temp_todo[0][0],temp_todo[0][1])
                                else:
                                    continue
                            elif (num_flags+len(adjacents_left))==self.action_taken[i][3]:
                                for pair in adjacents_left:
                                    self.toflag.append(pair)
                                temp_toflag=collections.deque()
                                temp_toflag.append(self.toflag[0])
                                self.toflag.popleft()
                                self.add_stateSpace("F",temp_toflag[0][0],temp_toflag[0][1],number)
                                self.mine_count-=1
                                return Action(AI.Action.FLAG,temp_toflag[0][0],temp_toflag[0][1])
                            else:
                                continue
                                #selective opening check
                        
                        else:
                            return Action(AI.Action.LEAVE)
            elif number==-1:
                tileX=self.action_taken[-1][1]
                tileY=self.action_taken[-1][2]
                neighbors_list=self.neighbors(tileX,tileY)
                adjacents_left=self.adjacent_left(neighbors_list)
                uncovered=[i for i in neighbors_list if i not in adjacents_left]
                for pairs in uncovered:
                    hint=self.hint_checker(pairs)
                    tileX=pairs[0]
                    tileX=pairs[1]
                    neighbors_list=self.neighbors(tileX,tileY)
                    num_flags=self.num_flag_checker(neighbors_list)
                    if num_flags==hint:
                        adjacents_left=self.adjacent_left(neighbors_list)
                        if adjacents_left:
                            for pair in adjacents_left:
                                self.todo.append(pair)
                            temp_todo=collections.deque()
                            temp_todo.append(self.todo[0])
                            self.todo.popleft()
                            self.add_stateSpace("U",temp_todo[0][0],temp_todo[0][1],number)
                            return Action(AI.Action.UNCOVER,temp_todo[0][0],temp_todo[0][1])
                        else:
                            continue
                            #return Action(AI.Action.LEAVE)
                    else:
                        continue
                for i in range(len(self.action_taken)):
                    if self.action_taken[i][3]==0:
                        tileX=self.action_taken[i-1][1]
                        tileY=self.action_taken[i-1][2]
                        neighbors_list=self.neighbors(tileX,tileY)
                        adjacents_left=self.adjacent_left(neighbors_list)
                        if adjacents_left:
                            for pair in adjacents_left:
                                self.todo.append(pair)
                        else:
                            continue
                        self.counter=len(self.todo)
                        self.add_stateSpace("U",self.todo[0][0],self.todo[0][1],number)
                        temp_todo=collections.deque()
                        temp_todo.append(self.todo[0])
                        self.todo.popleft()
                        return Action(AI.Action.UNCOVER,temp_todo[0][0],temp_todo[0][1])
                        
                    elif self.action_taken[i][3] in range(1,9):
                            tileX=self.action_taken[i-1][1]
                            tileY=self.action_taken[i-1][2]
                            neighbors_list=self.neighbors(tileX,tileY)
                            adjacents_left=self.adjacent_left(neighbors_list)
                            num_flags=self.num_flag_checker(neighbors_list)
                            if num_flags==self.action_taken[i][3]:
                                if adjacents_left:
                                    for pair in adjacents_left:
                                        self.todo.append(pair);
                                    self.counter=len(self.todo)
                                    self.add_stateSpace("U",self.todo[0][0],self.todo[0][1],number)
                                    temp_todo=collections.deque()
                                    temp_todo.append(self.todo[0])
                                    self.todo.popleft()
                                    return Action(AI.Action.UNCOVER,temp_todo[0][0],temp_todo[0][1])
                                else:
                                    continue
                            elif (num_flags+adjacents_left)==self.action_taken[i][3]:
                                for pair in adjacents_left:
                                    self.toflag.append(pair)
                                temp_toflag=collections.deque()
                                temp_toflag.append(self.toflag[0])
                                self.toflag.popleft()
                                self.add_stateSpace("F",temp_toflag[0][0],temp_toflag[0][1],number)
                                self.mine_count-=1
                                return Action(AI.Action.FLAG,temp_toflag[0][0],temp_toflag[0][1])
                            else:
                                continue
                                #selective opening check
            else:
                #Give up condiion
                return Action(AI.Action.LEAVE)
            
        else:
            self.add_stateSpace("U",self.startX,self.startY,0)
            neighbors_list=self.neighbors(self.startX,self.startY)
            for pairs in neighbors_list:
                self.todo.append(pairs)  
            self.counter=len(self.todo)
            temp_todo=collections.deque()
            temp_todo.append(self.todo[0])
            self.todo.popleft()
            self.add_stateSpace("U",temp_todo[0][0],temp_todo[0][1],number)
            return Action(AI.Action.UNCOVER,temp_todo[0][0],temp_todo[0][1])
            
    def add_stateSpace(self,action,cordx,cordy,pastperceptNo):
        act=[action,cordx,cordy,pastperceptNo]
        self.action_taken.append(act)
        
    def num_flag_checker(self,neighbors_list):
        counter=0
        c=[]
        cords=self.extractcords()
        for tiles in neighbors_list:
            c=[tiles[0],tiles[1]]
            if c in cords:
                for states in self.action_taken:
                    if states[1]==tiles[0] and states[2]==tiles[1]:
                        if states[0]=="F":
                            counter+=1
                        else:
                            continue
                    else:
                        continue
            else:
                continue
                
        return counter
            
    
    def hint_checker(self,pair):
        for i in range(len(self.curr_world)):
            if self.curr_world[i][1]==pair[0] and self.curr_world[i][2]==pair[1]:
                return self.curr_world[i+1][3]
            else:
                return None
    
    def state_checker(self,pair):
        counter=0
        for state in self.curr_world:
            if state[1]==pair[0] and state[2]==pair[1]:
                counter+=1    
        if counter==0:
            return True,pair
        else:
            return False,pair
        
    def createWorld(self):
        val=[1]*self.num_rows
        for i in range(self.num_rows):
            val[i]=[1]*self.num_cols
                    
        return val
            
    def parseActionsForCurrWorld(self,prev_actions):
        
        new_world=self.createWorld()
        for i in range(len(prev_actions)):
            action,cordx,cordy,hint=prev_actions[i]
            new_world[cordx][cordy]=hint
            
        return new_world
    
    def adjacent_left(self,neighbors_list):
        adjacents=[]
        c=[]
        cords=[]
        for tiles in neighbors_list:
            c=[tiles[0],tiles[1]]
            cords=self.extractcords()
            if c not in cords:
                adjacents.append(c)
            else:
                continue
        return adjacents
    
    def extractcords(self):
        cords=[]
        for states in self.action_taken:
            a=states[1]
            b=states[2]
            cords.append([a,b])
        return cords
    
    def tiles_left(self,action_taken):
        left_list=[]
        world_list=[]
        cords_list=self.extractcords()
        for i in range(self.num_rows):
            for j in range(self.num_cols):
                world_list.append([i,j])
        for pairs in world_list:
            if pairs not in cords_list:
                left_list.append(pairs)
        return left_list
                       
    
            
    def neighbors(self,tileX,tileY):
            #Send tiles-1
            #Return list of (x,y) pairs of neighbor tiles
            #neighbor_list=[]
            #For Corner tiles
            if tileX==0 and tileY==0:
                neighbor_list=[[tileX+1,tileY],[tileX+1,tileY+1],[tileX,tileY+1]]
                return neighbor_list
            elif tileX==0 and tileY==(self.num_cols-1):
                neighbor_list=[[tileX+1,tileY],[tileX+1,tileY-1],[tileX,tileY-1]]
                return neighbor_list
            elif tileX==(self.num_rows-1) and tileY==0:
                neighbor_list=[[tileX-1,tileY],[tileX-1,tileY+1],[tileX,tileY+1]]
                return neighbor_list
            elif tileX==(self.num_rows-1) and tileY==(self.num_cols-1):
                neighbor_list=[[tileX-1,tileY],[tileX-1,tileY-1],[tileX,tileY-1]]
                return neighbor_list
            #For wall tiles
            elif tileX in range(1,self.num_rows-1) and tileY==0:
                neighbor_list=[[tileX-1,tileY],[tileX-1,tileY+1],[tileX,tileY+1],[tileX+1,tileY+1],[tileX+1,tileY]]
                return neighbor_list
            elif tileX in range(1,self.num_rows-1) and tileY==(self.num_cols-1):
                neighbor_list=[[tileX-1,tileY],[tileX-1,tileY-1],[tileX,tileY-1],[tileX+1,tileY-1],[tileX+1,tileY]]
                return neighbor_list
            elif tileX==0 and tileY in range(1,self.num_cols-1):
                neighbor_list=[[tileX,tileY+1],[tileX+1,tileY+1],[tileX+1,tileY],[tileX+1,tileY-1],[tileX,tileY-1]]
                return neighbor_list
            elif tileX==(self.num_rows-1) and tileY in range(1,self.num_cols-1):
                neighbor_list=[[tileX,tileY+1],[tileX-1,tileY+1],[tileX-1,tileY],[tileX-1,tileY-1],[tileX,tileY-1]]
                return neighbor_list
            #For all other central tiles
            else:
                neighbor_list=[[tileX-1,tileY+1],[tileX,tileY+1],[tileX+1,tileY+1],[tileX+1,tileY],[tileX+1,tileY-1],[tileX,tileY-1],[tileX-1,tileY-1],[tileX-1,tileY]]
                return neighbor_list
            
                    
                    
                    
                
            