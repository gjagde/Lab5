#!/usr/bin/python3

# This code runs continually in the background to apply
# the stored PWM slider value to the GPIO output

import RPi.GPIO as GPIO
import time
import json
from stepper import stepper


while True:
  try:
    with open("/home/pi/cgi/angle.txt", 'r') as file:
      data = json.load(file) # read duty cycle value from file
      angle = int(data['angle'])
    if(angle >= 0):
      stepper.goAngle(angle)
    else:
      stepper.zero()
    
  except KeyboardInterrupt:
    print('Keyboard Interrupt')
    GPIO.cleanup()
  except ValueError:
    print(ValueError)
    time.sleep(0.1)
