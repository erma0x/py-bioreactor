from machine import Pin,Timer,PWM

pwm =PWM(Pin(2),100)
polar = 0
duty = 0

def setLed(t):
  global duty,polar
  if(polar == 0):
    duty+=16
    if(duty >= 1008):
      polar = 1
  else:
    duty -= 16
    if(duty <= 0):
      polar = 0
  pwm.duty(duty)

tim = Timer(1)
tim.init(period=10,mode=Timer.PERIODIC, callback=setLed)

try:
  while True:
    pass

except:
  tim.deinit()
  pwm.deinit()
