import RPi.GPIO as GPIO
from gpiozero import Button
from subprocess import check_call
from signal import pause
import serial
from matplotlib import pyplot
import pyfirmata
from time import *
import numpy as np
import schedule
import sqlite3
from pyfirmata import *
from time import *
import scheduler


if __name__ =='__main__':

    # RASPBERRY
    GPIO.setmode ( GPIO.BOARD )  # 2 modi:  BCM or BOARD
    GPIO.setwarnings ( False )
    GPIO.setup ( port_or_pin , GPIO.IN )  # set a port/pin as an input
    GPIO.setup ( port_or_pin , GPIO.OUT )  # set a port/pin as an output
    GPIO.add_event_detect ( Button , GPIO.RISING , callback=main )
    
    # ARDUINO
    port = "COM3"
    board = Arduino(port)
    it = pyfirmata.util.Iterator(board)
    it.start()

    #### INIZIALIZZO DB ####
    globals(db_file)
    
    shutdown_btn = Button ( 17 , hold_time=2 )  # bottone shutdown pin 17
    shutdown_btn.when_held = shutdown
    pause ( )

    sec_salinity = freq_salinity / 1440  # 1440=min in 24h
    sec_temp = freq_tem / 1440
    sec_cibo = freq_cibo / 1440  # solenoid_valve
    sec_ph = freq_ph / 1440
    sec_od = freq_od / 1440
