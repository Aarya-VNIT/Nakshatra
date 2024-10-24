from RPi import GPIO
from time import sleep

from pins import Pin

GPIO.setmode(GPIO.BCM)

GPIO.setup(Pin.RELAY_SENSOR_SWITCH, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(Pin.RELAY_MOTOR_SWITCH, GPIO.OUT, initial=GPIO.LOW)

GPIO.setup(Pin.RELAY_5V, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(Pin.RELAY_TF_PRIMARY, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(Pin.RELAY_TF_SECONDARY, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(Pin.RELAY_FAN, GPIO.OUT, initial=GPIO.LOW)

try:
    while True:

        print("Relay 5V ON")
        # input()
        GPIO.output(Pin.RELAY_5V, GPIO.HIGH)
        sleep(2)

        print("Relay Sensor Switch ON")
        GPIO.output(Pin.RELAY_SENSOR_SWITCH, GPIO.HIGH)
        sleep(2)

        print("Relay Motor Switch ON")
        GPIO.output(Pin.RELAY_MOTOR_SWITCH, GPIO.HIGH)
        sleep(2)

        print("Relay TF P ON")
        # input()
        GPIO.output(Pin.RELAY_TF_PRIMARY, GPIO.HIGH)
        sleep(1)

        print("Relay TF S ON")
        # input()
        GPIO.output(Pin.RELAY_TF_SECONDARY, GPIO.HIGH)
        sleep(5)

        print("Relay FAN ON")
        # input()
        GPIO.output(Pin.RELAY_FAN, GPIO.HIGH)
        sleep(5)

        print("Relay FAN OFF")
        GPIO.output(Pin.RELAY_FAN, GPIO.LOW)
        sleep(0.5)

        print("Relay TF S OFF")
        GPIO.output(Pin.RELAY_TF_SECONDARY, GPIO.LOW)
        sleep(0.5)

        print("Relay TF P OFF")
        GPIO.output(Pin.RELAY_TF_PRIMARY, GPIO.LOW)
        sleep(0.5)

        print("Relay Motor Switch OFF")
        GPIO.output(Pin.RELAY_SENSOR_SWITCH, GPIO.LOW)
        sleep(2)

        print("Relay Sensor Switch OFF")
        GPIO.output(Pin.RELAY_MOTOR_SWITCH, GPIO.LOW)
        sleep(2)

        print("Relay 5V OFF")
        GPIO.output(Pin.RELAY_5V, GPIO.LOW)
        sleep(2)
        
except KeyboardInterrupt:
    pass

finally:
    GPIO.cleanup()