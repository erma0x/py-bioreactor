def ph( colonna ):
    ph_pin = bioreattore_pin ( colonna , 'ph' )
    board.analog[ ph_pin ].enable_reporting ( )
    #board.analog[ ph_pin ].write ( 1 )  # accendo
    misurazione_ph = board.analog[ 1 ].read ( )  # leggo
    #board.digital[ ph_pin ].write ( 0 )  # spengo
    board.analog[ ph_pin ].disable_reporting ( )
    t = ora ( )
    db (t , misurazione_ph , colonna,'ph' )