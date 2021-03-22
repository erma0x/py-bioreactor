import serial
from pyfirmata import *
import pyfirmata
from time import *
import numpy as np
#imposto la board
#sensor=board.get_pin('a:1:i')
port = "COM3"
board = Arduino(port)
it = pyfirmata.util.Iterator(board)
it.start()
########## FUNZIONE LUCE  ############
def light(freq,ri,gi,bi,pulse_on,fade_on):
    #pulse_on per emettere luce discreta con intensita' date
    #fade_on la luce viene mandata gradualmente
    #accendere anche i led in modo differenziale r->g->b
    #daily_cycle tempo su 24 quanto restare acceso
    #freq [Hz] di emissione luce
    #ri,gi,bi sono le intensita' dei vari colori [0:100] %
    #devo farlo con transistor e batteria, perche' richiedono >5V
    #in pwm gestisco le intensita' RGB dato che sono 3 canali diversi
    #se lo connetto al digitale che ha pwm e gli do i valori che voglio io
    #nel range di 0/1024 con raspberry e 0/255 con Arduino 
    #1% duty cycle di risoluzione
    pin_red,pin_green,pin_blue=1,2,3
    valore_ri=ri*255/100 #trasformo intensita' percentuale 
    valore_gi=gi*255/100 # in una che arduino puo' comprendere
    valore_bi=bi*255/100 #per RBerry invece essendo da 1/100 non ho bisogno
    delay=1/freq 
    increment_r=valore_ri/128 #incrementi per arrivare al massimo dopo 128 passi
    increment_g=valore_gi/128 # 512 su RBerry
    increment_b=valore_bi/128
    while pulse_on==True and fade_on==False: 
        board.analog[1].write(valore_ri)
        board.analog[2].write(valore_gi)
        board.analog[3].write(valore_bi)
        sleep(delay)
        board.analog[1].write(0)
        board.analog[2].write(0)
        board.analog[3].write(0)
        sleep(delay)
        
## PARTE DOVE L'ACCENSIONE E' GRADUALE
##    while pulse_on==False and fade_on==True:
##        time_unit=delay/255 #su Arduino mentre /1024 su Rb
##        board.analog[1].write(0)
##        board.analog[2].write(0)
##        board.analog[3].write(0)
##        val_r,val_g,val_b=0,0,0 #3 incrementi diversi a seconda dell'intensita' max
##        #inc_r,g,b sono gli incrementi, partono da zero e arrivano a valore_r,g,b (massimo)
##        while valore_ri and valore_gi and valore_bi>inc_b
##
##        else:
##                value -= increment
##                time.sleep(0.002)
##        if (value >=1024):
##                increasing = False
##        if (value <= 0):
##                increasing = True
    
        
        
        
    
    
    
    
