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
    t = ora()
    db (t , value , colonna,'temperature')
    

def temperature(n_col,temp,range_temp):
    #imposto la temperatura per colonna nella main
    #richiamo la funzione inserendo numero colonna, temperatura e range
    #range_temp nella main = oscillazione temperatura massima ex +-1 grado
    pin_temp_1,pin_temp_2,pin_temp_3=1,2,3
    pin_endo_1,pin_endo_2,pin_endo_3=4,5,6
    pin_eso_1,pin_eso_2,pin_eso_3=7,8,9
    #endo = cella di peltier
    #eso = fascia riscaldante
    #value sono i valori della temperatura
    #tempo per prendere le misure a tot tempo
    board.analog[1].enable_reporting()
    board.analog[2].enable_reporting()
    board.analog[3].enable_reporting()
    sensor_col_1=board.get_pin('a:1:i') # pinMode
    sensor_col_2=board.get_pin('a:2:i') # non ho capito se sono 
    sensor_col_3=board.get_pin('a:3:i') #evitabili queste assegnazioni
    if n_col==1:
        value_1=board.analog[1].read()
        tempo_1temp=localtime()
        if value_1>temperatura+range_temp/2:
            board.digital[7].write(1) #accendo peltier
            sleep(60) #tengo 60 sec
            board.digital[7].write(0)
        elif  value_1<temperatura-range_temp/2:
            board.digital[4].write(1) #accendo la fascia
            sleep(60)
            board.digital[4].write(0)
        else:
            pass
        return(value_1,tempo_1)
    elif n_col==2:
        value_2=board.analog[2].read()
        tempo_2_temp=localtime()
        if value_2>temperatura+range_temp/2:
            board.digital[8].write(1) #accendo peltier
            sleep(60) #tengo 60 sec
            board.digital[8].write(0)
        elif  value_2<temperatura-range_temp/2:
            board.digital[5].write(1) #accendo la fascia
            sleep(60)
            board.digital[5].write(0)
        else:
            pass
        return(value_2,tempo_2)
    elif n_col==3:
        value_3=board.analog[3].read()
        tempo_3_temp=localtime()
        if value_3>temperatura+range_temp/2:
            board.digital[9].write(1) #accendo peltier
            sleep(60) #tengo 60 sec
            board.digital[97].write(0)
        elif  value_3<temperatura-range_temp/2:
            board.digital[6].write(1) #accendo la fascia
            sleep(60)
            board.digital[6].write(0)
        else:
            pass
        return(value_3,tempo_3)
        
    else:
        print('valore numero colonna "n_col" sbagliato')
        pass