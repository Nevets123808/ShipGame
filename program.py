import math
import numpy as np
import random
def thrust(desired_vector, current_vector):
    Areq = np.subtract(desired_vector,current_vector)
    size = np.linalg.norm(Areq)
    if size == 0:
        return Areq
    Anorm = np.rint(Areq/size)

    return Anorm

def think(dp, theta, r, angle, vx, vy, ax, ay):
    current_vector = [vx,vy]
    desired_vector = [0,0]
    dx = dp*math.cos(theta*math.pi/180)
    dy = dp*math.sin(theta*math.pi/180)

    #determines desired vector component for player position.
    if 0 <= dx <= 50:
        desired_vector[0] = round((dx-50))
    elif -50 <= dx < 0:
        desired_vector[0] = round((dx+50))

    if 0 <= dy <= 50:
        desired_vector[1] = round((dy-50))
    elif -50 <= dx < 0:
        desired_vector[1] = round((dy+50))

    #The enemy wants to return to the origin. A restoring component is added to
    #the desired vector. Plus a small random element.
    
    x = round(r*math.cos(angle*math.pi/180))#+ math.floor(random.random()+0.5)
    y = round(r*math.sin(angle*math.pi/180))#+ math.floor(random.random()+0.5)
    #print("x = ",x,", y = ",y)
    desired_vector = np.add(desired_vector,[x,y])
    #print(desired_vector)
    return thrust(desired_vector,current_vector)

a = think(100,30,0,0,0,0,0,0)
print(a)
