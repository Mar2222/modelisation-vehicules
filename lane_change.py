# -*- coding: utf-8 -*-
"""
Created on Fri May 24 10:38:14 2019

@author: mgtpe
"""

"""
fonction premettant de calculer l'utilité marginale due à l'impact d'un changement de voie sur les autres véhiules 

ENTREES :
    a_f2_new (float): accélération du follower de la voie où ego_vehicle considère aller, si ego_vehicle change de voie
    a_f2_current (float): accélération du follower de la voie où ego_vehicle considère aller, si ego_vehicle ne change pas de voie
    a_f_new (float): acceleration du follower de la voie où se trouve ego_vehicle, si ego_vehicle change de voie
    a_f_current (float): accélération du follower de la voie où se trouve ego_vehicle, si ego_vehicle ne change pas de voie
    p (float): coefficient de politesse d'ego_vehicle
    
SORTIE :
    I (float): utilité marginale due à l'impact sur les véhicules followers d'un changement de voie
"""

def utility_courtesy(a_f2_new, a_f2_current, a_f_new, a_f_current, p):
    I=p*(a_f2_new - a_f2_current + a_f_new - a_f_current)
    return I


"""
fonction premettant de calculer l'utilité marginale due aux règles pour doubler (ex: en europe o ne peut pas doubler par la droite)

ENTREES : 
    xl1 (float): position du véhicule leader dans la voie où se trouve ego_vehicle
    xl2 (float): position du véhicule leader dans la voie où veut aller ego_vehicle
    l1, l2 (float): numéros des voies considérées
    xv (float): position longitudinale de ego_vehicle;
    R (float): coefficient de respect du code de la route de ego_vehicle


PARAMETRES:
    cste: ce qui donne poids à overtaking

SORTIES:
    O (float): utilité marginale due aux règles de conduite    
"""

def utility_overtaking(xl1, xl2, l1, l2, xv, R):
    cste=0.2
    if l1<l2:    # si la voie considérée est à droite de la voie actuelle
        if xl1-xv < 100 : # si il y a un véhicule proche sur la voie actuelle, il ne faut pas le doubler par la droite
            O=cste*R/50
        if xl1-xv>100 and xl2-xv>200 : # si il n'y a pas de véhicule proche sur la voie actuelle et qu'il n'y a pas de véhicue à droite,
            #il faut se rabattre
            O=-cste*R/50
        else :
            O=0
    else: #si la voie considérée est à gauche de la voie actuelle
        O=0
    return O

"""
fonction premettant de calculer l'utilité marginale due à la présence de véhicules lourds

ENTREES :
    leading_yv (string): type de véhicule ('VL', 'Bus', 'PL') se trouvant devant ego_vehicle
    leading_ye (string) : type de vehicule se trouvant devant ego_vehicle sur la voie considéré
    cv (string): classe ego_vehicle ('HD','AV')
    # à revoir: prendre en compte les distances à ces vehicules (c'est déjà un peu vu dans la fonction générale parce que les leaders 
    sont sensés être proches, mais peut-être faire un truc inversement proportionnel à la distance)
    
PARAMETRE : 
    cste : donne l'impact de la présence d'un camion ou bus

SORTIE:
    (float) : utilité marginale due à la présence de véhicules lourds
"""

def utility_truck(leading_yv, leading_ye, cv):
    cste=0.1
    if cv is 'HD': 
        if leading_yv is not 'VL' and leading_ye is 'VL':
            c= -1
        if leading_ye is not 'VL' and leading_yv is 'VL':
            c= 1
        else :
            c=0
    else :
        c=0
    return c*cste


"""
fonction donnant l'utilité marginale due à l'approche d'un tournant obligatoire 

ENTREES : 
    xv/xt (float): positions longitudinale de la voitue/du tournant 
    lv/lt/le (float): numéros de voies où se trouve ego_vehicle/le tournant/où veut aller ego_vehicle
    cv (string): classe du véhicule ('AV' ou 'HD')
    v (float): vitesse du véhicule 
    rv/rt (float): numéros des routes sur lesquelles se trouvent ego_vehicle/le futur tournant à prendre

PARAMETRES :

Tth/Tta (floats): temps restant à partir duquel human driver/ autonomous vehicle commence à considérer le tournant
cste : coefficient pondérant l'approche au tournant

REMARQUE:
on suppose que les voies sont notées par ordre croissant (de gauche à droite) 
"""


def utility_turn(xv, xt, lv, lt, le, rt,rv, cv, v):
    Tth = 7 
    Tta = 10
    cste= 100 #il faut que l'utilité de l'approche du tournant soit la plus élevée
    if rt==rv: # si la route sur laquelle se trouve le tournant est la route où se trouve le véhicule 
        if cv is 'AV' and (xv-xt)/v<=Tta or cv is 'HD' and (xv-xt)/v<=Tth : #si le véhicule se trouve dans la zone où il a "conscience" du tournant
            if abs(lv-lt)<abs(le-lt): #si changer de voie fait se rapprocher de la voie désirée
                d=1
            else :
                d= -1
            n= cste/(abs(xt-xv)+1)
        else :
            n=0
            d=0
    else:
        n=0
        d=0  
        
    return n*d


"""
fonction permettant de faire évoluer l'aggressivité de ego_vehicle

ENTREES:
    Ag0 (float) : aggressivité de base de ego_vehicle
    cv (float): classe du véhicule (autonome ou pas)
    xv/xt (float): position de ego_vehicle/ du futur tournant 
    v (float): vitesse du véhicule
    r/rt (floats) : routes où se trouve le véhicule/le tournant 

PARAMETRES:
    Tth (float): temps restant à partir duquel human driver vehicle commence à considérer le tournant
"""


def aggressivity(Ag0, cv, xv, r, xt, rt, v):
    Tth = 7
    if r==rt:
        if cv is 'HD' and (xv-xt)/v<=Tth :
            Ag= Ag0 + (99-Ag0)/(2*abs(xt-xv)+1)
        else :
            Ag= Ag0
    else:
        Ag=Ag0
    return Ag


"""
fonction permmettant de déterminer si les accélérations de ego_vehicle et de son follower sont "safe"

ENTREES :
    Ag (float): aggressivité de ego_vehicle
    a/af (floats): accélérations de ego_vehicle/de son vehicule followerans se voie;

PARAMETRES :
    bsafe (float): décélération max acceptée (décélération moyenne)
"""

def safety_criterion (Ag,a,af):
    bsafe= -2
    b= bsafe*(1+ 0.1*(Ag-50)/50)
    if a >= b  and af >= b:
        safe= True
    else:
        safe=False
    return safe
