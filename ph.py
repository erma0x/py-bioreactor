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
def ph():
    ph_pin=1
    board.analog[ph_pin].enable_reporting()
    board.digital[2].write(1) #accendo
    misurazione_ph=board.analog[1].read() #leggo
    tempo_ph=localtime()
    board.digital[2].write(0) #spengo
    return(misurazione_ph,tempo_ph)
    
    
