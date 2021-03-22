# Funzioni del Bioreattore
# Laser / "optical_density"

# Slinita / "saltinity_meter"
# Carico / Scarico "change_terrain"
# pH_meter
#Faccio finta che i pin sono

def pH_meter():

def equispaced(low,up,leng):  #Funzione che crea lista di valori equispaziati
    #Per gestire tante misurazioni in breve tempo per poi fare la media
    list = []
    step = (up - low) / float(leng)
    for i in range(leng):
        list.append(low)
        low = low + step
    return list

misurazione_od=[]
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
#DATO= | misura | mese , giorno, ora,minuti, secondi | secondi del processo | num misura
    time.sleep(delay) #aspetta fino a prossima misura
