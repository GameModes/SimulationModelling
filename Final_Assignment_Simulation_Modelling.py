#!/usr/bin/env python
# coding: utf-8

# In[56]:


import math
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import figure
from ipywidgets import interact

# fysische informatie:
TANK_INHOUD1 = 100          # liter
INSTROOM1 = 6 / 60           # liter per s
INSTROOM2_1 = 1/ 60
CONCENTRATIE_INSTROOM = 0.2 # kg / liter
UITSTROOM1 = 4 / 60         # liter per s
UITSTROOM1_2 = 3/60
instroom_salt_tank1 = CONCENTRATIE_INSTROOM * INSTROOM1

TANK_INHOUD2 = 100          # liter
INSTROOM1_2 = UITSTROOM1_2  # liter per s
UITSTROOM2_1 = INSTROOM2_1 
UITSTROOM2 = 2/60

def simulatiesettings():
    '''maakt een aantal globale variabelen aan voor de simulatie zoals stapgrootte en DUUR
    '''
    DUUR = 10*3600 # 3600 seconden = 1 uur
    AANTAL_STAPPEN = 100
    stapgrootte = DUUR / AANTAL_STAPPEN # in seconden
    return stapgrootte, AANTAL_STAPPEN

stapgrootte, AANTAL_STAPPEN = simulatiesettings()

def array_maker(stapgrootte):
    ''' array_maker maakt met behulp van stapgrootte een tijd array en een lege zout array
    '''
    tijd = stapgrootte * np.arange(AANTAL_STAPPEN + 1)
    zout = np.zeros(AANTAL_STAPPEN + 1)
    return zout, tijd
    
def simulatieloop(stapgrootte):
    '''simulatieloop maakt met behulp van stapgrootte een array van tijd 
       en de verandere zoutconcentratie van de tanks in een array
    '''
    zout, tijd = array_maker(stapgrootte)
    zout_1 = zout.copy() #copy van dezelfde groote van de zout array
    zout_2 = zout.copy() #copy van dezelfde groote van de zout array
    zout_2[0] = 20 #tank 2 begint bij 20kg
    for stap in range(1, AANTAL_STAPPEN + 1):    
        concentratie_t_min1_1 = zout_1[stap - 1] / TANK_INHOUD1 # zoutconcentratie van tank 1
        concentratie_t_min1_2 = zout_2[stap - 1] / TANK_INHOUD2 # zoutconcentratie van tank 2
                      # vorige stap     +  stapgrootte * postieve stromingen                                         - negatieve stromingen

        zout_1[stap] = zout_1[stap - 1] + stapgrootte * ((instroom_salt_tank1 + (concentratie_t_min1_2 * INSTROOM2_1)) - ((concentratie_t_min1_1 * (UITSTROOM1_2 + UITSTROOM1))))
        zout_2[stap] = zout_2[stap - 1] + stapgrootte * ((concentratie_t_min1_1 * INSTROOM1_2) - (concentratie_t_min1_2 * (UITSTROOM2_1 +  UITSTROOM2)))
    return tijd, zout_1, zout_2


# plot
@interact
def plot(stapgrootte=360):#interactieve variabele is stapgrootte met standaard 
    '''plot aka de main functie waarin de functies worden aangeroepen en geplot met een interactie van ipywidgets
    '''
    tijd, zout_1, zout_2 = simulatieloop(stapgrootte)
    fig, ax = plt.subplots()
    ax.plot(tijd, (zout_1)/100, color="red", label="zout in tank 1")
    ax.plot(tijd, (zout_2)/100, color="blue",  label="zout in tank 2")
    ax.set_title('zoutconcentratie in de tank')
    ax.set_xlabel('tijd (seconden)')
    ax.set_ylabel('zout concentratie (kg / liter)')
    plt.legend(loc="best")
    return plt.figure()


# In[ ]:




