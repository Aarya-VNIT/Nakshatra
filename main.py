import os
from time import sleep
import signal

from RPi import GPIO

from nakshatra import Nakshatra
from arduino import Arduino
from motor import Motor
from pins import Pin
from log import Logger

from model import Model

log = Logger.get_logger()

if __name__ == "__main__":
    
    log.info('Starting Application...')
    
    log.info('Initializing all the dependecies')
    
    nks = Nakshatra()
    nano = Arduino()
    motor = Motor()
    
    log.debug(f'Current Pin Mappings : ')
    for k, v in Pin.get_mappings():
        log.debug(f'{k} -> {v}')
    
    model = Model(motor, nks, nano)  

    try:
        print("Current Angle : ", nano.get_angle())
        model.step(float(input("Enter target angle : ")))
        # model.run()
    except KeyboardInterrupt:
        log.warning('Detected Keyboard Interrupt')
        log.warning('Quitting Application!!!')
    except Exception as e:
        log.exception("Unknown Exception Occurred!!!")
        log.exception(e)
    finally:
        log.info('Cleaning up GPIO')
        GPIO.cleanup()