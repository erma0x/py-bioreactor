#Gestisce la funzione con la lunghezza dei programmi
if __name__ == '__main__':
    #Setto i Pin del Raspberry Pi
    import RPi.GPIO as GPIO
    import time
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    #attivo il multiprocesso
    jobs = []
    programs=['pHmeter','change_terrain','saltinity_meter','optical_density'
    for i in range(len(programs)):
        p = multiprocessing.Process(target=main)
              #faccio partire il main che contiene tutti i programmi assieme
        jobs.append(p)
        p.start()

    
