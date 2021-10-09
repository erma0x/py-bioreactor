# ____ RASPBERRY ________
GPIO.setmode ( GPIO.BOARD )  # 2 modi:  BCM or BOARD
GPIO.setwarnings ( False )
GPIO.setup ( port_or_pin , GPIO.IN )  # set a port/pin as an input
GPIO.setup ( port_or_pin , GPIO.OUT )  # set a port/pin as an output
GPIO.add_event_detect ( Button , GPIO.RISING , callback=main )
# ___________ ARDUINO _________
port = "COM3"
board = Arduino ( port )
it = pyfirmata.util.Iterator ( board )
it.start ( )