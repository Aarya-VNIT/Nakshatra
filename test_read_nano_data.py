from arduino import Arduino
from RPi import GPIO
from time import sleep

from pins import Pin

nano = Arduino()

TOGGLE_SENSOR = False

try:
    GPIO.setmode(GPIO.BCM)
    
    GPIO.setup(Pin.RELAY_5V, GPIO.OUT, initial=GPIO.LOW)
    GPIO.setup(Pin.RELAY_SENSOR_SWITCH, GPIO.OUT, initial=GPIO.LOW)
    
    GPIO.output(Pin.RELAY_5V, GPIO.HIGH)
    sleep(2)
    
    for _ in range(20):
            
        GPIO.output(Pin.RELAY_SENSOR_SWITCH, GPIO.HIGH if TOGGLE_SENSOR else GPIO.LOW)
        sleep(20)
            
        angle = nano.get_angle()
        print(f"Current System : {'B' if TOGGLE_SENSOR else 'A'}")
        print(f"Current Angle : {angle}")

        TOGGLE_SENSOR = not TOGGLE_SENSOR

    GPIO.output(Pin.RELAY_5V, GPIO.LOW)
except KeyboardInterrupt:
    pass
finally:
    nano.ser.close()
    GPIO.cleanup()