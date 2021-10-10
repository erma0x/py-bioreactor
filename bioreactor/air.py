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
        
    
def air(colonna ,on):
    pin_aria = bioreattore_pin ( colonna , 'air' )
    if on == True:
        board.digital[ pin_aria ].write ( 1 )
        db( t , 1 , colonna , 'air' )
    else:
        board.digital[ pin_aria ].write ( 0 )
        db(t ,0 , colonna,'air')