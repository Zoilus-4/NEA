import os
import sys
if "M:/Python Packages" not in sys.path:
    sys.path.append("M:/Python Packages")
import pygame, time, random, math, ctypes
import math as m
import random

pygame.init()

user32 = ctypes.windll.user32
def draw_text(screen, x, y, size, colour, message):
    font = pygame.font.SysFont("Verdana Bold", size)
    image = font.render(message, True, colour)
    screen.blit(image, (x, y))

W = user32.GetSystemMetrics(0) # window width
H = user32.GetSystemMetrics(1) # window height


screen = pygame.display.set_mode((W,H))#sets screen bounds
pygame.display.set_caption("Одна часть существует")
WHITE = (255,255,255)
BLACK = (0,0,0)

def dist(a,b):
    return math.sqrt( ( a[0] - b[0] ) ** 2 + ( a[1] - b[1] ) ** 2 )

clock = pygame.time.Clock()
class CirclePrototypes():#circles class
    def __init__ (self, colour, initpos, radius):
        self.xpos = initpos[0]
        self.ypos = initpos[1]
        self.colour = colour
        self.radius = radius
        self.collided = 0
        number = random.randint(1,2)
        if number == 1:
            self.fissile = True
        else:
            self.fissile = False
    def distcalc(self, otherx, othery):#gets distance between self and something else
        a = (self.xpos - otherx)**2
        b = (self.ypos - othery)**2
        c = math.sqrt(a + b)
        return c
    def draw(self, screen):#draws it on the screen
        pygame.draw.circle(screen, self.colour, (self.xpos, self.ypos), self.radius)
class Neutron(CirclePrototypes):#subclass of circles, for neutrons and other "movers"
    def __init__ (self, colour, initpos, radius, lowtime, uptime):
        CirclePrototypes.__init__(self, colour, initpos, radius)
        self.angle = random.uniform(0, 2*math.pi)
        self.timer = random.randint(lowtime, uptime)#time before neutron vanishes
        self.mag = 10#size of movement vector 
    def move(self):
        if speedscalar != 0:
            self.xpos += (self.mag * math.cos(self.angle)) #determines motion
            self.ypos += (self.mag * math.sin(self.angle))
def Operations(item, nuc, newtlist, chunklist, NEUTRON_SIZE, SUB_SIZE): #subroutine for interactions betwixt neutrons and nuclei
    global interact_count
    global total_count
    global speedscalar
    dist = item.distcalc(nuc.xpos, nuc.ypos)
    if nuc.radius == NO_RADIUS:
        o = 1
    elif dist < item.radius + nuc.radius and nuc.fissile == True and item.radius != 15:
        #item.isinteract = 1
        chunklist[currentchunk[0]][currentchunk[1]].remove(nuc) #removes nucleus from its chunk list
        flipper = 0 #flipper variable ensures both outcomes occur within both loops
        
        for i in range(2):
            
            neutron = Neutron((255, 0, 255), [nuc.xpos, nuc.ypos], NEUTRON_SIZE, LOWER_TIME, UPPER_TIME)#instances Neutron class to add to the main loop
            if flipper == 0:
                
                neutron.angle = item.angle + ((math.pi)/8)
                flipper = 1
            else:
                neutron.angle = item.angle - ((math.pi)/8)
                flipper = 0
            neutron.mag *= speedscalar
            newtlist.append(neutron)#adds to neutron list to be drawn
            submunition1 = Neutron((0, 120, 255), [nuc.xpos, nuc.ypos], SUB_SIZE, LOWER_TIME, UPPER_TIME) #make use of Neutron class but are actually remnants from fission reactions
            submunition1.mag = 3 * speedscalar
            submunition1.timer = 25 
            if flipper == 0:
                
                submunition1.angle = item.angle + (math.pi/2)
            else:
                submunition1.angle = item.angle - (math.pi/2)
                
            newtlist.append(submunition1)
        interact_count += 1
        total_count += 1#for the energy meter later in the code
        pygame.draw.circle(screen, (255,76,0), [item.xpos,item.ypos],100)#rudimentary explosion sfx
        if item in newtlist:
            newtlist.remove(item)
        #return 0
    elif dist < item.radius + nuc.radius and nuc.fissile == False: #for turning non-fissile into fissile
        #item.isinteract = 1
        nuc.fissile = True
        nuc.colour = (0, 255, 130)#change in colour to show fissile-ness
        try:
            #pygame.draw.circle(screen, (255,76,0), [item.xpos,item.ypos],100)
            newtlist.remove(item)
        except:
            pass               
class Control_Rod(): #class for making control rods
    def __init__(self, height):
        self. width = W/20
        self.height = height
        self.ypos = H/4
        self.xpos = (W/2)
        self.radius = NO_RADIUS #basically a unique identifier to make sure it gets ignored in any radius calculations (since it is a rectangle)
    def draw(self, screen):
        pygame.draw.rect(screen, (0, 0, 255), pygame.Rect((self.xpos - self.width/2), 0, self.width, self.height))
def Tutorial_Message():
    draw_text(screen, W - 320, H/6 + 5, 40, (255, 255, 0), "Tutorial")
    draw_text(screen, W - 320, H/6 + 40, 30, (255, 255, 255), "0 to add rod")
    draw_text(screen, W - 320, H/6 + 60, 30, (255, 255, 255), "1 to remove rod")
    draw_text(screen, W - 320, H/6 + 80, 30, (255, 255, 255), "left arrow to slow time")
    draw_text(screen, W - 320, H/6 + 100, 30, (255, 255, 255), "right arrow to speed up time")
    draw_text(screen, W - 320, H/6 + 120, 30, (255, 255, 255), "down arrow to lower all rods")
    draw_text(screen, W - 320, H/6 + 140, 30, (255, 255, 255), "up arrow to raise all rods")
    draw_text(screen, W - 320, H/6 + 160, 30, (255, 255, 255), "P to pause/unpause")
    draw_text(screen, W - 320, H/6 + 180, 30, (255, 255, 255), "BKSP to exit to menu")
interact_count = 0 #this entire column is relevant variables for use in the main loop
average = 0
NO_RADIUS = 5000000
leftmove = 1
rightmove = 1
LOWER_TIME = 100
UPPER_TIME = 300
NEUTRON_SIZE = 7
SUB_SIZE = 15
NUCLEUS_SIZE = 25
flipper = 0
fps = 60
play = False
preplay = True
xpos = 10
ypos = 10
timer = 0
temp = 0
secondx = W/2
secondy = H/2
newtlist = []
nuclist = []
czechx = []
czechy = []
chunkW = W/7
chunkH = H/7
chunklist = []
control_list = []
moving_average = []
goingup = False
goingdown = False
speedscalar = 1

while preplay:
    if play == False:
        screen.fill((0, 35, 35))
        draw_text(screen, W/6, H/2, 50, (255, 255, 255), "PRESS SPACE TO START THE SIMULATION, OR PRESS ESC TO EXIT")
        pygame.draw.circle(screen, (255, 0, 0), (W/8, H/6), 25)
        pygame.draw.circle(screen, (0, 255, 130), (W/8 + 75, H/6), 25)
        pygame.draw.circle(screen, (0, 255, 0), (W/8 + 150, H/6), 25)  
        pygame.draw.circle(screen, (255, 0, 255), (W/8 + 225, H/6), 7)
        pygame.draw.rect(screen, (0, 0, 255), pygame.Rect((W/8 - 105), H/6 - 25, 50, 50))
        draw_text(screen, W/8 - 20, H/6 + 35, 20, (255, 255, 255), "U-238")
        draw_text(screen, W/8 + 55, H/6 + 35, 20, (255, 255, 255), "Pu-239")
        draw_text(screen, W/8 + 130, H/6 + 35, 20, (255, 255, 255), "U-235")
        draw_text(screen, W/8 + 200, H/6 + 35, 20, (255, 255, 255), "Neutron")
        draw_text(screen, W/8 - 117, H/6 + 35, 20, (255, 255, 255), "Control Rod")
        Tutorial_Message()
        
    for event in pygame.event.get():

        
        if event.type == pygame.KEYDOWN and event.key ==pygame.K_SPACE:
            play = True
            interact_count = 0 #this entire column is relevant variables for use in the main loop
            average = 0
            NO_RADIUS = 5000000
            leftmove = 1
            rightmove = 1
            LOWER_TIME = 100
            UPPER_TIME = 300
            NEUTRON_SIZE = 7
            SUB_SIZE = 15
            NUCLEUS_SIZE = 25
            flipper = 0
            fps = 60
            xpos = 10
            ypos = 10
            timer = 0
            temp = 0
            secondx = W/2
            secondy = H/2
            newtlist = []
            nuclist = []
            czechx = []
            czechy = []
            chunkW = W/7
            chunkH = H/7
            chunklist = []
            control_list = []
            moving_average = []
            goingup = False
            goingdown = False
            speedscalar = 1
            holding_var = 1
            total_count = 0
            for i in range(7):
                chunklist.append([[],[],[],[],[],[],[]]) #instantiation of the chunk list 
            i = 0
            control = Control_Rod(H/2)
            control_list.append(control) #adds to the control rod list with a control rod
            while i < 50:
                nucleus = CirclePrototypes((0, 255, 0), [random.randint(50, W-25), random.randint(25, H-25)], NUCLEUS_SIZE) #this block sets up 50 initial nuclei 
                if nucleus.fissile == False:
                    nucleus.colour = (255, 0, 0)
                if nucleus.xpos not in czechx and nucleus.ypos not in czechy:
                    
                    chunklist[int(nucleus.xpos//chunkW)-1][int(nucleus.ypos//chunkH)-1].append(nucleus)
                    czechx.append(nucleus.xpos)
                    czechy.append(nucleus.ypos)
                    i += 1
                
            for i in range(0, 50):   
                neutron = Neutron((255, 0, 255), [random.randint(25, W), random.randint(1, H)], NEUTRON_SIZE, LOWER_TIME, UPPER_TIME) #This is 50 initial neutrons for debugging
                newtlist.append(neutron)

    
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            preplay = False
            play = False    
    while play:#main loop
        
        screen.fill((0, 35, 35))
         
        for event in pygame.event.get():
            if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                play = False
                preplay = False# SPACE shuts down program
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_BACKSPACE:
                play = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_0 and len(control_list) <= 6: #allows for adding control rods
                if flipper == 0: #flipper variable here to ensure that the rods appear on alternating sides
                    if len(control_list) > 0:
                        new_cont = Control_Rod(control_list[0].height)
                    else:
                        new_cont = Control_Rod(H/2)
                    
                    
                    new_cont.xpos -= ((W/8) * leftmove)
                    control_list.append(new_cont)
                    flipper = 1
                    leftmove += 1
                else:
                    if len(control_list) > 0:
                        new_cont = Control_Rod(control_list[0].height)
                    else:
                        new_cont = Control_Rod(H/2)
                    new_cont.xpos += ((W/8) * rightmove)
                    control_list.append(new_cont)
                    flipper = 0
                    rightmove += 1
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_n and len(newtlist) == 0:
                substitute = Neutron((255, 0, 255), [random.randint(25, W), random.randint(1, H)], NEUTRON_SIZE, LOWER_TIME, UPPER_TIME)
                substitute.mag *= speedscalar
                newtlist.append(substitute)
                 
                
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_1 and len(control_list) != 0:#allows for removing control rods
                control_list.pop(-1)
                #if len(control_list) == 0:
                if flipper == 0:
                    rightmove -= 1
                    flipper = 1
                else:
                    leftmove -= 1
                    flipper = 0
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_UP:
                if goingdown:
                    goingdown = False
                else:
                    goingup = True
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN:
                if goingup:
                    goingup = False
                else:
                    goingdown = True
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_LEFT:
                if speedscalar >= 0.25:
                    speedscalar *= 0.5
                for item in newtlist:
                    item.mag = 10 * speedscalar 
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT:
                if speedscalar <= 8:
                    speedscalar *= 2
                for item in newtlist:
                    item.mag = 10 * speedscalar
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_p:
                if speedscalar != 0:
                    holding_var = speedscalar
                    speedscalar = 0
                    
                else:
                    speedscalar = holding_var
            
                    
                """if LOWER_TIME >= 5 and UPPER_TIME >= 205:
                    LOWER_TIME -= 10
                    UPPER_TIME -= 10
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_1:
                if LOWER_TIME <= 500 and UPPER_TIME <= 700:
                    LOWER_TIME += 10
                    UPPER_TIME += 10"""
        #colour = (50, (xpos/W) * 255, (ypos/H)*255) 
      
        clock.tick(fps) #makes the clock tick according to the fps
        screen.fill((0, 35, 35))
        for item in control_list:
            if goingup and item. height >= 5:
                item.height -= 5 * speedscalar
                item.ypos -= 5 * speedscalar
            elif goingdown and item.height < H:
                item.height += 5 * speedscalar
                item.ypos += 5 * speedscalar
        for item in newtlist: # this block is where all the neutron stuff happens, be it movement or interactions
            item.draw(screen)
            item.move()
            if item.xpos >= W:#this part makes the neutrons loop across the screen at boundaries
                item.xpos = 26
            if item.xpos <= 25:
                item.xpos = W-1
            if item.ypos >= H:
                item.ypos = 1
            if item.ypos <= 0:
                item.ypos = H-1
            currentchunk = [int(item.xpos // chunkW)-1, int(item.ypos // chunkH)-1]
            for i in range(-1,2):
                for j in range(-1,2):
                    try:
                        for nuc in chunklist[currentchunk[0]+i][currentchunk[1]+j]:
                            #if not item.isinteract:
                            Operations(item, nuc, newtlist, chunklist, NEUTRON_SIZE, SUB_SIZE)
                    except ValueError:
                        pass
            for cont in control_list: #this makes the control rods 'eat' the neutrons if they come in contact
                if item.xpos < (cont.xpos+(cont.width/2)):
                    if item.xpos > (cont.xpos - (cont.width/2)) and item.ypos < (cont.height):
                                                                           
                        try:
                            newtlist.remove(item)
                        except:
                            pass
            item.timer -= 1 * speedscalar
            if item.timer <= 0:
                for i in range(4): #manages the creation of 4 new nuclei for every neutron that 'dies'. It attempts to place them in areas where there aren't some already. 
                    try:
                        newtlist.remove(item)
                    except:
                        pass
                    if item.radius != 15:
                        for i in range(2):
                            X = random.randint(50, W-25)
                            Y = random.randint(25, H-25)
                            c = 0
                            while 1:
                                c += 1
                                done = True
                                for i in range(3):
                                    for u in range(3):
                                        try:
                                            for n in chunklist[int(X//chunkW)-1+(i-1)][int(Y//chunkH)-1+(i-1)]:
                                                if (n.xpos-X)**2 + (n.ypos-Y)**2 < 625: done = False
                                        except:
                                            done = False
                                if done: break
                                X = random.randint(50, W-25)
                                Y = random.randint(25, H-25)
                                if c >= 25: break
                                            
                            nucleus = CirclePrototypes((0, 255, 0), [X, Y], 25)
                            if nucleus.fissile == False:
                                nucleus.colour = (255, 0, 0)
                        
                    
                            chunklist[int(nucleus.xpos//chunkW)-1][int(nucleus.ypos//chunkH)-1].append(nucleus)
        for item in chunklist:#the grand drawing piece, which also removes and replaces nuclei if they're caught under a control rod.
            for thing in item:
                for chose in thing:
                    if len(control_list)!= 0:
                        for cont in control_list:
                            if chose.xpos < (cont.xpos+(cont.width/2)):
                                if chose.xpos > (cont.xpos - (cont.width/2)) and chose.ypos < (cont.height):
                                    thing.remove(chose)
                                    nucleus = CirclePrototypes((0, 255, 0), [random.randint(50, W-25), random.randint(25, H-25)], 25)
                                    if nucleus.fissile == False:
                                        nucleus.colour = (255, 0, 0)
            
                                    chunklist[int(nucleus.xpos//chunkW)-1][int(nucleus.ypos//chunkH)-1].append(nucleus)
                                
                                else:
                                    chose.draw(screen)
                            else:
                                
                                chose.draw(screen)
                    else:
                        chose.draw(screen)
        for item in control_list:
            item.draw(screen)
        #if len(newtlist) > 150:
        #    newtlist.pop(0)
        if len(newtlist) == 0:
            #newtlist.append(Neutron((255, 0, 255), [random.randint(25, W), random.randint(1, H)], NEUTRON_SIZE, LOWER_TIME, UPPER_TIME)) # for debug, makes a new neutron if there are none left
            draw_text(screen, W/4, H/2, 50, (255, 255, 255), "REACTION HALTED - PRESS N FOR NEW NEUTRON")
        if speedscalar == 0:
            draw_text(screen, W/2 - 67, H/2, 50, (255, 255, 255), "PAUSED")
            string = ("Energy Released: "+ str(total_count*200)+ "MeV")
            draw_text(screen, W - 450, 50, 40, (255, 255, 0), (string))
            Tutorial_Message()
            
        
        timer += 1
        if speedscalar != 0:
            if timer >= (5 / speedscalar):
                moving_average.append(interact_count) # handling of moving average for the energy meter
                interact_count = 0
                timer = 0
        if len(moving_average) > 60:
            while len(moving_average) > 60 and speedscalar != 0:
                moving_average.pop(0) #makes the moving average, well, move
            
        
        for item in moving_average:
            temp += int(item)
        try:
            average = temp / len(moving_average)
        except:
            pass
        """if average > 75:
            screen.fill((255,76,76))
            time.sleep(10)
            exit()"""
        temp = 0 # resets temp
        pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(0, 0, 25, H))#makes a black rectangle on the leftmost side of the screen to ensure no UI overlap.
        #print(moving_average)
        if (average) >= 10:
            pygame.draw.rect(screen, (255, 0, 0),pygame.Rect(0, H - average * 50, 25, (average * 50)+5))#this little section manages the creation, size, and colour of the energy meter based on the moving average.
            if average * 50 >= H:
                screen.fill((225, 76, 0))
                draw_text(screen, W/3 +80, H/2, 50, (255, 255, 255), "! NUCLEAR CATASTROPHE !")
                pygame.display.update()
                time.sleep(5)
                play = False
        elif (average) <= 1:
            pygame.draw.rect(screen, (0, 255, 200),pygame.Rect(0, H - average * 50, 25, (average * 50)+5))
        else:
            pygame.draw.rect(screen, (255, 125, 125),pygame.Rect(0, H - average * 50, 25, (average * 50)+5))
        pygame.draw.rect(screen, (255, 255, 255), pygame.Rect(22, 0, 3, H))

            
        pygame.display.update()
    pygame.display.update()
#time.sleep(5)
pygame.quit()
