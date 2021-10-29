import RPi.GPIO as GPIO
import time

from PCF8591 import PCF8591


class Stepper:
  def __init__(self):
    self.pins = [18,21,22,23] # controller inputs: in1, in2, in3, in4
    for pin in self.pins:
      GPIO.setup(pin, GPIO.OUT, initial=0)
    self.sequence = [[1,0,0,0],[1,1,0,0],[0,1,0,0],[0,1,1,0],
             [0,0,1,0],[0,0,1,1],[0,0,0,1],[1,0,0,1] ]
    self.state = 0  # current position in stator sequence
    self.current = 0
    self.stepAngle = 4*512*2/360
    self.ADC = PCF8591(0x48)
    self.brightness = 1000
    
  # Define the pin sequence for counter-clockwise motion, noting that
  # two adjacent phases must be actuated together before stepping to
  # a new phase so that the rotor is pulled in the right direction:
  
  def delay_us(tus): # use microseconds to improve time resolution
    endTime = time.time() + float(tus)/ float(1E6)
    while time.time() < endTime:
      pass

  def halfstep(self,dir):
    # dir = +/- 1 (ccw / cw)
    self.state += dir
    if self.state > 7: self.state = 0
    elif self.state < 0: self.state =  7
    for pin in range(4):    # 4 pins that need to be energized
      GPIO.output(self.pins[pin], self.sequence[self.state][pin])
    self.delay_us(1000)

  def moveSteps(self,steps, dir):
    # move the actuation sequence a given number of half steps
    for step in steps:
      self.halfstep(dir)

  def goAngle(self, angle):
    #CCW first Case
    if (angle - self.current >0) and (angle-self.current <=180):
      steps = (angle-self.current)*self.angleStep
      self.moveSteps(steps,1)
    #CCW second Case
    elif angle-self.current <=-180:
      steps = (angle-self.current+360)*self.angleStep
      self.moveSteps(steps,1)
    #CW first case
    elif (angle-self.current<0) and (angle-self.current>-180):
      steps = (self.current-angle)*self.angleStep
      self.moveSteps(steps,-1)
    #CW second case
    elif (angle-self.current>180):
      steps = (360-(angle-self.current))*self.angleStep
      self.moveSteps(steps,-1)

  def Zero(self):
    while (self.brightness>500):
      self.brightness = int(self.ADC.read(0))
      self.halfstep(1)
    self.current = 0
  