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
from pyfirmata import *
from time import *

import scheduler

def settings():
    x='Y'
    while x=='Y' or x=='y':
        name_function=input('''Which function do you want to set? 
        1 - Optical Density
        2 - Food
        3 - Salinity
        4 - PH
        4 - Reservoir
        5 - Light
        6 - 
        ''')
        if name_function==1:
            col=input('Which column do you want to set? - ')
            num_day=input('How many times at day do you want to measure OD? - ')
        if name_function==2:
            col = input ( 'Which column do you want to set? - ' )
            num_day = input ( 'How many times at day do you want to measure OD? - ' )
        if name_function==3:
            col = input ( 'Which column do you want to set? - ' )
            num_day = input ( 'How many times at day do you want to measure OD? - ' )
        if name_function==4:
            col = input ( 'Which column do you want to set? - ' )
            num_day = input ( 'How many times at day do you want to measure pH? - ' )
        if name_function==5:
            col = input ( 'Which column do you want to set? - ' )
            num_day = input ( 'How many times at day do you want to measure OD? - ' )
        if name_function==6:
            col = input ( 'Which column do you want to set? - ' )
            num_day = input ( 'How many times at day do you want to measure OD? - ' )


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
              
def air(on, n_col):
    # n_col is the number of the column

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

def shutdown( ):  # Definisco uno shutdown se premo 2 secondi un bottone
    check_call( [ 'sudo' , 'poweroff' ] )
    
def analisi_rubinetto(num_misure):
    """
    I want a function that calculates how much to hold
    opened the tap to withdraw tot ml, and then
    pass them to nourishment, for example, I want to do some analyzes
    on a column to plate them or incubate them and then I want that
    by pressing a button you take me tot ml, it would always be with a solenoid valve
    but with bottleneck, empirical evidence to establish scope
    I press a button to get the sample and finished pressing the solenoid valve
    closes. I want to know how much I have withdrawn
    
    To the liquid I have to go and add it to the liquid that the culture has lost
    in the next food session.
    """
    #portata=*** #Calcolare empiricamente
    
    pin_bottone=1
    elettrovalvola=2
    sensor=board.get_pin('d:1:i') # pinMode
    board.digital[pin_bottone].enable_reporting()
    if board.digital[1].read()==1:
        tempoi=localtime()
        
        while board.digital[1].read()==1:
            board.digital[2].write(1)
        
        tempof=localtime()
    
    tempo_totale=tempof-tempoi #liq=t*p
    liq=tempo_totale*portata
    
    return liq

def equispaced(low,up,leng):  #Funzione che crea lista di valori equispaziati
    #Per gestire tante misurazioni in breve tempo per poi fare la media
    list = []
    step = (up - low) / float(leng)
    for i in range(leng):
        list.append(low)
        low = low + step
    return list


def optical_density(frequenza_misurazioni_giorno, pin_laser,pin_fotoresistenza,
                    num_misurazioni_volta, tempo_misurazione):
    #__SETUP_______________
    t0 = time.clock() #controllo quanto tempo ci mette il processo
    delay=frequenza_misurazioni_giorno/86400 #secondi in un giorno
    GPIO.setmode(GPIO.BCM)            # choose BCM or BOARD
    GPIO.setup(pin_laser, GPIO.OUT)  # set a port/pin as an input
    GPIO.setup(pin_fotoresistenza, GPIO.IN) # set a port/pin as an output
    # inserire la serie di misurazioni
    # fai la media delle misurazioni e restituiscile
    #__MAIN____________
    start = timeit.timeit() #prendo il tempo
    global misurazione_od
    #step=distanza_serie_misurazioni/tempo_misurazione #step di tempo
    #lista_temporale=equispaced(0,tempo_misurazione,num_misurazioni_volta) #dorme in secondi
    #p.e. voglio 30 misurazioni
    counter=0
    while misurazioni>counter: # faccio 1 lettura,  1 ms delay, a ciclo
        GIPO.output(pin_laser,1) #faccio partire il laser
        misurazione_od=GPIO.input(pin_fotoresistenza) #leggo valori
        tempo_misurazione.extend([misurazione_od]) #creo lista di valori misurazioni
        GIPO.output(pin_laser,0)
        time.sleep(0.001) # delay 1ms
        counter+=1

    #crea lista con valori
    #calcola media e restituiscila
    misura=mean(tempo_misurazione)
    tempo=time.localtime()
    tempo_finale_processo = time.clock() #fine processo
    return(misura,tempo[1:6],tempo_finale_processo, counter)

def create_db():
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


def ph( colonna ):
    ph_pin = bioreattore_pin ( colonna , 'ph' )
    board.analog[ ph_pin ].enable_reporting ( )
    #board.analog[ ph_pin ].write ( 1 )  # accendo
    misurazione_ph = board.analog[ 1 ].read ( )  # leggo
    #board.digital[ ph_pin ].write ( 0 )  # spengo
    board.analog[ ph_pin ].disable_reporting ( )
    t = ora ( )
    db (t , misurazione_ph , colonna,'ph' )


def temperature( colonna , temp , range_temp ): #sempre on per controllare Temperatura
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

def salinity( colonna ):
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

def run_threaded ( job_func ):
    job_thread = threading.Thread ( target=job_func )
    job_thread.start ( )

    schedule.every( sec_salinity ).minutes.do ( run_threaded , salinity ( ) )
    schedule.every( sec_temp ).minutes.do ( run_threaded , temperature ( n_col , temp , range_temp ) )
    schedule.every( sec_cibo ).minutes.do ( run_threaded , solenoid_valve ( quanto_togliere , colonna ) )
    schedule.every( sec_ph ).minutes.do ( run_threaded , ph )
    schedule.every( sec_od ).minutes.do ( run_threaded , od ( num_misure , colonna ) )
    
if __name__ =='__main__':

    # RASPBERRY
    GPIO.setmode ( GPIO.BOARD )  # 2 modi:  BCM or BOARD
    GPIO.setwarnings ( False )
    GPIO.setup ( port_or_pin , GPIO.IN )  # set a port/pin as an input
    GPIO.setup ( port_or_pin , GPIO.OUT )  # set a port/pin as an output
    GPIO.add_event_detect ( Button , GPIO.RISING , callback=main )
    
    # ARDUINO
    port = "COM3"
    board = Arduino(port)
    it = pyfirmata.util.Iterator(board)
    it.start()

    #### INIZIALIZZO DB ####
    globals(db_file)
    
    shutdown_btn = Button ( 17 , hold_time=2 )  # bottone shutdown pin 17
    shutdown_btn.when_held = shutdown
    pause ( )

    sec_salinity = freq_salinity / 1440  # 1440=min in 24h
    sec_temp = freq_tem / 1440
    sec_cibo = freq_cibo / 1440  # solenoid_valve
    sec_ph = freq_ph / 1440
    sec_od = freq_od / 1440


