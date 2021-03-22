#!/usr/bin/python
# Import required libraries
#import imp
#foo = imp.load_source('pyserial','\users\ermano\appdata\local\programs\python\python36-32\lib\site-packages\pyfirmata.py')
#foo.MyClass()
import pyfirmata
from time import sleep
board=Arduino('COM3')
iterator=util.iterator(board)
iterator.start()
val=board.get_pin('a:0:i')
print (val.read())
sleep(1.0)

