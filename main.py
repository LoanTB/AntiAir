import pygame,random,time
from math import atan2,pi,cos,sin

pygame.init()
timer = pygame.time.Clock()

resolution = (1000,700)
screen = pygame.display.set_mode(resolution)

def collision(rectA, rectB):
    if rectB[0]+rectB[2] < rectA[0]:
        return False
    elif rectB[1]+rectB[3] < rectA[1]:
        return False
    elif rectB[0] > rectA[0]+rectA[2]:
        return False
    elif rectB[1] > rectA[1]+rectA[3]:
        return False
    else:
        return True

def angle(A,B,C): #Trois [x,y]
    AB = [B[0]-A[0],B[1]-A[1]]
    AC = [C[0]-A[0],C[1]-A[1]]
    rad = atan2(AC[1],AC[0])-atan2(AB[1],AB[0])
    return rad

missiles = []
antis = []
particules = []

recu = 1
envoyer = 1
hist = [0,time.time()+1,0]

while True:
    timer.tick(60)
    if hist[1] < time.time():
        hist = [envoyer,time.time()+1,envoyer-hist[0]]
    if random.randint(0,2) == 0:
        rnd = random.randint(1,3)
        if rnd == 1:
            pos = [resolution[0],random.randint(0,resolution[1])]
        elif rnd == 2:
            pos = [random.randint(600,resolution[0]),0]
        elif rnd == 3:
            pos = [random.randint(600,resolution[0]),resolution[1]]
        missiles.append([[pos[0],pos[1],3],5,0])
        recu += 1
        pygame.display.set_caption("Missile allié pour un missile enemie : "+str(round((envoyer/recu*100),0))+"% Débit:"+str(hist[2])+"envoie/seg")
    screen.fill([25,25,25])
    for particule in particules:
        pygame.draw.circle(screen, (random.randint(0,255),random.randint(0,255),random.randint(0,255)), [particule[0][0],particule[0][1]],particule[0][2])
        #pygame.draw.circle(screen, (255,255,0), [particule[0][0],particule[0][1]],particule[0][2])
        #particule[1][0] *= 0.99
        #particule[1][1] *= 0.99
        particule[0][0] += particule[1][0]
        particule[0][1] += particule[1][1]
        particule[2] -= 1
        coll = False
        for missile in missiles:
            Dx = (missile[0][0]-particule[0][0])
            Dy = (missile[0][1]-particule[0][1])
            D = abs(Dx)+abs(Dy)
            if D < 5:
                missile[2] = 2
                missiles.remove(missile)
                coll = True
        if coll or particule[2] == 0:
            particules.remove(particule)
    for missile in missiles:
        Dx = (0-missile[0][0])
        Dy = (resolution[1]/2-missile[0][1])
        D = abs(Dx)+abs(Dy)
        if D < 100 and random.randint(0,10) == 0:
            print(missile)
            missile[2] = 2
            missiles.remove(missile)
        elif missile[2] == 0 and D < 500:
            antis.append([[0,resolution[1]/2,3],missile[1]*(1+random.random()/2+0.5),0,missile])
            missile[2] = 1
            envoyer += 1
            pygame.display.set_caption("Missile allié pour un missile enemie : "+str(round((envoyer/recu*100),0))+"% Débit:"+str(hist[2])+"envoie/seg")
        elif missile[2] == 1 and D < 500*0.5:
            for i in range(3):
                antis.append([[0,resolution[1]/2,2],missile[1]*(i+1),0,missile])
                envoyer += 1
                pygame.display.set_caption("Missile allié pour un missile enemie : "+str(round((envoyer/recu*100),0))+"% Débit:"+str(hist[2])+"envoie/seg")
            missile[2] = 3
        elif missile[2] == 3 and D < 500*0.5*0.5:
            antis.append([[0,resolution[1]/2,1],missile[1]*(2-random.random()*1),0,missile])
            envoyer += 1
            pygame.display.set_caption("Missile allié pour un missile enemie : "+str(round((envoyer/recu*100),0))+"% Débit:"+str(hist[2])+"envoie/seg")
        missile[0][0] += (Dx/D)*missile[1]
        missile[0][1] += (Dy/D)*missile[1]
        pygame.draw.circle(screen, (255-155*(D/1350),100*(D/1350),0), [missile[0][0],missile[0][1]], missile[0][2])
    for anti in antis:
        Dx = (anti[3][0][0]-anti[0][0])
        Dy = (anti[3][0][1]-anti[0][1])
        D = abs(Dx)+abs(Dy)
        if anti[3][2] == 2:
            for i in sorted(missiles, key=lambda missile:abs(missile[0][0]-anti[0][0])+abs(missile[0][1]-anti[0][1])):
                if i[2] == 0:
                    anti[3] = i
                    i[2] = 1
                    break
        if D <= anti[1]*2:
            antis.remove(anti)
            for i in range(anti[0][2]*2):
                particules.append([[anti[0][0],anti[0][1],random.randint(1,2)],[anti[1]*cos(anti[2])+(((random.random()-0.5)*2)*0.5),anti[1]*sin(anti[2])+(((random.random()-0.5)*2)*0.5)],random.randint(30,100)])
        ang = angle([anti[0][0],anti[0][1]],[anti[0][0]+100,anti[0][1]],[anti[3][0][0],anti[3][0][1]])
        """if ang-anti[2] < 0.5*pi:
            anti[2] += (ang-anti[2])/100
        else:
            anti[2] += (ang-anti[2]-(0.5*pi))/100"""

        anti[2] = ang
        anti[0][0] += anti[1]*cos(anti[2])
        anti[0][1] += anti[1]*sin(anti[2])
        #pygame.draw.lines(screen,[100,100,100],5,[[anti[3][0][0],anti[3][0][1]],[anti[0][0],anti[0][1]],[anti[0][0]+100,anti[0][1]]])
        pygame.draw.line(screen,[50,25,50],[anti[3][0][0],anti[3][0][1]],[anti[0][0],anti[0][1]],3)
        #pygame.draw.circle(screen, (0,255,255), [anti[0][0],anti[0][1]], anti[0][2])
        #pygame.display.update()

        """missile[0][0] += (Dx/D)*missile[1]
        missile[0][1] += (Dy/D)*missile[1]"""
    for anti in antis:
        pygame.draw.circle(screen, (255,0,255), [anti[3][0][0],anti[3][0][1]], anti[3][0][2])
        pygame.draw.circle(screen, (0,255,0), [anti[0][0],anti[0][1]], anti[0][2])
    pygame.display.update()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
