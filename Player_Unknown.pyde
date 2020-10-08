add_library('minim')
path = os.getcwd()
musicplayer = Minim(this)
# The lists below are the coordinates of objects being displayed in the game
walk_list = [[107,30],[139,28],[168,32],[201,32],[235,28],[266,29],[297,32],[330,36],[366,31]]
walk_list1 = [[407,39],[450,32],[490,27],[524,25],[559,22],[591,24],[623,24],[652,28],[689,27],[720,34],[759,37],[800,47]]
walk_list2 = [[1070,27],[1032,28],[985,35],[928,41],[878,39],[834,36],[799,31],[767,29],[730,28],[698,29]]
walk_list3 = [[1023,49],[965,47],[910,46],[855,50],[807,47],[756,44],[703,45],[658,41],[615,41],[570,38],[520,40],[472,38],[424,40],[380,37],[332,38],[281,42],[230,49],[179,43]]
walk_list4 = [[960,33],[992,31],[1025,30],[1057,30],[1089,32]]
walk_list5 = [[137,29],[173,30],[208,31],[240,27]]
walk_list6 = [[2,33],[36,33],[71,32],[105,31],[136,32],[170,36],[210,31],[243,31]]
walk_list7 = [[3,35],[45,33],[85,31],[120,30]]
walk_list8 = [[157,31],[198,31],[238,31],[278,30]]
walk_list9 = [[314,33],[357,35],[401,36],[444,37]]
walk_list_s = [[926,29],[963,27],[997,25],[1030,24],[1061,21]]
soldier_death=[[1,29],[39,68],[78,109],[119,153],[163,202],[213,255],[264,307],[317,365],[377,423],[434,482],[494,542],[553,600],[610,656],[667,714],[725,773]]
player_death=[[709,740],[744,781],[783,825],[829,874],[876,921],[925,970],[975,1020],[1021,1067],[1070,1117],[1122,1169]]
player_life=[[3,49],[55,100],[104,145],[149,191],[196,237],[240,277],[280,312],[317,349],[352,380],[385,415],[418,448],[449,478],[481,506],[512,537],[542,567],[569,595],[599,624],[627,650],[655,681]]
platform=[[[685,840,108],[1191,1265,164],[1196,1450,63],[1282,1463,115],[1479,1553,164],[1484,1738,63],[1570,1751,115],[1854,1928,164],[1859,2113,63],[1945,2126,115],[2248,2368,118],[2814,3195,101]],[[73,132,106],[198,254,106],[290,359,106],[414,479,106],[508,575,111],[621,689,111],[752,794,120],[866,908,120],[992,1022,105],[1100,1140,105],[3002,3566,87]],[[242,350,61],[548,656,61],[992,1106,68],[1238,1316,52],[1910,2018,92],[2540,2648,92],[2696,2768,64],[2924,3026,92]]]
leg_list = [[256,277],[280,308],[311,342],[345,364],[366,382],[384,401],[404,425],[428,454],[457,489],[491,511],[512,528],[530,549]]
mine=[[978,12],[991,13],[1006,13],[1019,20],[1040,17]]
grenade=[[32,267,43,286],[89,249,101,268],[149,246,163,265],[219,240,234,259],[245,250,263,267],[267,263,284,277],[288,274,308,286],[306,289,325,300]]
water = [[57,86],[87,120],[121,153],[154,190],[193,227],[228,260],[261,289],[291,320]]

class Creature:
    def __init__(self,x,y,r,g,img,w,h,F):
        self.x=x
        self.y=y
        self.r=r  # the radius of the corresponding circle
        self.g=g  # the ground
        self.img = loadImage(path+"/images/"+img)
        self.w=w
        self.h=h
        self.F=F  # total number of frames 
        self.vx=0  # horizontal velocity 
        self.vy=0  # vertical velocity
        self.f=0  # counter corresponding to the current frame being displayed
        self.dir=1  # direction the creature is facing
        
    
    def gravity(self):
        if self.y + self.r < self.g:  # if the creature is in the air
            self.vy += 0.8
            if self.y+self.r+self.vy > self.g:
                self.vy = self.g-(self.y+self.r)  # prevent that one single addition of vertical value surpasses the ground
        else:
            self.vy = 0
        
        for i in platform[g.mission-1]:  # add platforms in three missions
            if self.x in range(i[0],i[1]) and self.y+self.r <= i[2]:
                self.g = i[2]
                break
            else:
                self.g = g.g
        
        if g.mission==2:  # add stairs in mission2      
            if self.x in range(1268,1346) and self.y <= -0.833333*self.x+1229:
                self.g = -0.833333*self.x+1230
                if self.y + self.r >= self.g:
                    self.y = self.g-self.r
                else:
                    self.vy += 0.8
                    self.y += self.vy
            elif self.x in range(1346,1472) and self.y<=100:
                 self.g=97.33378+self.r
    
    def update(self):
        self.gravity()
        self.x += self.vx
        self.y += self.vy
    
    def display(self):
        self.update()
        #display the image of figures based on the direction they are facing
        if self.dir > 0:
            image(self.img,self.x-self.w//2-g.x,self.y-self.h//2,self.w,self.h,int(self.f)*self.w,0,int(self.f+1)*self.w,self.h)
        elif self.dir < 0:
            image(self.img,self.x-self.w//2-g.x,self.y-self.h//2,self.w,self.h,int(self.f+1)*self.w,0,int(self.f)*self.w,self.h)        

class Player(Creature):
    def __init__(self,x,y,r,g,img,w,h,F,life,jump=False):
        Creature.__init__(self,x,y,r,g,img,w,h,F)
        self.life = life  # number of lives when game starts
        self.jump=jump 
        self.keyHandler={LEFT:False,RIGHT:False,UP:False,DOWN:False}
        self.fire=[]
        self.grenade = False
        self.ofire = False
        self.dead = False
        self.liveF = 19
        self.livef = 0
        self.deadF = 10
        self.deadf = 0   
        self.water = False 
        self.waterf = 0
        self.killCnt = 0
        self.rampage = False
        self.gameoverSound = musicplayer.loadFile(path+"/sounds/gameover.mp3")
        self.gun = musicplayer.loadFile(path+"/sounds/gun.wav")
        
    def display(self):
        if self.rampage:
            self.rampagetime -= 1
            if self.rampagetime >= 0:
                image(g.two,self.x-self.w//2-g.x,self.y-self.h//2,30,56,695,2456,725,2512)
                self.vx = 30  # fast movement during rampage
                self.x += self.vx
                if self.x >= g.w/2:  # scrolling of screen
                    if (g.mission==1 and self.x<3068) or (g.mission==2 and self.x<2993) or (g.mission==3 and self.x<2090):
                        g.x += self.vx
                for s in g.soldier:  # all soldiers on the way are killed
                    if self.distance(s) < self.r + s.r and not s.dead and not self.dead:
                        s.dead = True
                        self.killCnt += 1
            else:
                self.rampage = False
        else:
            if self.water:
                self.update()
                self.waterf = (self.waterf+0.2)%self.F
                #display drinking water movements
                if self.waterf <= 5:
                    if self.dir > 0:
                        image(self.img,self.x-self.w//2-g.x,self.y-self.h//2,water[int(self.waterf)][1]-water[int(self.waterf)][0],38,water[int(self.waterf)][0],139,water[int(self.waterf)][1],177)
                    else:
                        image(self.img,self.x-self.w//2-g.x,self.y-self.h//2,water[int(self.waterf)][1]-water[int(self.waterf)][0],38,water[int(self.waterf)][1],139,water[int(self.waterf)][0],177)
                else:
                    self.water=False
                
            else:
                self.update()
                if not self.dead:
                    if self.ofire == True:
                        self.gun.rewind()
                        self.gun.play()
                        if self.dir > 0:
                            if self.vx != 0:#allowing legs to move when opening fire by seperating the torso and legs 
                                image(self.img,self.x-self.w//2-g.x,self.y-self.h//2,52,23,53,57,105,80)
                                image(g.two,self.x-self.w//2-g.x,self.y+1,leg_list[int(self.f)][1]-leg_list[int(self.f)][0],20,leg_list[int(self.f)][0],1533,leg_list[int(self.f)][1],1553)
                            else:
                                image(self.img,self.x-self.w//2-g.x,self.y-self.h//2,52,38,53,57,105,95)                       
                        else:
                            if self.vx != 0:#allowing legs to move when opening fire by seperating the torso and legs
                                image(self.img,self.x-self.w//2-g.x-20,self.y-self.h//2,52,23,105,57,53,80)
                                image(g.two,self.x-self.w//2-g.x+4,self.y+1,leg_list[int(self.f)][1]-leg_list[int(self.f)][0],20,leg_list[int(self.f)][1],1533,leg_list[int(self.f)][0],1553)
                            else:
                                image(self.img,self.x-self.w//2-g.x-20,self.y-self.h//2,52,38,105,57,53,95)
                    
                    elif self.grenade == True:
                        if self.dir > 0:
                            if self.vx != 0:#allowing legs to move when throwing grenades by seperating the torso and legs
                                image(self.img,self.x-self.w//2-g.x+1,self.y-self.h//2,self.w,23,48,260,80,286)
                                image(g.two,self.x-self.w//2-g.x,self.y+1,leg_list[int(self.f)][1]-leg_list[int(self.f)][0],20,leg_list[int(self.f)][0],1533,leg_list[int(self.f)][1],1553)
                            else:
                                image(self.img,self.x-self.w//2-g.x+1,self.y-self.h//2,self.w,38,48,260,80,301)                       
                        else:
                            if self.vx != 0:#allowing legs to move when throwing grenades by seperating the torso and legs
                                image(self.img,self.x-self.w//2-g.x,self.y-self.h//2,self.w,23,80,260,48,286)
                                image(g.two,self.x-self.w//2-g.x+4,self.y+1,leg_list[int(self.f)][1]-leg_list[int(self.f)][0],20,leg_list[int(self.f)][1],1533,leg_list[int(self.f)][0],1553)
                            else:
                                image(self.img,self.x-self.w//2-g.x,self.y-self.h//2,self.w,38,80,260,48,301)            
                    #jumping image
                    elif self.vy != 0 and self.dir > 0:
                        image(self.img,self.x-self.w//2-g.x,self.y-self.h//2,self.w,self.h,186,190,215,self.h+190)
                    elif self.vy != 0 and self.dir < 0:
                        image(self.img,self.x-self.w//2-g.x,self.y-self.h//2,self.w,self.h,215,190,186,self.h+190)
                    #normal walking
                    elif self.dir > 0 and self.vy == 0:
                        image(self.img,self.x-self.w//2-g.x,self.y-self.h//2,walk_list[int(self.f)][1],self.h,walk_list[int(self.f)][0],0,walk_list[int(self.f)][0]+walk_list[int(self.f)][1],self.h)
                    elif self.dir < 0 and self.vy == 0:
                        image(self.img,self.x-self.w//2-g.x,self.y-self.h//2,walk_list[int(8-self.f)][1],self.h,walk_list[int(8-self.f)][1]+walk_list[int(8-self.f)][0],0,walk_list[int(8-self.f)][0],self.h)
                else:
                    self.deadf = self.deadf+0.8
                    if self.deadf <= 10:#display dying movements
                        if self.dir < 0:
                            image(g.two,self.x-self.w//2-g.x,self.y-self.h//2,player_death[int(self.deadf)][1]-player_death[int(self.deadf)][0],48,player_death[int(self.deadf)][1],3060,player_death[int(self.deadf)][0],3108)                    
                        elif self.dir > 0:
                            image(g.two,self.x-self.w//2-g.x,self.y-self.h//2,player_death[int(self.deadf)][1]-player_death[int(self.deadf)][0],48,player_death[int(self.deadf)][0],3060,player_death[int(self.deadf)][1],3108)
                    else:
                        if self.life > 0:
                            self.livef = self.livef + 0.7    
                            if self.livef <= 19:#display reborning movements
                                if self.dir < 0:
                                    image(g.two,self.x-self.w//2-g.x,self.y-self.h//2,player_life[int(self.livef)][1]-player_life[int(self.livef)][0],48,player_life[int(self.livef)][1],3210,player_life[int(self.livef)][0],3250)                    
                                elif self.dir > 0:
                                    image(g.two,self.x-self.w//2-g.x,self.y-self.h//2,player_life[int(self.livef)][1]-player_life[int(self.livef)][0],48,player_life[int(self.livef)][0],3210,player_life[int(self.livef)][1],3250)
                            else:
                                self.life -= 1 
                                self.dead = False
                                self.livef=0
                                self.deadf=0
                        else:
                            g.state = 'gameover'
                            
    def update(self):
        if self.vx != 0 or self.jump==True:
            self.f = (self.f+0.3)%self.F
        self.gravity()
        
        if self.keyHandler[LEFT] == True and not self.dead:
            self.vx = -6
            self.dir = -1
        elif self.keyHandler[RIGHT] == True and not self.dead:
            self.vx = 6
            self.dir = 1
        else:
            self.vx = 0
            
        if self.keyHandler[UP] == True and self.y+self.r == self.g and not self.dead:
            self.vy = -13
        
        self.x += self.vx
        self.y += self.vy
        
        #Any contact with enemies kills both the captain and soldier
        for s in g.soldier:
            if self.distance(s) < self.r + s.r and not s.dead and not self.dead:
                self.dead = True
                s.dead = True
                self.killCnt += 1

        #Roll the screen
        if self.x >= g.w/2:
            if (g.mission==1 and self.x<3068) or (g.mission==2 and self.x<2993) or (g.mission==3 and self.x<2090):  # screen stops scrolling when approaching the end
                g.x += self.vx

        for w in g.water:
            if self.distance(w) < self.r + w.r:
                self.water = True
                g.water.remove(w)
                del w
                self.life += 1
        
    def distance (self,e):
        return ((self.x-e.x)**2+(self.y-e.y)**2)**0.5

class Soldier(Creature):
    def __init__(self,x,y,r,g,img,w,h,F):
        Creature.__init__(self,x,y,r,g,img,w,h,F)
        self.dir = -1
        self.ddir = self.dir
        self.dead = False
        self.deadF = 15
        self.deadf = 0
        self.cy = 92 #this is the left up y cordinate where we crop particular soldier from a large soldier picture
        self.wl = walk_list_s
        self.sdead=musicplayer.loadFile(path+"/sounds/sdeath.wav")
        self.notplayed=True  # play the death sound only once
        
    def display(self):
        if not self.dead:
            self.update()
            if self.dir>0:
                image(self.img,self.x-self.w//2-g.x,self.y-self.h//2,self.wl[int(self.F-self.f-1)][1],self.h,self.wl[int(self.F-self.f-1)][1]+self.wl[int(self.F-self.f-1)][0],self.cy,self.wl[int(self.F-self.f-1)][0],self.cy+self.h)
            elif self.dir<0:
                image(self.img,self.x-self.w//2-g.x,self.y-self.h//2,self.wl[int(self.f)][1],self.h,self.wl[int(self.f)][0],self.cy,self.wl[int(self.f)][0]+self.wl[int(self.f)][1],self.cy+self.h)         
        else:
            self.gravity()
            self.y += self.vy 
            #display dying movements
            self.deadimg()
            if self.notplayed:#only play dying sound once
                self.sdead.rewind()
                self.sdead.play()
                self.notplayed=False
    
    def update(self):
        self.f = (self.f+0.4)%self.F
        self.gravity()
        self.y += self.vy
    
    def deadimg(self):
        self.deadf = self.deadf+0.3
        if self.deadf <= 15:
            if self.ddir > 0:
                image(self.img,self.x-self.w//2-g.x,self.y-self.h//2,soldier_death[int(self.deadf)][1]-soldier_death[int(self.deadf)][0],45,soldier_death[int(self.deadf)][1],1430,soldier_death[int(self.deadf)][0],1475)                    
            elif self.ddir < 0:
                image(self.img,self.x-self.w//2-g.x,self.y-self.h//2,soldier_death[int(self.deadf)][1]-soldier_death[int(self.deadf)][0],45,soldier_death[int(self.deadf)][0],1430,soldier_death[int(self.deadf)][1],1475)
        else:
            g.soldier.remove(self)
 
        
class Soldier1(Soldier):
    def __init__(self,x,y,r,g,img,w,h,F,x1,x2):
        Soldier.__init__(self,x,y,r,g,img,w,h,F)
        self.x1 = x1
        self.x2 = x2
        self.vx = -4
        self.cy = 243
        self.wl = walk_list1
                
    def update(self):
        if self.vx != 0:
            self.f = (self.f+0.5)%self.F    
        self.gravity()
        if self.x not in range(self.x1,self.x2):
            self.vx = -self.vx
            self.dir = -self.dir
            self.ddir = -self.ddir
        self.x += self.vx
        self.y += self.vy
    
class Soldier2(Soldier):
    def __init__(self,x,y,r,g,img,w,h,F):
        Soldier.__init__(self,x,y,r,g,img,w,h,F)
        self.dir = 1
        self.ddir = -1
        self.vx = -3
        self.cy = 509
        self.wl = walk_list2
                
    def update(self):
        self.f = (self.f+0.4)%self.F
        self.gravity()
        if self.f<7.7 and self.f>7.5:#only append one fire ball once each process
            g.ball.append(Ball(self.x+2,self.y+self.r,8,g.g,'soldier.png',16,16,8))
        self.y += self.vy

class Soldier3(Soldier):
    def __init__(self,x,y,r,g,img,w,h,F):
        Soldier.__init__(self,x,y,r,g,img,w,h,F)
        self.dir = 1
        self.ddir = -1
        self.vx = -3
        self.cy = 677
        self.wl = walk_list3
        
    def update(self):
        self.f = (self.f+0.4)%self.F
        if self.f<13.7 and self.f>13.5:#only append one mine once each process
            g.mine.append(Mine(self.x+2,self.y,9,g.g,'soldier.png',18,15,5))
        self.gravity()
        self.y +=self.vy
       
class Soldier4(Soldier1):
    def __init__(self,x,y,r,g,img,w,h,F,x1,x2):
        Soldier1.__init__(self,x,y,r,g,img,w,h,F,x1,x2)
        self.vx = -4
        self.vy = -10
        self.cy = 0
        self.wl = walk_list4
    def update(self):
        if self.vx != 0:
            self.f = (self.f+0.5)%self.F    
        self.gravity()
        if self.x not in range(self.x1,self.x2):
            self.vx = -self.vx
            self.dir = -self.dir
            self.ddir = -self.ddir
        
        if self.y + self.r >= self.g:
            self.vy = -6
        
        self.x += self.vx
        self.y += self.vy

class Soldier5(Soldier):
    def __init__(self,x,y,r,g,img,w,h,F):
        Soldier.__init__(self,x,y,r,g,img,w,h,F)
        self.cy = 0
        self.wl = walk_list5

class Soldier6(Soldier1):
    def __init__(self,x,y,r,g,img,w,h,F,x1,x2):
        Soldier1.__init__(self,x,y,r,g,img,w,h,F,x1,x2)
        self.vx = -10
        self.cy = 1963
        self.wl = walk_list6

class Soldier7(Soldier):
    def __init__(self,x,y,r,g,img,w,h,F):
        Soldier.__init__(self,x,y,r,g,img,w,h,F)
        self.dir = 1
        self.ddir = 1
        self.cy = 90
        self.wl = walk_list7

class Soldier8(Soldier):
    def __init__(self,x,y,r,g,img,w,h,F):
        Soldier.__init__(self,x,y,r,g,img,w,h,F)
        self.cy = 90
        self.wl = walk_list8

class Soldier9(Soldier):
    def __init__(self,x,y,r,g,img,w,h,F):
        Soldier.__init__(self,x,y,r,g,img,w,h,F)
        self.cy = 90
        self.wl = walk_list9        

class Ball(Creature):
    def __init__(self,x,y,r,g,img,w,h,F):
        Creature.__init__(self,x,y,r,g,img,w,h,F)
        self.vx = -5
        self.ttl = 60
        self.bomb = musicplayer.loadFile(path+"/sounds/bomb.wav")
        
    def display(self):
        self.ttl -= 1 #fire ball disappears after one sec
        self.gravity()
        self.f = (self.f+0.3)%self.F    
        self.x += self.vx
        self.y += self.vy
        image(self.img,self.x-self.w//2-g.x,self.y-self.h//2,self.w,self.h,978+int(self.f)*self.w,873,978+int(self.f+1)*self.w,873+self.h)
        
        if self.distance(g.player) < self.r + g.player.r and g.player.dead == False and not g.player.rampage:#kill the player
            self.bomb.rewind()
            self.bomb.play()
            g.player.dead = True
            g.ball.remove(self)
            del self  
    
    def distance (self,e):
        return ((self.x-e.x)**2+(self.y-e.y)**2)**0.5

class Mine(Creature):
    def __init__(self,x,y,r,g,img,w,h,F):
        Creature.__init__(self,x,y,r,g,img,w,h,F)
        self.vx = -5
        self.vy = -10
        self.bomb = musicplayer.loadFile(path+"/sounds/bomb.wav")
    def display(self):
        self.update()
        image(self.img,self.x-self.w//2-g.x,self.y-self.h//2,self.w,self.h,mine[int(self.f)][0],855,mine[int(self.f)][0]+mine[int(self.f)][1],855+self.h)
        
        if self.distance(g.player) < self.r + g.player.r and g.player.dead == False and not g.player.rampage:#kill the player
            self.bomb.rewind()
            self.bomb.play()
            g.player.dead = True
            image(g.one,self.x-self.r-g.x,self.y-self.r,self.w,self.h,336,310,384,407)
            g.mine.remove(self)
            del self 
    
    def update(self):
        for i in platform[g.mission-1]:#mines explode and disappear when touching the ground
            if self.x in range(i[0],i[1]) and self.y+self.r <= i[2]:
                self.g = i[2]
                break
            else:
                self.g = g.g
        if self.vx != 0:
            self.f = (self.f+0.3)%self.F    
        
        self.vy += 0.6
        self.x += self.vx
        self.y += self.vy
        
    def distance (self,e):
        return ((self.x-e.x)**2+(self.y-e.y)**2)**0.5 

class Grenade(Mine):
    def __init__(self,x,y,r,g,img,w,h,F,dir):
        Mine.__init__(self,x,y,r,g,img,w,h,F)
        self.dir = dir
        self.vx = 10*self.dir
        self.vy = -8
    def display(self):
        self.update()
        image(self.img,self.x-self.w//2-g.x,self.y-self.h//2,self.w,self.h,grenade[int(self.f)][0],grenade[int(self.f)][1],grenade[int(self.f)][2],grenade[int(self.f)][3])
        
        for e in g.soldier:#kill the enemies
            if self.distance(e) < self.r + e.r and e.dead == False:
                e.dead = True
                self.bomb.rewind()
                self.bomb.play()
                image(g.one,self.x-self.r*5-g.x,self.y-self.r*10,self.w*5,self.h*5,336,310,384,407)
                g.grenade.remove(self)

class Fire(Creature):
    def __init__(self,x,y,r,g,img,w,h,F,vx,ttl):
        Creature.__init__(self,x,y,r,g,img,w,h,F)
        self.vx = vx
        self.dir = vx
        self.ttl = ttl*60
        
    def update(self):
        self.ttl -= 1
        self.x += self.vx
        
        for s in g.soldier:#kill the enemies
            if self.distance(s) < self.r + s.r and s.dead == False:
                s.dead = True
                g.player.killCnt += 1
                g.player.fire.remove(self)
                return
              
    def distance (self,e):
        return ((self.x-e.x)**2+(self.y-e.y)**2)**0.5

class Water(Creature):
    def __init__(self,x,y,r,g,img,w,h,F):
        Creature.__init__(self,x,y,r,g,img,w,h,F)
        
    def display(self):
        image(self.img,self.x-self.w//4-g.x,self.y-self.h//4,self.w//2,self.h//2,14,6,14+self.w,6+self.h)

class Game:
    def __init__(self,w,h,g,m,state='menu',life=3):
        self.w=w
        self.h=h
        self.g=g
        self.x=0
        self.mission=m
        self.life = life
        self.player=Player(50,50,16,self.g,'1.png',32,40,9,self.life)
        self.soldier=[]
        self.a=30#to control the message of completion appearing time
        self.grenade=[]
        self.mine=[]
        self.ball=[]
        self.water=[]
        self.mainMusic=musicplayer.loadFile(path+"/sounds/"+str(self.mission)+".mp3")
        self.winSound = musicplayer.loadFile(path+"/sounds/win.mp3")
        
        #distribution of enemies and objects in three missions respectively
        if self.mission==1:
            self.append() 
        elif self.mission==2:
            self.append()
            self.water.append(Water(240,105,15,self.g,'water.png',55,37,1)) 
        elif self.mission==3:
            self.append()
            self.water.append(Water(1300,50,12,self.g,'water.png',55,37,1)) 
        self.one=loadImage(path+"/images/1.png")
        self.two=loadImage(path+"/images/2.gif")
        self.bg1=loadImage(path+"/images/bg1.png")
        self.bg2=loadImage(path+"/images/bg2.png")
        self.bg3=loadImage(path+"/images/bg3.png")
        self.sky1=loadImage(path+"/images/sky.png")
        self.goimg=loadImage(path+"/images/gameover.png")
        self.winimg=loadImage(path+'/images/win.jpeg')
        self.state=state
        
        
    def append(self):
        f = open(path+"/soldierlevel.csv","r")
        for l in f:
            l = l.strip().split(",")
            if l[0]==str(self.mission):
                if l[1]=="Soldier":
                    self.soldier.append(Soldier(int(l[2]),int(l[3]),15,self.g,'soldier.png',35,38,5))
                elif l[1]=="Soldier1":
                    self.soldier.append(Soldier1(int(l[2]),int(l[3]),16,self.g,'soldier.png',35,48,12,int(l[4]),int(l[5])))
                elif l[1]=="Soldier2":
                    self.soldier.append(Soldier2(int(l[2]),int(l[3]),16,self.g,'soldier.png',35,43,10))
                elif l[1]=="Soldier3":
                    self.soldier.append(Soldier3(int(l[2]),int(l[3]),16,self.g,'soldier.png',35,48,18))
                elif l[1]=="Soldier4":
                    self.soldier.append(Soldier4(int(l[2]),int(l[3]),16,self.g,'soldier.png',35,45,5,int(l[4]),int(l[5])))
                elif l[1]=="Soldier5":
                    self.soldier.append(Soldier5(int(l[2]),int(l[3]),15,self.g,'soldier.png',35,43,4))
                elif l[1]=="Soldier6":
                    self.soldier.append(Soldier6(int(l[2]),int(l[3]),16,self.g,'soldier.png',35,43,8,int(l[4]),int(l[5])))
                elif l[1]=="Soldier7":
                    self.soldier.append(Soldier7(int(l[2]),int(l[3]),15,self.g,'soldier.png',35,40,4))
                elif l[1]=="Soldier8":
                    self.soldier.append(Soldier8(int(l[2]),int(l[3]),15,self.g,'soldier.png',35,40,4))
                elif l[1]=="Soldier9":
                    self.soldier.append(Soldier9(int(l[2]),int(l[3]),15,self.g,'soldier.png',35,40,4))
        
    def display(self):
        if self.mission==1:
            #loop the sky and the background
            image(self.sky1,0,0,self.w-self.x+1,132,self.x-1,0,self.w,113)
            image(self.sky1,self.w-self.x,0,self.x,132,0,0,self.x,113)     
            image(self.bg1,0,70,self.w,120,9+self.x,580,self.w+self.x,671)
            image(self.bg1,0,0,self.w,230,7+self.x,0,self.w+self.x,230)
            image(self.bg1,1862-self.x,0,336,230,1500,4,1836,230)
            
            self.show()
            #reach the completion gate
            if self.player.x>=3518:
                fill(255,0,0)
                textSize(60)
                if self.a>0:
                    text("MISSION1 COMPLETED!",215,130)       
                    self.a -= 1     
                else:
                    self.mainMusic.pause()  # stop the music of current mission
                    self.__init__(1000,230,190,2,'play',life=g.player.life)
       
        elif self.mission==2:
            #background
            image(self.bg2,0,0,self.w,self.h,self.x,0,self.w+self.x,220)   
            
            self.show()
            #completion gate
            if self.player.x>=3463:
                fill(255,0,0)
                textSize(60)
                if self.a>0:
                    text("MISSION2 COMPLETED!",215,130)       
                    self.a -= 1     
                else:
                    self.mainMusic.pause()
                    g.__init__(1000,230,165,3,'play',life=g.player.life)       
        
        elif self.mission==3:
            #background
            image(self.bg3,0,0,self.w,self.h,7+self.x,0,self.w+self.x,231)
            
            self.show()
            #completion gate
            if self.player.x>=2540:
                fill(255,0,0)
                textSize(60)
                if self.a>0:
                    text("ALL MISSIONS COMPLETED!",140,130)       
                    self.a -= 1     
                else:
                    self.state='win'
                    self.mainMusic.pause()
                
        
        image(loadImage(path+"/images/heart.png"),20,20,36,36,0,0,720,720)  # display number of lives
        fill(255)
        textSize(25)
        text('X '+str(self.player.life),60,45)
        
        strokeWeight(2)  # the bar shows when rampage can be activated
        fill(255,0,0)
        rect(280,26,100,20)
        fill(255,255,0)
        rect(280,26,min(100,20*self.player.killCnt),20)
        fill(255)
        textSize(25)
        text('RAMPAGE',150,45)
    
    def show(self):
        #display everything that should be in the game
        self.player.display()
        for f in self.player.fire:
            f.display()
            if f.ttl <= 0 and f in self.player.fire:
                self.player.fire.remove(f)
        for w in self.water:
            w.display()
        for s in self.soldier:
            s .display()
        for b in self.ball:
            b.display()
            if b.ttl <= 0 and b in self.ball:
                self.ball.remove(b)
        for g in self.grenade:
            g.display()
            if g.y+g.r > g.g:
                g.bomb.rewind()
                g.bomb.play()
                self.grenade.remove(g)
                image(self.one,g.x-g.r*4-self.x,g.y-g.r*10,g.w*5,g.h*5,3,408,53,506)
        for m in self.mine:
            m.display()
            if m.y+m.r > m.g and m in self.mine:
                image(self.one,m.x-m.r-self.x,m.y-m.r,m.w,m.h,336,310,384,407)
                self.mine.remove(m)
            
        
g = Game(1000,230,190,1)

def setup():
    size(g.w,g.h)
    background(0)
    
def draw():
    if g.state == "menu":  # contents of the main menu
        background(0)
        textSize(30)
        
        if g.w//2.5< mouseX < g.w//2.5 + 180 and g.h//4 < mouseY < g.h//4+30:
            fill(255,0,0)
        else:        
            fill(255)
        text("Play Game",g.w//2.5+10, g.h//3+8)

        if g.w//2.5 < mouseX < g.w//2.5 + 180 and g.h//3+60 < mouseY < g.h//3+90:
            fill(255,0,0)
        else:        
            fill(255)
        text("Instructions", g.w//2.5, g.h//3+85)
    
    elif g.state == 'instruction':  # three options are available at instruction page
        background(0)
        fill(0,0,255)
        textSize(25)
        fill(255)
        
        if 130 < mouseX < 310 and g.h//2.5 < mouseY < g.h//2.5+30:  
            fill(255,0,0)
        else:
            fill(255)
        text("Briefing",170,g.h//2.5+25)
        if 422 < mouseX < 602 and g.h//2.5 < mouseY < g.h//2.5+30:  
            fill(255,0,0)
        else:
            fill(255)
        text("Enemy Info",462,g.h//2.5+25)
        if 700 < mouseX < 880 and g.h//2.5 < mouseY < g.h//2.5+30: 
            fill(255,0,0)
        else:
            fill(255)
        text("Control",740,g.h//2.5+25)
        
        if g.w//2-40 < mouseX < g.w//2 + 95 and g.h//3+100 < mouseY < g.h//3+125:
            fill(255,0,0)
        else:
            fill(255)
        text("Back",g.w//2-10, g.h//3+122)
    
    elif g.state == 'control':
        background(0)
        textSize(20)
        fill(255)
        text("Fire: Space",g.w//3, g.h//3+10)
        text("Activate Rampage: R",g.w//3, g.h//3+30)
        text("Grenade: F",g.w//3, g.h//3+50)
        text("Movement: UP LEFT RIGHT",g.w//3, g.h//3+70)
        
        if g.w//2-40 < mouseX < g.w//2 + 95 and g.h//3+100 < mouseY < g.h//3+125:
            fill(255,0,0)
        else:
            fill(255)
        text("Back",g.w//2-10, g.h//3+122)
    
    elif g.state == 'brief':
        background(0)
        textSize(20)
        fill(255)
        text('''You start with three lives, water bottle adds one life. 
             There are three missions in this game.''',g.w//4, g.h//3+10)
        
        if g.w//2-40 < mouseX < g.w//2 + 95 and g.h//3+100 < mouseY < g.h//3+125:
            fill(255,0,0)
        else:
            fill(255)

        text("Back",g.w//2-10, g.h//3+122)
    
    elif g.state == 'info':
        background(0)
        textSize(13)
        fill(255)
        text('''Soldier:  scout soldier(stand still looking around)
Soldier1: patrol soldier(walk around in  a certain area)
Soldier2: mine soldier(roll the fire ball on the ground)
Soldier3: artillery soldier(fire a shell)
Soldier4: frog soldier(jump in a certain area)
Soldier5: timid soldier(hiding behind a wall)
Soldier6: mad soldier(run in a certain area with speed increased)
Soldier7,8,9:talking soldier(stand still chatting)''',g.w//3, g.h//8)
        
        if g.w//2-40 < mouseX < g.w//2 + 95 and g.h//3+100 < mouseY < g.h//3+125:
            fill(255,0,0)
        else:
            fill(255)
        textSize(20)
        text("Back",g.w//2-10, g.h//3+122)
        
    elif g.state == "play":
        background(0)
        g.display()
        g.mainMusic.play()
            
    elif g.state == 'gameover':
        image(g.goimg,0,0,g.w,g.h)  
        g.player.gameoverSound.play()
        g.mainMusic.pause() 
        textSize(20)
        fill(255)
        text('Press Enter to restart',200,200)
    
    elif g.state == 'win':
        g.mainMusic.pause()
        g.winSound.play()
        image(g.winimg,0,0,250,230,0,0,713,724)
        image(g.winimg,250,0,250,230,0,0,713,724)
        image(g.winimg,500,0,250,230,0,0,713,724)
        image(g.winimg,750,0,250,230,0,0,713,724)
        
        
def mouseClicked():
    if g.state == "menu" and g.w//2.5< mouseX < g.w//2.5 + 180 and g.h//4 < mouseY < g.h//4+30:
        g.state="play"
    elif g.state == "menu" and g.w//2.5 < mouseX < g.w//2.5 + 180 and g.h//3+60 < mouseY < g.h//3+90:
        g.state='instruction'
    elif g.state == 'instruction' and g.w//2-40 < mouseX < g.w//2 + 95 and g.h//3+100 < mouseY < g.h//3+125:
        g.state='menu'
    elif g.state == 'instruction' and 700 < mouseX < 880 and g.h//2.5 < mouseY < g.h//2.5+30: 
        g.state = 'control'
    elif g.state == 'instruction' and 422 < mouseX < 602 and g.h//2.5 < mouseY < g.h//2.5+30:
        g.state = 'info'
    elif g.state == 'instruction' and 130 < mouseX < 310 and g.h//2.5 < mouseY < g.h//2.5+30: 
        g.state = 'brief'
    elif g.state == 'control' and g.w//2-40 < mouseX < g.w//2 + 95 and g.h//3+100 < mouseY < g.h//3+125:
        g.state = 'instruction'
    elif g.state == 'info' and g.w//2-40 < mouseX < g.w//2 + 95 and g.h//3+100 < mouseY < g.h//3+125:
        g.state = 'instruction'
    elif g.state == 'brief' and g.w//2-40 < mouseX < g.w//2 + 95 and g.h//3+100 < mouseY < g.h//3+125:
        g.state = 'instruction'
        
    
        
        
def keyPressed():
    if keyCode == LEFT:
        g.player.keyHandler[LEFT]=True
    elif keyCode == RIGHT:
        g.player.keyHandler[RIGHT]=True
    elif keyCode == UP:
        g.player.keyHandler[UP]=True
    elif keyCode == DOWN:
        g.player.keyHandler[DOWN]=True
    elif keyCode == 32 and not g.player.dead and not g.player.rampage and not g.player.water:
        g.player.fire.append(Fire(g.player.x+g.player.dir*g.player.r+8,g.player.y-8,12,g.player.g,"f.png",25,10,1,g.player.dir*20,0.2))
        g.player.ofire = True
    elif keyCode == 70 and not g.player.dead and not g.player.rampage and not g.player.water:
        g.grenade.append(Grenade(g.player.x+g.player.dir*g.player.r+8,g.player.y-12,8,g.player.g,"1.png",20,20,8,g.player.dir))
        g.player.grenade = True   
    elif keyCode == 82 and g.player.killCnt >= 5:
        g.player.rampage = True 
        g.player.rampagetime = 30
        g.player.killCnt = 0
    elif keyCode == 10 and g.state=='gameover': 
        g.__init__(1000,230,190,1)
        
        
def keyReleased():
    if keyCode == LEFT:
        g.player.keyHandler[LEFT]=False
    elif keyCode == RIGHT:
        g.player.keyHandler[RIGHT]=False
    elif keyCode == UP:
        g.player.keyHandler[UP]=False
    elif keyCode == DOWN:
        g.player.keyHandler[DOWN]=False 
    elif keyCode == 32:
        g.player.ofire = False
    elif keyCode == 70:
        g.player.grenade = False
