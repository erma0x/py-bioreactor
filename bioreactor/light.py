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
        

def pulse( colonna , delay , R , G , B , light_on , percentuale_tempo_acceso ):
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


def continous_light( colonna , R , G , B , light_on ):
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