import serial
from pyfirmata import *
import pyfirmata
from time import *
import numpy as np

#imposto la board
port = "COM3"
board = Arduino(port)
it = pyfirmata.util.Iterator(board)
it.start()
########## _FUNZIONE_  ############
def solenoid_valve(quanto_togliere,colonna):
    #voglio farli separati i controlli dell'solenoide
    tempo_attesa=quanto_togliere/portata #portata [ml/s]
    pin_carico, pin_scarico=1,2
    sensor=board.get_pin('d:1:o')
    sensor=board.get_pin('d:2:o')
    global check,tempo_solenoid
    tempo_solenoid=localtime()
    board.digital[1].write(1) 
    board.digital[2].write(1)
    sleep(tempo_attesa)
    board.digital[1].write(0)
    board.digital[2].write(0)
    check+=1
    return(check,time)

    
    
    
    

    
