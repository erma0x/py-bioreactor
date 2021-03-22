import serial
from pyfirmata import *
from matplotlib import pyplot
import pyfirmata
from time import *
import numpy as np
#imposto la board
port = "COM3"
board = Arduino(port)
it = pyfirmata.util.Iterator(board)
it.start()
########## _FUNZIONE_  ############
def analisi_rubinetto(num_misure):
#voglio una funzione che calcoli quanto tenere
#aperto il rubinetto per prelevare tot ml, per poi
#passarli all'nutrimento, esempio, voglio fare delle analisi
#su colonna per piastrarli oppure incubarli ed allora voglio che
#premendo un bottone mi prelevi tot ml, sarebbe sempre con elettrovalvola
#ma con strozzatura, prove empiriche per stabilire la portata
#premo un bottone per avere il campione e finito di premere l'elettrovalvola
#si chiude. Voglio sapere quanto ho prelevato
    #portata=*** #Calcolare empiricamente
    pin_bottone=1
    elettrovalvola=2
    sensor=board.get_pin('d:1:i') # pinMode
    board.digital[pin_bottone].enable_reporting()
    if board.digital[1]read()==1:
        tempoi=localtime()
        while board.digital[1]read()==1:
            board.digital[2].write(1)
        tempof=localtime()
    tempo_totale=tempof-tempoi #liq=t*p
    liq=tempo_totale*portata
    return liq
#al liquido devo andarlo ad aggiungere al liquido che la coltura ha perso
#nella prossima sessione di food
    
        
        
        
        
        
