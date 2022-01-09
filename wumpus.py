import random
import sys
class Agent:
    def __init__(self,pos,mes):
        self.pos = pos
        self.mes = mes
    
    def step(self):
        return self.I.step()

class AI:
    def __init__(self,agent):
        self.agent = agent
        self.path = []
        self.wamcan = []
        self.wamnot = []
    
    
    def base_analyze(self):
        for can in self.wamcan:
            if can in self.wamnot:
                self.wamcan.remove(can)
                self.wamnot.remove(can)
        
        if len(self.wamcan) == 1:
            self.coor = self.wamcan[0]
    
    
    
    def analyze(self,a):
        ancan = a
        if ancan == None:
            self.base_analyze()
        else:
            for can in self.wamcan:
                if can in self.wamnot and can in ancan:
                    self.wamcan.remove(can)
                    self.wamnot.remove(can)      
                    ancan.remove(can)
                elif can in self.wamnot:
                    self.wamnot.remove(can)
                    self.wamcan.remove(can)
                elif can in ancan:
                    self.wamcan.remove(can)
                    ancan.remove(can)
            
            if len(self.wamnot)>0:
                for an in self.wamcan:
                    if an not in ancan:
                        self.wamcan.remove(an)
            for b in ancan:
                self.wamcan.append(b)
            
            if len(self.wamcan)==1:
                self.coor = self.wamcan[0]
    
    
    
    def ret(self):
        self.agent.pos = self.path[len(self.path)-1]
        self.path.pop(len(self.path)-1)       
    
    
    
    
    def step(self):
        print("You are in room {}".format(self.agent.pos))
        print("You can move or shoot at rooms {}".format(self.agent.env.map[self.agent.pos][1]))
        
        ok = True
        iss = False
        if self.agent.env.agents[1].pos in self.agent.env.map[self.agent.pos][1]:
            print(self.agent.env.agents[1].mes)
            ok = False  
        for ag in range(2,len(self.agent.env.agents)):
            if self.agent.env.agents[ag].pos in self.agent.env.map[self.agent.pos][1]:
                print(self.agent.env.agents[ag].mes)
                iss = True
        print(ok,self.agent.env.agents[1].pos,self.agent.env.map[self.agent.pos][1])
        if ok:
            for place in self.agent.env.map[self.agent.pos][1]:
                if place not in self.wamnot:
                    self.wamnot.append(place)
            self.analyze(None)
            if iss:
                self.ret()
            else:
                self.path.append(self.agent.pos)
                self.agent.pos = random.choice(self.agent.env.map[self.agent.pos][1])
        else:
            if len(self.wamcan) == 1:
                if self.coor in self.agent.env.map[self.agent.pos][1]:
                    print("Shoot at room {}".format(self.coor))
                    if self.coor == self.agent.env.agents[1].pos:
                        print("You won")
                        return False,True
                    else:
                        print("...")
                        return True,False
            self.analyze(self.agent.env.map[self.agent.pos][1])
            self.ret()
        return False,False



class Player:
    def __init__(self,agent):
        self.agent = agent
        self.arrows = 5
    
    
    
    def shooting(self):
        try:
            cur = self.agent.pos
            print("You have {} arrow(s)".format(self.arrows+1))
            rooms = int(input("Number of rooms "))
            for i in range(rooms):
                nex = int(input("Next room "))
                if nex in self.agent.env.map[cur][1]:
                    cur = nex
                else:
                    cur = random.choice(self.agent.env.map[cur][1])
                if cur == self.agent.env.agents[1].pos:
                    print("You won!")
                    return True
                elif cur == self.agent.pos:
                    print("Oohhh... You killed yourself...")
                    return True
            print("You missed")
        except:
            print("You write bad things")
    
    
    
    def step(self):
        print("You are in room {}".format(self.agent.pos))
        print("You can move or shoot at rooms {}".format(self.agent.env.map[self.agent.pos][1]))
        for ag in range(1,len(self.agent.env.agents)):
            if self.agent.env.agents[ag].pos in self.agent.env.map[self.agent.pos][1]:
                print(self.agent.env.agents[ag].mes)
        while True:
            try:
                task,num = input().split()
                task = str(task)
                num = int(num)
                if task == "move" or task == "m":
                    if num < 20 and num >0 and num in self.agent.env.map[self.agent.pos][1]:
                        self.agent.pos = num
                        return False,False
                    else:
                        continue
                elif (task == "shoot" or task == "shot" or task == "s") and self.arrows>0 :
                    self.arrows-=1
                    ex = self.shooting()
                    if ex!=None:
                        break
                    return True,False
            except:
                continue
        
        return True,True



class Wampus:
    def __init__(self,agent):
        self.agent = agent
    
    def step(self):
        do = random.randint(0, 3)
        if do == 0:
            pass
        else:
            self.agent.pos = random.choice(self.agent.env.map[self.agent.pos][1])
    




class Environment:
    def __init__(self,agents):
        self.make_map()
        self.agents = agents
    
    def update(self):
        shot,ex = self.agents[0].step()
        if ex:
            sys.exit()
        
        if self.agents[0].pos == self.agents[2].pos or self.agents[0].pos == self.agents[3].pos:
            print("A bat transported you to another room!")
            self.agents[0].pos = random.randint(0,19)
        if self.agents[0].pos == self.agents[1].pos:
            print("You are eaten by wampus!Wumpus is happy :)!")
            sys.exit()
        if shot:
            self.agents[1].step()
    
    
    
    def make_map(self):
        mapp = []
        mapp.append([0,[1,2,3]])
        mapp.append([1,[0,6,18]])
        mapp.append([2,[0,4,5]])
        mapp.append([3,[0,8,19]])
        mapp.append([4,[2,6,10]])
        mapp.append([5,[2,8,11]])
        mapp.append([6,[1,4,7]])
        mapp.append([7,[6,12,15]])
        mapp.append([8,[3,5,9]])
        mapp.append([9,[8,13,17]])
        mapp.append([10,[4,11,12]])
        mapp.append([11,[5,10,13]])
        mapp.append([12,[7,10,14]])
        mapp.append([13,[9,11,14]])
        mapp.append([14,[12,13,16]])
        mapp.append([15,[7,16,18]])
        mapp.append([16,[14,15,17]])
        mapp.append([17,[9,16,19]])
        mapp.append([18,[1,15,19]])
        mapp.append([19,[3,17,18]])
        self.map = mapp.copy()


if __name__ == '__main__':
    print("HUNT THE WUMPUS")
    
    mode = input("Write p to play, write a to watch ai ")
    
    player = Agent(0,'')
    
    
    if mode == "p":
        pl = Player(player)
    else:
        pl = AI(player)
    
    player.I = pl
    
    wampus = Agent(random.randint(4,19),"You feel a Wampus!")
    wm = Wampus(wampus)
    wampus.I = wm
    
    bat1 = Agent(random.randint(4,19),"You hear a loud noise")
    bat2 = Agent(random.randint(4,19),"You hear a loud noise")
    if bat1.pos == bat2.pos:
        if bat2.pos!=0:
            bat2.pos-=1
        else:
            bat2.pos+=1
    
    env = Environment([player,wampus,bat1,bat2])
    player.env = env
    wampus.env = env
    bat1.env = env
    bat2.env = env
    a=0
    while a<100:
        env.update()
        a+=1