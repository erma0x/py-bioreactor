def waste( colonna , quanto_togliere ):
    tempo_attesa = quanto_togliere / portata  # portata [ml/s]
    pin_reservoir = bioreattore_pin ( colonna , "reservoir" )  # FUNZIONE DA IMPLEMENTARE
    board.digital[ pin_reservoir ].write ( 1 )
    sleep ( tempo_attesa )  # passa l'aggiunta alla colonna
    board.digital[ pin_reservoir ].write ( 0 )
    t = ora ( )
    db (t , quanto_togliere , colonna,'reservoir')