import math
import random
import numpy as np
import pygame
import program

pygame.init()

display_width = 800
display_height = 640
ship_size = display_width/100
center = (int(display_width/2),int(display_height/2))

black = (0,0,0)
white = (255,255,255)
green = (0, 200, 0)
red = (200,0,0)
yellow = (0,150,150)
blue = (0,0,150)

gameDisplay = pygame.display.set_mode((display_width,display_height))
pygame.display.set_caption("Ship Game")
gameDisplay.fill(green)
pygame.display.update()
clock = pygame.time.Clock()
clock.tick(15)

class Ship:
    def __init__(self, name, position, velocity, acceleration, drag, fire_range, hp):
        self.name = name
        self.position = position
        self.velocity = velocity
        self.acceleration = acceleration
        self.drag = drag
        self.fire_range = fire_range
        self.hp = hp
        

    def spawn(self):
        self.position = [math.floor((random.random()*2-0.5)*100),math.floor((random.random()*2-0.5)*100)]
        self.velocity = [math.floor((random.random()*2-0.5)*10),math.floor((random.random()*2-0.5)*10)]
        self.acceleration = [math.floor((random.random()*2)-0.5),math.floor((random.random()*2)-0.5)]
        
    def turn(self, move):
        
        if (move == 1):
            self.acceleration[0] -= 1
            self.acceleration[1] -= 1
        elif (move == 2):
            self.acceleration[1] -= 1
        elif (move == 3):
            self.acceleration[0] += 1
            self.acceleration[1] -= 1
        elif (move == 4):
            self.acceleration[0] -= 1            
        elif (move == 6):
            self.acceleration[0] += 1
        elif (move == 7):
            self.acceleration[0] -= 1
            self.acceleration[1] += 1
        elif (move == 8):
            self.acceleration[1] += 1
        elif (move == 9):
            self.acceleration[0] += 1
            self.acceleration[1] += 1
    

    def move(self):
        for i in range(2):
            self.velocity[i] += self.acceleration[i]-math.trunc(self.velocity[i]*self.drag)
            self.position[i] += self.velocity[i]

        
def init_ships(p1,e,e_num):
#Define player start position, velocity and acceleration
    p1.spawn()

#Define enemy start position, velocity and acceleration
    for i in range(e_num):
        name = "enemy_{}"
        e.append(Ship(name.format(i),0,0,0, 0.1,0, 3))
        e[i].spawn()
    print(len(e))

def init_planet(radius,circle):
    newarray=pygame.PixelArray(circle)
    for i in range(2*radius):
        for j in range(2*radius):
            #print(i,"   ",j)
            I=i-radius
            J=j-radius
            c = int(255*(1 - math.sqrt(I*I+J*J)/radius))
            if (c <0):
                c = int(0)
            newarray[i][j]=(255,0,0,c)
    newarray.close()
    
def distance(a,b):
    x=[]
    y=[]
    r=[]
    theta=[]
    for i in range(len(a)):
        x.append(a[i].position[0] - b.position[0])
        y.append(a[i].position[1] - b.position[1])
        r.append(math.sqrt(x[i]**2+y[i]**2))
        theta.append(math.atan2(y[i],x[i])*180/math.pi)
    index = r.index(min(r))
    d = [min(r),theta[index],index]
    return d

def display(distance, p1):
    #print("The enemy is ", math.floor(distance[0]), " units away on a bearing of ",math.floor(distance[1]),".\nYou are moving", p1.velocity, "units per turn")
    #print("Your acceleration is: ", p1.acceleration,"units per turn per tur.\nYou are at: ",p1.position,"\n\n")
    font = pygame.font.SysFont(None, 25)
    text = font.render("Pos:  "+str(p1.position)+"  Vel:  "+str(p1.velocity)+"  Acc:  "+str(p1.acceleration), True,(0,0,255))
    gameDisplay.blit(text,(0,0))
    
def think(enemy, player):
# layer1, layer1_bias, output, output_bias):
    #calculate inputs for brain
    x= enemy.position[0]
    y= enemy.position[1]
    #Distance to player
    dx = player.position[0] - x
    dy = player.position[1] - y
    dp= math.sqrt(dx**2 + dy**2)
    

    #player direction
    theta = math.atan2(dy,dx)*180/math.pi

    #origin distance
    r = math.sqrt(x**2 + y**2)

    #origin direction
    angle = math.atan2(-y,-x)*180/math.pi

    #Ai velocity
    vx = float(enemy.velocity[0])
    vy = float(enemy.velocity[1])

    #AI acceleration
    ax = float(enemy.acceleration[0])
    ay = float(enemy.acceleration[1])

    i = program.think(dp, theta, r, angle, vx, vy, ax, ay)
    return i


def game_loop():
    p1 = Ship("player",0,0,0,0.01, 30,1)
    e = []
    e_num = 20
    init_ships(p1,e, e_num)
    radius = 100
    circle = pygame.Surface((2*radius,2*radius)).convert_alpha()
    init_planet(radius,circle)
    
    gameDisplay.fill(black)
    player_rect = (int((display_width-ship_size)/2),int((display_height-ship_size)/2),int(ship_size), int(ship_size))
    print(player_rect)
    pygame.draw.rect(gameDisplay, white, player_rect)
    pygame.display.update()
   
    win = 0
    scan = 0
    turn = 0
    hit_check = 0
    d = distance(e,p1)
    dx = d[0]*math.cos(d[1]*math.pi/180)
    dy = d[0]*math.sin(d[1]*math.pi/180)
    display(d,p1)
    
    #This is the actual game logic, each iteration through the while loop is one game turn.
    while (win != 1):
        gameDisplay.fill((hit_check*60,0,0))
        for event in pygame.event.get():
            #print(event)
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_KP1:
                    move = 1
                elif event.key == pygame.K_KP2:
                    move = 2
                elif event.key == pygame.K_KP3:
                    move = 3
                elif event.key == pygame.K_KP4:
                    move = 4
                elif event.key == pygame.K_KP6:
                    move = 6
                elif event.key == pygame.K_KP7:
                    move = 7
                elif event.key == pygame.K_KP8:
                    move = 8
                elif event.key == pygame.K_KP9:
                    move = 9
                else:
                    move = 5
                turn += 1
                
                if hit_check > 0:
                    hit_check -= 1
        
    
                p1.turn(move)
                if (move==5):
                    scan += 1
                    print("You have been scanning for ", scan, "/3 turns.")
                else:
                    scan = 0
                #When the player makes their choice their ship is moved accordingly
                p1.move()

                #After the player has moved all the enemy ships move
                for i in range(len(e)):
                    emove = think(e[i], p1)#, layer1, layer1_bias, output, output_bias)
                    #print("Enemy move = ",emove)
                    e[i].acceleration = emove
                    #if(e[i].acceleration[0]>10): e[i].acceleration[0] = 10
                    #elif(e[i].acceleration[0]<-10): e[i].acceleration[0] = -10
                    #elif(e[i].acceleration[1]>10): e[i].acceleration[1] = -10
                    #elif(e[i].acceleration[1]<-10): e[i].acceleration[1] = -10
                    #e[i].turn(emove)
                    e[i].move()

                #The distance between the nearest enemy ship and the player's ship is calculated and displayed
                d = distance(e,p1)
                dx = d[0]*math.cos(d[1]*math.pi/180)
                dy = d[0]*math.sin(d[1]*math.pi/180)
                display(d,p1)

                #if the player hasn't changed their acceleration for at least 3 turns, the nearest enemy ship's velocity is displayed.
                if (scan >= 3):
                    print("The enemy is moving at ", e[d[2]].velocity," units per turn.")
    
                #This begins combat calculations, first is the nearest enemy ship in range?
                if(d[0] <= p1.fire_range):
                    #If the ship is in range, it is shot at.
                    print("\n--You fire on the enemy.--")
                   #There is a random element for accuracy, changing accuracy calculation could account for range modifiers etc.
                    dist = d[0]
                    if dist == 0: dist = 1
                    hit = random.random()*p1.fire_range/dist
                    print("^\nHit Roll: ", hit,"\n^")
                    if (hit >= 0.5):
                        print("\n<-You hit the enemy.->")
                        #If the enemy is hit, reduce its hp, if its hp is zero remove it from the game.
                        e[d[2]].hp-= 1
                        gameDisplay.fill(red)
                        hit_check = 3
                        if (e[d[2]].hp==0):
                            e.pop(d[2])
                            #If an enemy is removed check the win condition
                            if (len(e)>0):
                                print("\n<-Your fire destroyed the enemy!->")
                            else:
                                print("You defeated the enemy!\nIt took", turn, "turns.")
                                win = 1
                    else:
                        print("\nx-You missed-x")
                
                
        display(d,p1)
        
        
        gameDisplay.blit(circle,((center[0]-(p1.position[0]*ship_size)-radius),(center[1]+(p1.position[1]*ship_size)-radius)))
        pygame.draw.line(gameDisplay, blue, center, (center[0]-(p1.position[0]*ship_size),center[1]+(p1.position[1]*ship_size)),2)
        pygame.draw.rect(gameDisplay, white, player_rect)
        for i in range(len(e)):
            pygame.draw.rect(gameDisplay, (200,255,255),[display_width/2+((e[i].position[0] - p1.position[0])*ship_size),display_height/2-((e[i].position[1] - p1.position[1])*ship_size),5,5])
        pygame.draw.line(gameDisplay,green,center,((int(display_width/2+(dx*ship_size)),int(display_height/2-(dy*ship_size)))))
        pygame.display.update()
        
game_loop()
pygame.quit()
quit()
