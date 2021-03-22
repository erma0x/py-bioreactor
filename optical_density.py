import serial
from pyfirmata import *
from matplotlib import pyplot
import pyfirmata
from time import *
import numpy as np

#SE PROGRAMMA  NON PARTE
#non aprire lo sketch standardfirmata se il processo e' in esecuzione
#spengi/riaccendi/salva/esci

#ANALISI DATI
# l'od cambia a seconda della specie?
#se non cambia posso fare curve di taratura inizia;o
#e sapera anche le concentrazioni delle cellule

#Da implementare nella Main
##secondi in un giorno 86400 <- Schedule!
##delay=frequenza_misurazioni_giorno/86400
##time.sleep(delay) #aspetta fino a prossima misura

#imposto la board
port = "COM3"
board = Arduino(port)
#faccio partire il processo
it = pyfirmata.util.Iterator(board)
it.start()
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
start =clock() #prendo il tempo
od(20)
end = clock() #fine processo
print(" il processo dura ", end-start ," sec")
print(valore_output)

