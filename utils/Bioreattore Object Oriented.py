################# OGGETTI ############

class Bioreattore:
    def __init__(self,colonna,misura, ora, on,time):
        # type: (object, object, object, object, object) -> object
        self.colonna=colonna
        self.misura=misura
        self.ora=ora
        self.on=on
        self.time = localtime ()
    def set_pin(self,pin=[],push=1):
        #Posso metterli in ordine
        #Impostare tutti i pin di tutto
        self.colonna=input('Inserisci il numero della colonna (1,2,3) : ' )
        while push in range(0,60):
            push=input('''Inserisci i pin del Bioreattore:
            1 - temperatura 
            2 - pH
            3 - LED 
            4 - pompa aria
            5 - cibo
            6 - reservoir
            7 - salinometro
            ''')
            if push==3:
                pin_R, pin_G, pin_B
                    
class ora(Bioreattore):
    Bioreattore.__init__ (self, colonna, misura, ora, on)
    def __init__(self, time=0):
        self.time = time
    def ora(self):
        self.time = localtime ()
        self.time = self.time[::-1]
        time = self.time[3:]
        # rint(time)# sec/min/ora/giorno/mese/anno
        return (time)
    #now=ora.ora() -> DB
#colonna_1.termometro.ora() bioreattore -> metodo termometro e dentro c'e' ora.
#definisco per ogni sensore che ho una sottoclasse del bioreattore

class od(Bioreattore):
        def __init__(self,sensore,num_misure,pin_fotoresistenza,pin_transistor,tempo_attesa,check:
            Bioreattore.__init__(self,colonna, misura, ora, on)
            self.check = check
            self.sensore = sensore
            self.pin_fotoresistenza = pin_fotoresistenza
            self.pin_transistor = pin_transistor
            self.num_misure =num_misure
            self.tempo_attesa=tempo_attesa #attesa fra un impulso e l'altro (0.1ms)
        def lettura(self):
            # sesor_index = ('a:{}:i').format(self.pin_fotoresistenza)  # pinMode
            # sensor = board.get_pin(sesor_index)
            # laser_index=('d:{}:o').format(self.pint_transistor)
            # laser= board.get_pin(laser_index)
            # essential for reports
            board.analog[self.pin_fotoresistenza].enable_reporting()
            counter = 0
            lista_misure = [] # setto variabili
            while self.num_misure > counter:
                board.digital[self.pin_transistor].write(1)
                misurazione_od = board.analog[self.pin_fotoresistenza].read()  # leggo
                sleep(self.tempo_attesa)
                board.digital[7].write(0)
                sleep(0.1)
                misurazione_od = board.analog[1].read()
                # creo lista di valori misurazioni
                lista_misure.append(misurazione_od)
                counter += 1
            misura = np.mean(lista_misure)
            # inserire anche un intervallo di confidenza stimato
            # oppure errore della misura nella lista
            return (misura)
            
class light(Bioreattore):
    def __init__(self, misura, ora, on, frequenza, R, G, B, funzione, pinR, pinG, pinB, ciclo24h, light_on):
        Bioreattore.__init__(self,colonna,misura, ora, on,time)
        self.R=R
        self.G=G
        self.B=B
        self.frequenza=frequenza
        self.funzione=funzione
        self.pinR=pinR
        self.pinG=pinG
        self.pinB=pinB
        self.light_on=light_on
    lista_funzioni=[fade, pulse, continua]

    def pulse(self,delay):
            if self.funzione == 'pulse'and self.on == True and light_on==True:
                #PULSE
                valore_R = R * 255 / 100  # trasformo intensita' percentuale
                valore_G = G * 255 / 100  # in una che arduino puo' comprendere
                valore_B = B * 255 / 100  # per RBerry invece essendo da 1/100 non ho bisogno

                while self.on==True:
                    #DELAY= Percentuale del tempo acceso
                    board.analog[self.pinR].write(valore_R) #accendo fino al valore voluto di intensita'
                    board.analog[self.pinG].write(valore_G)  # che passo come R,G,B, per esempio in %
                    board.analog[self.pinB].write(valore_B) # ma riconverto in valori che Arduino o Raspberry possono gestire
                    sleep(delay/100) #aspetto tempo richiesto dato dalla percentuale alla frazione di secondo
                    board.analog[self.pinR].write(0)
                    board.analog[self.pinG].write(0)
                    board.analog[self.pinB].write(0)
                    sleep(1-delay/100) #aspetta

    def fade(self,periodo):
        if self.funzione == 'fade' and self.on == True and light_on==True:

            valore_R = self.R * 255 / 100  # trasformo intensita' da percentuale
            valore_G = self.G * 255 / 100  # in una che arduino puo' comprendere
            valore_B = self.B * 255 / 100  # per RBerry invece essendo da 1/100 non ho bisogno
            delay = 1 / (2 * freq)  # espressa in secondi # posso fare delay diviso due se intendo che in un secondo
            # mi deve fare "valore inserito " di cilci acceso e spento
            # posso impostare anche percentuale del tempo di attesa_on/off
            increment_r = valore_R / 128  # incrementi per arrivare al massimo dopo 128 passi e poi altri 128 in cui scende
            increment_g = valore_G / 128  # 512 su RBerry
            increment_b = valore_B / 128

            while self.on == True and  < valore:
                board.analog[self.pinR].write(valore_R)  # accendo fino al valore voluto di intensita'
                board.analog[self.pinG].write(valore_G)  # che passo come R,G,B, per esempio in %
                board.analog[self.pinB].write(valore_B)  # ma riconverto in valori che Arduino o Raspberry possono gestire
                sleep(1/delay)  # aspetto tempo richiesto dato, delay e' il periodo

    def continua(self,R,G,B):
        while self.funzione == 'continua' and self.on == True and self.light_on==True:
            valore_R = R * 255 / 100  # trasformo intensita' da percentuale
            valore_G = G * 255 / 100  # in una che arduino puo' comprendere
            valore_B = B * 255 / 100  # per RBerry invece essendo da 1/100 non ho bisogno

            board.analog[self.pinR].write(valore_R)
            board.analog[self.pinG].write(valore_G)
            board.analog[self.pinB].write(valore_B)
            #### DESCRIZIONI LUCI ##########3
            # R sta per intensita' del led rosso con PWM, mentre pinR e' il pin per controllarlo
            # Funzioni per luce = PULSE / FADE / CONTINOUS
            # pulse_on per emettere luce discreta con intensita' date
            # fade_on la luce viene mandata gradualmente
            # accendere anche i led in modo differenziale r->g->b
            # daily_cycle tempo su 24 quanto restare acceso
            # freq [Hz] di emissione luce
            # ri,gi,bi sono le intensita' dei vari colori [0:100] %
            # devo farlo con transistor e batteria, perche' richiedono >5V
            # in pwm gestisco le intensita' RGB dato che sono 3 canali diversi
            # se lo connetto al digitale che ha pwm e gli do i valori che voglio io
            # nel range di 0/1024 con raspberry e 0/255 con Arduino
            # 1% duty cycle di risoluzione

            ###############################
class solenoid(Bioreattore):
    Bioreattore.__init__( self , colonna,v alore, ora, on)
    def __init__(self, quanto_togliere, colonna, solenoid_on, *pin_apertura, *pin_chiusura):
        self.quanto_togliere=quanto_togliere
        self.pin_chiusura = pin_chiusura
        self.pin_apertura = pin_apertura
        self.solenoid_on=solenoid_on

#uso del solenoide per cibo/scarto + misure analisi + reservoir + salinita

    def Food(self):
            # voglio farli separati i controlli dell'solenoide
            # funzioni divere per cibo
        while solenoid_on and on ==True:
            tempo_attesa = self.quanto_togliere / portata  # portata [ml/s]
            for i in self.pin_apertura:
                board.digital[int(i)].write(1)
            for i in self.pin_chiusura:
                board.digital[int(i)].write(0)
            sleep(tempo_attesa)
            for i in self.pin_apertura:
                board.digital[int(i)].write(0)
            for i in self.pin_chiusura:
                board.digital[int(i)].write(1)


            for i in
            sensor = board.get_pin('d:{}:o')
            sensor = board.get_pin('d:{}:o')
            tempo_solenoid = localtime()
            board.digital[1].write(1)
            board.digital[2].write(1)
            sleep(tempo)
            check = board.analog[check_pin].read()
            board.digital[1].write(0)
            board.digital[2].write(0)

    def food(self):
class air(Bioreattore):
    def __init__(self, misura, ora, on, pin, frequenza, intensity, aria_on):
        Bioreattore.__init__(self,colonna,misura, ora, on,time)
        self.pin=pin
        self.frequenza=frequenza
        self.colonna=colonna
        self.intensity=intensity
        self.aria_on=aria_on
        intens= self.intensity * 255 / 100 # valore che board puo'capire
    def aria(self):
        while self.on==True and self.aria_on==True:
            board.analog[self.pinR].write(intens)
class temperatura(Bioreattore):

