import serial
from pyfirmata import *
import pyfirmata
from time import *
import numpy as np
port = "COM3"
board = Arduino(port)
it = pyfirmata.util.Iterator(board)
it.start()
#faccio aprire una valvola, chiudo, misuro, apro scarico, chiudo
########## _FUNZIONE_  ############
def salinity():
    solenoide_1, solenoide_2, transistor ,lettura=1,2,3,4 #pin
    board.analog[4].enable_reporting()
    global misura_salinity
    #tempo_riempimento= volume camera/portata
    #faccio passar corrente con un transistor
    #lettura a valle della corrente che passa
    board.digital[1].write(1) #apro e chiudo il solenoide
    sleep(tempo_riempimento)
    board.digital[1].write(0)
    
    board.digital[3].write(1) #attivo transistor e faccio passare corrente
    sleep(0.5) #permette letture piu' pulite
    misura_salinity=board.analog[4].read() #leggo
    
    board.digital[2].write(1) #svuoto
    sleep(tempo_riempimento)
    board.digital[2].write(0)
    
    
    
