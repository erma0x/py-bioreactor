def salinity( colonna ):
    tempo_riempimento=volume/portata #calcolo empirico!
    solenoide_1 , solenoide_2 , transistor , lettura = bioreattore_pin ( colonna , 'salinity' )  # pin
    board.analog[ lettura ].enable_reporting ( )
    # tempo_riempimento= volume camera/portata
    # faccio passar corrente con un transistor
    # lettura a valle della corrente che passa
    board.digital[ solenoide_1 ].write ( 1 )  # apro e chiudo il solenoide
    sleep(tempo_riempimento )
    board.digital[ solenoide_1 ].write ( 0 )
    board.digital[ transistor ].write ( 1 )  # attivo transistor e faccio passare corrente
    sleep( 0.5 )  # permette letture piu' pulite
    misura_salinity = board.analog[ lettura ].read ( )  # leggo
    sleep( 0.05 )
    board.digital[ transistor ].write ( 0 )  # tolgo la corrente
    board.digital[ solenoide_2 ].write ( 1 )  # svuoto
    sleep ( tempo_riempimento )
    board.digital[ solenoide_2 ].write ( 0 )  # chiudo
    board.analog[ lettura ].disable_reporting ( )
    t = ora ( )
    db(t , misura_salinity , colonna, 'salinity')
    
def salinity():
    solenoide_1, solenoide_2, transistor ,lettura=1,2,3,4 #pin
    board.analog[4].enable_reporting()
    global misura_salinity
    #tempo_riempimento= volume camera/portata
    #faccio passar corrente con un transistor
    #lettura a valle della corrente che passa
    board.digital[1].write(1) #apro e chiudo il solenoide
    sleep(tempo_riempimento)
    board.digital[1].write(0)
    
    board.digital[3].write(1) #attivo transistor e faccio passare corrente
    sleep(0.5) #permette letture piu' pulite
    misura_salinity=board.analog[4].read() #leggo
    
    board.digital[2].write(1) #svuoto
    sleep(tempo_riempimento)
    board.digital[2].write(0)
    
    
    