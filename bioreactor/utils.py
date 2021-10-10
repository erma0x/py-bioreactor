def shutdown():  # Definisco uno shutdown se premo 2 secondi un bottone
    check_call([ 'sudo' , 'poweroff' ])
    
    
def create_db():
    try:
        connection = sqlite3.connect ('bioreactor.db')
        c = connection.cursor ( )
        c.execute ( '''CREATE TABLE bioreattore( data TEXT , valore REAL, colonna INT, funzione TEXT)''' )
        connection.commit ( )
    except Error as e:
        print(e)
    finally:
        connection.close()
        
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

def equispaced(low,up,leng):  
    #Funzione che crea lista di valori equispaziati
    #Per gestire tante misurazioni in breve tempo per poi fare la media
    list = []
    step = (up - low) / float(leng)
    for i in range(leng):
        list.append(low)
        low = low + step
    return list


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