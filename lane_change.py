# -*- coding: utf-8 -*-
"""
Created on Fri May 24 10:38:14 2019

@author: mgtpe
"""

"""
entrées : a_f2_new la nouvelle accélération du follower de la voie où on change si on change de voie
a_f2_current l'accélération actuelle du follower de la voie où on veut changer, a_f_new l'acceleration du follower actuel si on change
a_f_current l'accélération du follower actuel, p le coefficient de politesse du véhicule
"""

def utility_courtesy(a_f2_new, a_f2_current, a_f_new, a_f_current, p):
    I=p*(a_f2_new - a_f2_current + a_f_new - a_f_current)
    return I

"""
entrées : ; xl1=position leader dans la voie où se trouve le véhicule; 
xl2= position leader dans la voie où veut aller le véhicule; l1, l2 =voies considérées; xv= position du véhicule;
R= coefficient de respect du code de la route


paramètres:
cste= ce qui donne poids à overtaking
"""

def utility_overtaking(xl1, xl2, l1, l2, xv, R):
    cste=0.01
    if l1<l2:    # si la voie considérée est à droite de la voie actuelle
        if xl1-xv < 100 : # si il y a un véhicule proche sur la voie actuelle, il ne faut pas le doubler par la droite
            O=cste*(99-R)/50
        if xl1-xv>100 and xl2-xv>200 : # si il n'y a pas de véhicule proche sur la voie actuelle et qu'il n'y a pas de véhicue à droite, il faut se rabattre
            O=-cste*(99-R)/50
        else :
            O=0
    else: #si la voie considérée est à gauche de la voie actuelle
        O=0
    return O

"""
entrées : leading_yv type de vehicule devant la voiture (camion, vl,...) ; type de véhicule qui serait devant la voiture
dans la voie évaluée: leading_ye; cv = classe voiture (autonome ou humain = 0)

paramètres: à définir
cste donne l'impact de la présence d'un camion ou bus
"""

def utility_truck(leading_yv, leading_ye, cv):
    cste=0.1
    if cv== 0: # ce qui correspond à un conducteur humain
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
donne l'utilité marginale due à l'approche d'un tournant obligatoire 

entrées : xv: position longitudinale de la voitue; xt: position longitudinale du tournant; 
yv : voie dans laquelle se trouve la voiture; yt : voie dans laquelle il faut etre pour tourner
ye voie où on veut aller; cv= classe du véhicule (autonome ou pas); v= vitesse du véhicule 
rv, rt: sont les routes du véhicule et du futur tournant à prendre
paramètres : à définir
Tth temps où human driver on commence à considérer le tournant
Tta temps avant le tournant à partir duquel le AV commence à considérer le tournant
cste : coefficient pondérant l'approche au tournant


on suppose que les voies sont notées par ordre croissant (de gauche à droite) 
"""


def utility_turn(xv, xt, yv, yt, ye, rt,rv, cv, v):
    Tth = 10 
    Tta = 20
    cste= 0.1
    if rt==rv:
        if cv is 'AV' and (xv-xt)/v<=Tta or cv is 'HD' and (xv-xt)/v<=Tth :
            if abs(yv-yt)<abs(ye-yt):
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
entrées: Ag0 = aggressivité de base du véhicule, cv= classe du véhicule (autonome ou pas), xv= position véhicule dans voie
xt= position du tournant dans voie, v= vitesse du véhicule, r=route où se trouve le véhicule, rt= route où se trouve le tournant 
"""


def aggressivity(Ag0, cv, xv, r, xt, rt, v):
    Tth = 10 
    Tta = 20
    if r==rt:
        if cv is 'AV' and (xv-xt)/v<=Tta or cv is 'HD' and (xv-xt)/v<=Tth :
            Ag= Ag0 + (99-Ag0)/(2*abs(xt-xv)+1)
        else :
            Ag= Ag0
    else:
        Ag=Ag0
    return Ag


"""
# entrées : cv=classe véhicule (autonome ou human driver); a1= acceleration que devrait avoir le véhicule s'il restait dans se voie;
# a2= accélération que devrait avoir le véhicule s'il changeait de voie; af1= accélération du follower s'il ne se passe rien
# af2 accélération du nouveau follower s'il y a chagement de voie; Ag= agressivité du véhicule

#paramètres: bsafe décélération max acceptée
"""
def safety_criterion (Ag,a,af):
    bsafe= -2
    b= bsafe*(1+ 0.1*(Ag-50)/50)
    if a >= b  and af >= b:
        safe= True
    else:
        safe=False
    return safe

    
"""
def safety_criterion (cv, a1, a2, af1, af2, Ag):
    bsafe= -2
    b= bsafe*(1+ 0.1*(Ag-50)/50)
    if cv=='HD': # le conducteur humain ne va pas comparer sa sécurité à celle de la voie d'à côté parce que si jamais il y a un obstacle il va avoir tendance à piler alors que le VA va penser à changer de voie 
        safe_stay=True
        if a2 >= b  and af2 >= b: # si les décélrations imposées aux véhicules ne sont pas trop importantes
            safe=True # le changement de voie est possible
        else :
            safe= False #le changement de voie est pas possible
    
    if cv=='AV':
        if a1 < b or af1 < b: #si c'est dangereux de rester, on compare l'importance du danger avec l'autre voie
            safe_stay= False
            if a1 + af1 < a2 + af2 :
                safe= True
            else :
                safe=False
        else :  # si c'est pas dangereux de rester on regarde juste si c'est dangereux de changer
            safe_stay= True
            if a2 >= b and af2 >= b:
                safe = True
            else:
                safe= False            
    return (safe, safe_stay)
"""