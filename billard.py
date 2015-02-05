                                                #BILLARD AMERICAIN : Partie parfaite#




from tkinter import *
from math import *
from PIL import Image, ImageTk
from random import randint
import time

#Variables
diametre_boule = 11.59
diametre_trous_lat = 24.764
diametre_trous_coin = 21.59
mvt = 0

#On initialise la liste des positions futures de la boule
positions = []

#On definit les coordonnees initiales des boules
positions_ini = [
    (341.205, 340.905),
    (595.205, 340.905),
    (606.795, 335.11),
    (606.795, 346.7),
    (618.385, 329.315),
    (618.385, 352.495),
    (629.975, 335.11),
    (629.795, 346.7),
    (641.565, 340.905),
    (618.385, 340.905)
]

positions_act = positions_ini[:]

#On attribut( couleur a chaque boule
couleurs = ['white',
            '#FFFF00',
            '#0066FF',
            '#CC0000',
            '#660066',
            '#FF8C00',
            '#339933',
            '#A52A2A',
            '#081010',
            '#CCCC00'
]

#On definit les coordonnees des trous en precisant leur type: coin ou latéral
trous = [(204.041,203.741,225.631,225.331, diametre_trous_coin),
         (461.618,193.967,486.382,218.731, diametre_trous_lat),
         (722.369,203.741,743.959,225.331, diametre_trous_coin),
         (204.041,468.069,225.631,489.659, diametre_trous_lat),
         (461.618,474.636,486.382,499.4, diametre_trous_coin),
         (722.369,468.069,743.959,489.659, diametre_trous_coin)
         ]

#On attribut une position a chaque boule apres qu'elle soit tombee
#La boule blanche retourne au point de depart
positions_tombees = [(341.205, 340.905),
                     (150, 200),
                     (150, 215),
                     (150, 230),
                     (150, 245),
                     (150, 260),
                     (175, 200),
                     (175, 215),
                     (175, 230),
                     (175, 245)]

#On définit les 7 zones de deplacements possibles de la boule                     
zones = [(220, 716.41, 219.7, 462.11), #aire de jeu(x_min, x_max, y_min, y_max)
         (204.2454, 229.4174, 203.9454, 229.1714), #zone trou 1
         (461.618, 474.792, 193.031, 219.7), #zone trou 2
         (706.9386, 732.1646,203.9454, 229.1714), #zone trou 3
         (204.2454, 229.4174, 210.2286, 235.4546), #zone trou 4
         (461.618, 474.792, 462.11, 488.779),#zone trou 5
         (706.9386, 732.1646, 210.2286, 235.4546)] #zone trou 6
         


                     
#Fin variables
#Debut fonctions

def creer_boules():
    global boules
    #Creer les objets boules
    boules = 10*[0]
    for i in range(10):
        boules[i] = can.create_oval(0,0,diametre_boule,diametre_boule,width=0,fill='white')
    print(boules)

def initialiser_boules():
    global boules
    #attribuer la position et la couleur à chaque boule
    p = positions_ini[0]
    can.coords(boules[0], p[0], p[1], p[0]+diametre_boule, p[1]+diametre_boule)
    p = positions_ini[9]
    can.coords(boules[9], p[0], p[1], p[0]+diametre_boule, p[1]+diametre_boule)
    can.itemconfig(boules[9], fill=couleurs[9])
    n = [j for j in range(1,9)]
    positions_act[0] = positions_ini[0]
    positions_act[9] = positions_ini[9]
    for i in range(1, 9):
        v = randint(0, len(n)-1)
        p = positions_ini[n[v]]
        can.coords(boules[i], p[0], p[1], p[0]+diametre_boule, p[1]+diametre_boule)
        can.itemconfig(boules[i], fill=couleurs[i])
        positions_act[i] = p
        n.remove(n[v])

def calcul_pos(boules, pos_finale):
    #calcul des positions successives de la boule
    positions = []
    for i in range(1,11):
        l = (pos_finale[0]-positions_act[0][0])/10*i+positions_act[0][0]
        m = (pos_finale[1]-positions_act[0][1])/10*i+positions_act[0][1]
        positions.append([l,m])
        print(l,m)
    mouvement_boule(14, positions)

def rebond_mur(boule, pos):
    #calcule le rebond après choc contre un mur
    xf, yf = pos[0], pos[1]
    if pos[0] < 220:
        xf = positions_act[boule-14][0]-pos[0]+220
    if pos[0] > 716.41:
        xf = positions_act[boule-14][0]-pos[0]+716.41
    if pos[1] < 219.7:
        yf = abs(positions_act[boule-14][1]-pos[1])+219.7
    if pos[1] > 462.11:
        yf = positions_act[boule-14][1]-pos[1]+462.11
    pos_finale = (xf, yf)
    print("pos=" ,xf,yf)
    calcul_pos(boule-14,pos_finale)

def rebond_boule(boule1, boule2, pos):
    #calcule le rebond après choc entre deux boules
    can.coords(boule2, pos[0], pos[1], pos[0]+diametre_boule, pos[1]+diametre_boule)
    positions_act[boule2-14] = pos
    can.coords(boule1, 400, 400, 400+diametre_boule, 400+diametre_boule)
    positions_act[boule1-14] = (400,400)

def test_mur(boule, positions):
    #test si rencontre un mur
    valeurs = []
    for i in range(7):
        valeurs.append((zones[i][0]<positions[0]<zones[i][1] and zones[i][2]<positions[1]<zones[i][3]))
    return True in valeurs
    

def test_trous(boule, positions):
    #test si tombe dans un trou
    valeurs = []
    for i in range(6):
        valeurs.append((positions[0]+(diametre_boule/2)-(trous[i][0]+trous[i][2])/2)**2 + (positions[1]+(diametre_boule/2)-(trous[i][1]+trous[i][3])/2)**2 < (trous[i][4])**2)
    return True in valeurs

def test_boule(boule, positions):
    #test si rencontre une boule
    #valeurs = []
    for i in range(1, 9):
        if (positions[0]-positions_act[i][0])**2 + (positions[1]-positions_act[i][1])**2 < (diametre_boule)**2:
            return (True,i+14)
        return (False,0)
            
        #valeurs.append(positions[0]-(positions_act[i][0]+(diametre_boule/2))**2 + positions[1]-(positions_act[i][1]+(diametre_boule/2))**2 <= (diametre_boule)**2)
    #return True in valeurs 
        
##def mouvement_boule(boule, positions):
##    #deplacement de la boule
##    if positions == []:
##        return
##    v = 1
##    while positions != []:
##        p_future = positions[0]
##        if not test_mur(boule, positions): #test si rencontre mur
##            if test_trous(boule, positions): #test si tombe dans un trou
##                can.coords(boule, positions_tombees[boule-14][0], positions_tombees[boule-14][1], positions_tombees[boule-14][0]+diametre_boule, positions_tombees[boule-14][1]+diametre_boule)
##                positions_act[boule-14] = positions_ini[boule-14]
##                return
##            elif test_boule(boule, positions): #test si rencontre boule
##                mouvement_boule(boule, positions) 
##            return
##        else :
##            mouvement_boule(boule, positions)
##            
##            positions_act[boule-14] = p_future
##            can.coords(boule, p_future[0], p_future[1], p_future[0]+diametre_boule, p_future[1]+diametre_boule)
##            del positions[0]
##            can.update()
##            time.sleep(0.01*v)
##            v+=1
##        """else :
##            #rebond
##            xf, yf = p_future[0], p_future[1]
##            if p_future[0] < 194:
##                xf = positions_act[boule-14][0]-p_future[0]+194
##            if p_future[0] > 754:
##                xf = positions_act[boule-14][0]-p_future[0]+754
##            if p_future[1] < 194:
##                yf = abs(positions_act[boule-14][1]-p_future[1])+194
##            if p_future[1] > 499.4:
##                yf = positions_act[boule-14][1]-p_future[1]+499.4
##            pos_finale = (xf, yf)
##            print("pos=" ,xf,yf)
##            calcul_pos(boule-14,pos_finale)
##            return"""
##        positions_act[boule-14] = p_future

def mouvement_boule(boule, positions):
    #deplacement de la boule
    if positions == []:
        return
    v = 1
    while positions != []:
        p_future = positions[0]
        """positions_act[boule-14] = p_future
        can.coords(boule, p_future[0], p_future[1], p_future[0]+diametre_boule, p_future[1]+diametre_boule)
        del positions[0]
        can.update()
        time.sleep(0.01*v)
        v+=1"""
        if test_trous(boule, p_future): #test si tombe dans un trou
             #tombe
            print("tombe")
            can.coords(boule, positions_tombees[boule-14][0], positions_tombees[boule-14][1], positions_tombees[boule-14][0]+diametre_boule, positions_tombees[boule-14][1]+diametre_boule)
            positions_act[boule-14] = positions_tombees[boule-14]
            print("act=", positions_act[boule-14])
            return
        else:
            if not test_mur(boule, p_future): #test si rencontre mur
                print("rebond mur")
                rebond_mur(boule, positions[-1]) #rebond mur
                return
            else:
                reb = test_boule(boule, p_future)
                if reb[0]: #test si rencontre boule
                    print("rebond boule")
                    rebond_boule(boule,reb[1],positions[-1]) #rebond boule
                else:
                    positions_act[boule-14] = p_future
                    can.coords(boule, p_future[0], p_future[1], p_future[0]+diametre_boule, p_future[1]+diametre_boule)
                    del positions[0]
                    can.update()
                    time.sleep(0.01*v)
                    v+=1
                
    
        
"""def pointeur(event):
    x = event.x
    y = event.y
    positions  = [(x,y)]
    mouvement_boule(boules[0],positions)
    print(x,y)"""

def pointeur(event):
    #calcul de la position finale de la boule blanche apres impact de canne
    x = 2*positions_act[0][0]-event.x
    y = 2*positions_act[0][1]-event.y
    pos_finale  = (x,y)
    calcul_pos(14,pos_finale)

def curseur(event):
    #dessine la canne pointant la boule blanche
    x, y = event.x, event.y
    dx, dy = x-(positions_act[0][0]+diametre_boule/2), y-(positions_act[0][1]+diametre_boule/2)
    p = 294/sqrt(dx*dx+dy*dy)
    can.coords(canne, x,y,x,y-2,x+p*dx,y+p*dy,x+p*dx,y+p*dy+2)

#Fin fonctions
#Debut creation interface
        
# Creation de la fenetre
fen1 = Tk()
debug = False
    
# Creation du canvas
can = Canvas(fen1,width = 1000, height = 800, bg='grey')
can.pack(side=LEFT, padx =5, pady =5)
    
# Creation du plateau de billard
can.create_rectangle(194,194,754,499.4,fill='#562300')#cadre
can.create_rectangle(220,219.7,728,473.7,fill='#003B00')#surface de jeu
can.create_oval(345,344.7,349,348.7,width=0,fill='black')#point de départ 
can.create_oval(472,344.7,476,348.7,width=0,fill='black')#point du centre
can.create_oval(599,344.7,603,348.7,width=0,fill='black')#point de replacement
can.create_line(347,219.7,347,473.7,width=1,fill='black')#ligne de départ
can.create_oval(204.041,203.741,225.631,225.331,width=0,fill='black')#poche 1
can.create_oval(461.618,193.967,486.382,218.731,width=0,fill='black')#poche 2
can.create_oval(722.369,203.741,743.959,225.331,width=0,fill='black')#poche 3
can.create_oval(204.041,468.069,225.631,489.659,width=0,fill='black')#poche 4
can.create_oval(461.618,474.636,486.382,499.4,width=0,fill='black')#poche 5
can.create_oval(722.369,468.069,743.959,489.659,width=0,fill='black')#poche 6
canne = can.create_polygon(300,300,299,299,594,593,300,299,width=0,fill='chocolate')#canne
creer_boules()
initialiser_boules()

Button(fen1,text='Quitter',bg='red',command=fen1.destroy).pack(side=BOTTOM)
Button(fen1,text='Nouvelle partie',bg='green',command=initialiser_boules).pack(side=BOTTOM)

if debug==True:
    Button(fen1,text='Gauche',command=depl_gauche).pack()
    Button(fen1,text='Droite',command=depl_droite).pack()
    Button(fen1,text='Haut',command=depl_haut).pack()
    Button(fen1,text='Bas',command=depl_bas).pack()
can.bind("<Button-1>", pointeur)
can.bind("<Motion>", curseur)
fen1.mainloop()

#Fin creation interface
