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