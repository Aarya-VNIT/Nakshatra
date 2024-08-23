from time import sleep
from RPi import GPIO

from pins import Pin

from typing import *

class Motor:
    '''
    Allows you to control motor motion.
    '''
    
    __PULSE_DELAY = 0.001
    __NO_OF_PULSES = 10
    
    def __init__(self, delay: int = 0.035) -> None:
        self.delay = delay
    
    def forward(self):
        '''
        Moves the motor one step in clockwise direction
        '''        
        
        # Set high to Enable PIN on motor
        GPIO.output(Pin.MOTOR_ENA, GPIO.HIGH)
        sleep(self.delay)
        
        # Set the direction to move clockwise (LOW)
        GPIO.output(Pin.MOTOR_DIR, GPIO.LOW)
        sleep(0.001)
        
        for _ in range(Motor.__NO_OF_PULSES):
            
            # +ve Half Cycle
            GPIO.output(Pin.MOTOR_PUL, GPIO.HIGH)
            sleep(Motor.__PULSE_DELAY)
            
            # -ve Half Cycle
            GPIO.output(Pin.MOTOR_PUL, GPIO.LOW)
            sleep(Motor.__PULSE_DELAY)
        
        # Once done, set the Enable PIN to LOW
        GPIO.output(Pin.MOTOR_ENA, GPIO.LOW)
        
        # Adding pause, due to possible direction change
        sleep(self.delay)
                
    def reverse(self):
        '''
        Moves the motor one step in anti-clockwise direction
        '''        
        
        # Set high to Enable PIN on motor
        GPIO.output(Pin.MOTOR_ENA, GPIO.HIGH)
        sleep(self.delay)
        
        # Set the direction to move anti-clockwise (HIGH)
        GPIO.output(Pin.MOTOR_DIR, GPIO.HIGH)
        sleep(0.001)
        
        for _ in range(Motor.__NO_OF_PULSES):
            
            # +ve Half Cycle
            GPIO.output(Pin.MOTOR_PUL, GPIO.HIGH)
            sleep(Motor.__PULSE_DELAY)
            
            # -ve Half Cycle
            GPIO.output(Pin.MOTOR_PUL, GPIO.LOW)
            sleep(Motor.__PULSE_DELAY)
        
        # Once done, set the Enable PIN to LOW
        GPIO.output(Pin.MOTOR_ENA, GPIO.LOW)
        
        # Adding pause, due to possible direction change
        sleep(self.delay)
    