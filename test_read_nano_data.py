from arduino import Arduino
from RPi import GPIO
from time import sleep

from pins import Pin

nano = Arduino()

try:
    GPIO.setmode(GPIO.BCM)
    
    GPIO.setup(Pin.RELAY_5V, GPIO.OUT, initial=GPIO.LOW)
    
    GPIO.output(Pin.RELAY_5V, GPIO.HIGH)
    sleep(2)
    
    angle = nano.get_angle()
    print(f"Current Angle : {angle}")

    GPIO.output(Pin.RELAY_5V, GPIO.LOW)
except KeyboardInterrupt:
    pass
finally:
    nano.ser.close()
    GPIO.cleanup()