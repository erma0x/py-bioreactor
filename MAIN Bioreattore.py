# Gestisce la funzione con la lunghezza dei programmi
import RPi.GPIO as GPIO
from gpiozero import Button
from subprocess import check_call
from signal import pause
import serial
from matplotlib import pyplot
import pyfirmata
from time import *
import numpy as np
import schedule
import sqlite3



# ____ RASPBERRY ________
GPIO.setmode ( GPIO.BOARD )  # 2 modi:  BCM or BOARD
GPIO.setwarnings ( False )
GPIO.setup ( port_or_pin , GPIO.IN )  # set a port/pin as an input
GPIO.setup ( port_or_pin , GPIO.OUT )  # set a port/pin as an output
GPIO.add_event_detect ( Button , GPIO.RISING , callback=main )
# ___________ ARDUINO _________
port = "COM3"
board = Arduino ( port )
it = pyfirmata.util.Iterator ( board )
it.start ( )

#### INIZIALIZZO DB ####
globals(db_file)
def create_db()
    # type: () -> object
    try:
        connection = sqlite3.connect ( 'bioreattore.db' )
        c = connection.cursor ( )
        c.execute ( '''CREATE TABLE bioreattore( data TEXT , valore REAL, colonna INT, funzione TEXT)''' )
        connection.commit ( )
    except Error as e:
        print(e)
    finally:
        connection.close()



################################ FUNZIONI ##########################
def shutdown ( ):  # Definisco uno shutdown se premo 2 secondi un bottone
    check_call ( [ 'sudo' , 'poweroff' ] )


# tutte le funzioni mi restituiscono (data, valore, colonna)
# quelle che non hanno un valore restituiscono il record dell'input
# le funzioni della luce registrano quando vengono disattivate
# scrittura
def db (data,valore,colonna,funzione):
    try:
        #CHIAMA UNA FUNZIONE inserendo il suo nome come stringa
        # con libreria foo e bar
        # valore , colonna , data, funzione = funzione()
        conn = sqlite3.connect ( 'bioreattore.db' )
        c.execute ( "INSERT INTO bioreattore VALUES (data,valore,colonna)" ) , (data , valore , colonna, funzione)  # scrivo nel db
        conn.commit ( )  # Save (commit) the changes
    except Error as e:
        print(e)
    finally:
        connection.close()
########## FUNZIONI  ############
# Voglio fare un bottone che attiva lo start della funzione main
# Tutti i pin adesso sono sballati inserire tutti i pin quando sara' pronto
# LISTA FUNZIONI=[salinity,temperature,food,ph,air,light,od,reservoir]
def ora ( ):
    time = localtime ( )
    time = self.time[ ::-1 ]
    time = self.time[ 3: ]  # sec/min/ora/giorno/mese/anno
    return (time)

def bioreattore_pin ( num , pin ):
    # prendo il numero della colonna in int
    # prendo nome pin in str, e restitisco numero pin
    if num == 1 and pin =='reservoir':
        return (1)
    elif num == 1 and pin =='food':
        return (2 , 3)  # pin del cibo della colonna 1
    elif num == 1 and pin=='air':
        return (1)  # pin che controlla l'aria
    elif num == 1 and pin=='light':
        return (1 , 2 , 3)  # RGB
    elif num == 1 and pin=='salinity':
        return (1 , 2 , 3 , 4)  # solenoide_1, solenoide_2, transistor, lettura
    elif num == 1 and pin=='temperature':
        return (1 , 2 , 3)  # pin_temperatura, pin_caldo, pin_freddo
    elif num == 1 and pin=='ph':
        return (1)
    elif num == 1 and pin=='od':
        return (1 , 2)  # RGB
    # TOTALE PIN 17 per ogni COLONNA

def od ( colonna , num_misure , intervallo_misure ):
    # imposto classe pin
    # essential for reports
    # setto variabili
    laser_pin , fotoresistenza_pin = bioreattore_pin ( colonna , 'od' )
    board.analog[ fotoresistenza_pin ].enable_reporting ( )
    counter = 0
    lista_misure = [ ]
    while num_misure > counter:
        board.digital[ laser_pin ].write ( 1 )
        misurazione_od = board.analog[ fotoresistenza_pin ].read ( )  # leggo
        sleep ( intervallo_misure / 2 )
        board.digital[ laser_pin ].write ( 0 )
        sleep ( intervallo_misure / 2 )
        # creo lista di valori misurazioni
        lista_misure.extend ( [ misurazione_od ] )
        counter += 1
    misura = np.mean ( lista_misure )
    # inserire anche un intervallo di confidenza stimato
    # oppure errore della misura nella lista
    board.analog[ fotoresistenza_pin ].disable_reporting ( )
    t = ora ( )
    db(t , misura , colonna , 'od')
########## FUNZIONE LUCE  ########################
# trovare modo per accendere una ed automaticamente spengere l'altra
# possibile fare con flag=[1,2,3] tutto in una funzione
# stessa cosa con bioreattori

def pulse ( colonna , delay , R , G , B , light_on , percentuale_tempo_acceso ):
    flag=1 #flag 1 per pulse, 2 per fade, 3 per continue
    valore_R = R * 255 / 100  # trasformo intensita' percentuale
    valore_G = G * 255 / 100  # in una che arduino puo' comprendere
    valore_B = B * 255 / 100  # per RBerry invece essendo da 1/100 non ho bisogno
    pinR , pinG , pinB = bioreattore_pin ( colonna , 'light' )
    while light_on == True and flag==1:
        # DELAY= Percentuale del tempo acceso
        board.analog[ pinR ].write ( valore_R )  # accendo fino al valore voluto di intensita'
        board.analog[ pinG ].write ( valore_G )  # che passo come R,G,B, per esempio in %
        board.analog[ pinB ].write ( valore_B )  # ma riconverto in valori che Arduino o Raspberry possono gestire
        sleep (
            percentuale_tempo_acceso / 100 )  # aspetto tempo richiesto dato dalla percentuale alla frazione di secondo
        board.analog[ pinR ].write ( 0 )
        board.analog[ pinG ].write ( 0 )
        board.analog[ pinB ].write ( 0 )
        sleep ( 1 - percentuale_tempo_acceso / 100 )  # aspetta
    flag = 0
    t = ora ( )
    db ( t , 0 , colonna , 'light pulse' )
def fade ( colonna , R , G , B , freq , light_on ):
    pinR , pinG , pinB = bioreattore_pin ( colonna , 'light' )
    valore_R = R * 255 / 100  # trasformo intensita' da percentuale
    valore_G = G * 255 / 100  # in una che arduino puo' comprendere
    valore_B = B * 255 / 100  # per RBerry invece essendo da 1/100 non ho bisogno
    delay = 1 / (2 * freq)  # espressa in secondi # posso fare delay diviso due se intendo che in un secondo
    # mi deve fare "valore inserito " di cilci acceso e spento
    # posso impostare anche percentuale del tempo di attesa_on/off
    increment_r = valore_R / 128  # incrementi per arrivare al massimo dopo 128 passi e poi altri 128 in cui scende
    increment_g = valore_G / 128  # 512 su RBerry
    increment_b = valore_B / 128
    val_led= [0, 0 , 0]
    flag=2
    while light_on == True and flag==2:
        if val_led[0]<valore_R and valori_led[1]<valore_G and valori_led[2]<valore_B:
            board.analog[ pinR ].write ( valore_R )  # accendo fino al valore voluto di intensita'
            board.analog[ pinG ].write ( valore_G )  # che passo come R,G,B, per esempio in %
            board.analog[ pinB ].write ( valore_B )  # ma riconverto in valori che Arduino o Raspberry possono gestire
            sleep ( 1 / delay )  # aspetto tempo richiesto dato, delay e' il periodo
            val_led[ 0 ] += increment_r
            val_led[ 1 ] += increment_g
            val_led[ 2 ] += increment_b
        elif val_led[0]>valore_R and valori_led[1]> valore_G and valori_led[2]> valore_B:
            board.analog[ pinR ].write ( valore_R )  # accendo fino al valore voluto di intensita'
            board.analog[ pinG ].write ( valore_G )  # che passo come R,G,B, per esempio in %
            board.analog[ pinB ].write ( valore_B )  # ma riconverto in valori che Arduino o Raspberry possono gestire
            sleep ( 1 / delay )  # aspetto tempo richiesto dato, delay e' il periodo
            val_led[0]-= increment_r
            val_led[1] -=increment_g
            val_led[2] -= increment_b
        else:
            continue
    flag=0
    t = ora ( )
    return (t , 0 , colonna)
def continua ( colonna , R , G , B , light_on ):
    pinR , pinG , pinB = bioreattore_pin ( colonna , 'light' )
    flag=3
    while light_on == True and flag==3:
        valore_R = R * 255 / 100  # trasformo intensita' da percentuale
        valore_G = G * 255 / 100  # in una che arduino puo' comprendere
        valore_B = B * 255 / 100  # per RBerry invece essendo da 1/100 non ho bisogno
        board.analog[ self.pinR ].write ( valore_R )
        board.analog[ self.pinG ].write ( valore_G )
        board.analog[ self.pinB ].write ( valore_B )
    flag = 0
    # light_on=0 #si spenge a questa ora
    t = ora ( )
    db(t , 0 , colonna, 'light continue')

def air ( colonna , on ):
    pin_aria = bioreattore_pin ( colonna , 'air' )
    if on == True:
        board.digital[ pin_aria ].write ( 1 )
        db ( t , 1 , colonna , 'air' )
    else:
        board.digital[ pin_aria ].write ( 0 )
        db (t ,0 , colonna,'air')

def food ( quanto_togliere , colonna ):
    # voglio farli separati i controlli dell'solenoide
    tempo_attesa = quanto_togliere / portata  # portata [ml/s]
    pin_up , pin_down = bioreattore_pin ( colonna , 'food' )
    board.digital[ pin_up ].write ( 1 )
    board.digital[ pin_down ].write ( 1 )
    sleep ( tempo_attesa )  # riempimento coltura in contemporanea dello svuotamento
    board.digital[ pin_up ].write ( 0 )
    board.digital[ pin_down ].write ( 0 )  # svuotamento
    #sleep ( tempo_attesa )
    #board.digital[ pin_down ].write ( 0 )
    t = ora ( )
    db (t , quanto_togliere , colonna,'food')

def reservoir ( colonna , quanto_togliere ):
    tempo_attesa = quanto_togliere / portata  # portata [ml/s]
    pin_reservoir = bioreattore_pin ( colonna , "reservoir" )  # FUNZIONE DA IMPLEMENTARE
    board.digital[ pin_reservoir ].write ( 1 )
    sleep ( tempo_attesa )  # passa l'aggiunta alla colonna
    board.digital[ pin_reservoir ].write ( 0 )
    t = ora ( )
    db (t , quanto_togliere , colonna,'reservoir')

def ph ( colonna ):
    ph_pin = bioreattore_pin ( colonna , 'ph' )
    board.analog[ ph_pin ].enable_reporting ( )
    #board.analog[ ph_pin ].write ( 1 )  # accendo
    misurazione_ph = board.analog[ 1 ].read ( )  # leggo
    #board.digital[ ph_pin ].write ( 0 )  # spengo
    board.analog[ ph_pin ].disable_reporting ( )
    t = ora ( )
    db (t , misurazione_ph , colonna,'ph' )

def temperature ( colonna , temp , range_temp ): #sempre on per controllare Temperatura
    # imposto la temperatura per colonna nella main
    # richiamo la funzione inserendo numero colonna, temperatura e range
    # range_temp nella main = oscillazione temperatura massima ex +-1 grado
    pin_temperatura , pin_caldo , pin_freddo = bioreattore_pin ( colonna , 'temperature' )
    # freddo = cella di peltier
    # caldo = fascia riscaldante
    # value sono i valori della temperatura
    # tempo per prendere le misure a tot tempo
    board.analog[ pin_temperatura ].enable_reporting ( )
    value = board.analog[ pin_temperatura ].read ( )  # prima leggo e confronto
    # confronto temperatura con range impostato
    while True: #controlla sempre la temperatura
        if value > temperatura + range_temp / 2:  # fa caldo!
            board.digital[ pin_freddo ].write ( 1 )  # accendo peltier
            sleep ( 60 )  # tengo 60 sec
            board.digital[ pin_freddo ].write ( 0 )
        if value < temperatura - range_temp / 2:  # fa freddo!
            board.digital[ pin_caldo ].write ( 1 )  # accendo la fascia
            sleep ( 60 )
            board.digital[ pin_caldo ].write (0)
        sleep(10)


def misura_temperatura(colonna , temp , range_temp):
    pin_temperatura , pin_caldo , pin_freddo = bioreattore_pin ( colonna , 'temperature' )
    board.analog[ pin_temperatura ].enable_reporting ( )
    value = board.analog[ pin_temperatura ].read ( )
    board.analog[ pin_temperatura ].disable_reporting ( )
    t = ora ( )
    db (t , value , colonna,'temperature')

def salinity ( colonna ):
    tempo_riempimento=volume/portata #calcolo empirico!
    solenoide_1 , solenoide_2 , transistor , lettura = bioreattore_pin ( colonna , 'salinity' )  # pin
    board.analog[ lettura ].enable_reporting ( )
    # tempo_riempimento= volume camera/portata
    # faccio passar corrente con un transistor
    # lettura a valle della corrente che passa
    board.digital[ solenoide_1 ].write ( 1 )  # apro e chiudo il solenoide
    sleep ( tempo_riempimento )
    board.digital[ solenoide_1 ].write ( 0 )
    board.digital[ transistor ].write ( 1 )  # attivo transistor e faccio passare corrente
    sleep ( 0.5 )  # permette letture piu' pulite
    misura_salinity = board.analog[ lettura ].read ( )  # leggo
    sleep ( 0.05 )
    board.digital[ transistor ].write ( 0 )  # tolgo la corrente
    board.digital[ solenoide_2 ].write ( 1 )  # svuoto
    sleep ( tempo_riempimento )
    board.digital[ solenoide_2 ].write ( 0 )  # chiudo
    board.analog[ lettura ].disable_reporting ( )
    t = ora ( )
    db(t , misura_salinity , colonna, 'salinity')


# ________________CICLO____________________________________________
if __name__ == '__main__':  # Se imposto la funzione principale parte
    shutdown_btn = Button ( 17 , hold_time=2 )  # bottone shutdown pin 17
    shutdown_btn.when_held = shutdown
    pause ( )
# LISTA FUNZIONI=[salinity,temperature,solenoid_valve,ph,air,light,od]
# Definire sezione temporale per la lettura di questo codice
#    freq_salinity, freq_temp, freq_cibo,freq_ph,freq_od.
# prendo le frequenze di ogni funzione dall'database dell'utente
# le setto come intervallo delle funzioni
# trasformo valore di una frequenza giornaliera in secondi di delay
    sec_salinity = freq_salinity / 1440  # 1440=min in 24h
    sec_temp = freq_tem / 1440
    sec_cibo = freq_cibo / 1440  # solenoid_valve
    sec_ph = freq_ph / 1440
    sec_od = freq_od / 1440

def run_threaded ( job_func ):
    job_thread = threading.Thread ( target=job_func )
    job_thread.start ( )

schedule.every ( sec_salinity ).minutes.do ( run_threaded , salinity ( ) )
schedule.every ( sec_temp ).minutes.do ( run_threaded , temperature ( n_col , temp , range_temp ) )
schedule.every ( sec_cibo ).minutes.do ( run_threaded , solenoid_valve ( quanto_togliere , colonna ) )
schedule.every ( sec_ph ).minutes.do ( run_threaded , ph )
schedule.every ( sec_od ).minutes.do ( run_threaded , od ( num_misure , colonna ) )

# ogni funzione deve avere come argomento anche in numero della colonna
# per risparmiare tempo posso accendere la funzione ex temperatura per 60 sec
# e poi passare ad altro, cercare di non creare sleep all'interno della funzione
air ( on , n_col )
# sistemare aria con nanoArduino
while True:  # <------ partenza processo, sempre attivo
    schedule.run_pending ( )
    time.sleep ( 1 )
    # Devo calcolare i 2 tipi di multiprocesso che voglio attivare
    # p.e. optical_density non concorda con gli altri processi, effettivamente
    # SALVA DATI - non so dove metterla? nel processo dopo ogni programma

