import serial
from pyfirmata import *
from matplotlib import pyplot
import pyfirmata
from time import *
import numpy as np
#imposto la board
port = "COM3"
board = Arduino(port)
#faccio partire il processo
it = pyfirmata.util.Iterator(board)
it.start()
def air(on, n_col):
    #n_col e' il numero della colonna
    pin_aria_1,pin_aria_2,pin_aria_3=1,2,3
    if on==True:
        #posso fare con analog e dargli in pwm intensita' diverse
        if n_col==1:
            board.digital[pin_aria_1].write(1)
        elif n_col==2:
            board.digital[pin_aria_2].write(1)
        elif n_col==3:
            board.digital[pin_aria_3].write(1)
        else:
            pass
    elif on==False:
        if n_col==1:
            board.digital[pin_aria_1].write(0)
        elif n_col==2:
            board.digital[pin_aria_2].write(0)
        elif n_col==3:
            board.digital[pin_aria_3].write(0)
    else:
        print('valore "on" sbagliato ')
        pass
        
        
            
        
        
    
    
