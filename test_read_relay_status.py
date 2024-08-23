from RPi import GPIO
from time import sleep

from pins import Pin

GPIO.setmode(GPIO.BCM)

GPIO.setup(Pin.RELAY_5V, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(Pin.RELAY_TF_PRIMARY, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(Pin.RELAY_TF_SECONDARY, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(Pin.STATUS_RELAY_5V, GPIO.IN)

try:
    while True:
        GPIO.output(Pin.RELAY_5V, GPIO.HIGH)
        sleep(2)

        val = GPIO.input(Pin.STATUS_RELAY_5V)
        print(val)
        
        sleep(2)

        GPIO.output(Pin.RELAY_5V, GPIO.LOW)
        sleep(3)
        
        val = GPIO.input(Pin.STATUS_RELAY_5V)
        print(val)
        
        sleep(2)

except KeyboardInterrupt:
    pass

GPIO.cleanup()