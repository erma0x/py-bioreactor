def init_raspberry():
    #  RASPBERRY
    GPIO.setmode ( GPIO.BOARD )  # 2 modi:  BCM or BOARD
    GPIO.setwarnings ( False )
    GPIO.setup ( port_or_pin , GPIO.IN )  # set a port/pin as an input
    GPIO.setup ( port_or_pin , GPIO.OUT )  # set a port/pin as an output
    GPIO.add_event_detect ( Button , GPIO.RISING , callback=main )
    
def init_arduino():
    #  ARDUINO
    port = "COM3"
    board = Arduino ( port )
    it = pyfirmata.util.Iterator ( board )
    it.start()


def onOffFunction():
    arduino = serial.Serial('/dev/tty.usbmodem1411', 9600)

    command = input("Type something..: (on/ off / bye )")
    if command =="on":
        print("The LED is on...")
        time.sleep(1)
        arduino.write('H')
        onOffFunction()
    elif command =="off":
        print("The LED is off...")
        time.sleep(1)
        arduino.write('L')
        onOffFunction()
    elif command =="bye":
        print ("See You!...")
        time.sleep(1)
        arduino.close()
    else:
        print ("Sorry..type another thing..!")
        onOffFunction()
