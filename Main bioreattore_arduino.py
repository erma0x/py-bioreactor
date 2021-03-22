import schedule
import threading
import serial
from matplotlib import pyplot
import pyfirmata
from time import *
import numpy as np
########## _FUNZIONE_  ############
def od(num_misure):
    #imposto classe pin
    check=False
    fotoresistenza_pin=1
    laser_pin=7
    sensor=board.get_pin('a:1:i') # pinMode
    laser=board.get_pin('d:7:o')
    #essential for reports 
    board.analog[fotoresistenza_pin].enable_reporting()
    #setto variabili 
    counter=0
    lista_misure=[]
    valore_output=[]
    while num_misure>counter:
        board.digital[7].write(1)
        misurazione_od=board.analog[1].read() #leggo
        sleep(0.1)
        board.digital[7].write(0)
        sleep(0.1)
        misurazione_od=board.analog[1].read()
        #creo lista di valori misurazioni
        lista_misure.extend([misurazione_od])
        counter+=1
        check=True
    misura=np.mean(lista_misure)
    #inserire anche un intervallo di confidenza stimato
    #oppure errore della misura nella lista
    tempo=localtime()
    return(check, misura, tempo)
#######################################


#se lascio un pin acceso con una funzione poi lo devo
#anche spengere?
def job(on):
    if on==True:
        print("I'm working...")
        time=localtime()
        print(time)
def a(on):
    if on==True:
        print('on')
        sleep(5)
        
    
#al posto di job ci metto le varie funzioni
#devo rendere od mutualmente escludibilie
#dalle altre funzioni
schedule.every(1).seconds.do(job(True))
schedule.every(1).seconds.do(a(True))
while True:
    schedule.run_pending()
