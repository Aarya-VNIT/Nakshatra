from RPi import GPIO
from time import sleep

from pins import Pin as PIN
from motor import Motor

GPIO.setmode(GPIO.BCM)

GPIO.setup(PIN.MOTOR_ENA, GPIO.OUT)
GPIO.setup(PIN.MOTOR_DIR, GPIO.OUT)
GPIO.setup(PIN.MOTOR_PUL, GPIO.OUT)

GPIO.setup(PIN.RELAY_5V, GPIO.OUT)
GPIO.setup(PIN.RELAY_TF_PRIMARY, GPIO.OUT)
GPIO.setup(PIN.RELAY_TF_SECONDARY, GPIO.OUT)

motor = Motor()

try:
    
    GPIO.output(PIN.RELAY_5V, GPIO.HIGH)
    sleep(3)
    
    GPIO.output(PIN.RELAY_TF_PRIMARY, GPIO.HIGH)
    sleep(3)
    
    GPIO.output(PIN.RELAY_TF_SECONDARY, GPIO.HIGH)
    sleep(3)
    
    for _ in range(100):
        # motor.forward()
        motor.reverse()
    
    GPIO.output(PIN.RELAY_TF_SECONDARY, GPIO.LOW)
    sleep(3)

    GPIO.output(PIN.RELAY_TF_PRIMARY, GPIO.LOW)
    sleep(3)
    
    GPIO.output(PIN.RELAY_5V, GPIO.LOW)
    sleep(3)

except KeyboardInterrupt:
    
    print("Quitting...")

finally:
    
    GPIO.output(PIN.RELAY_TF_SECONDARY, GPIO.LOW)
    sleep(3)

    GPIO.output(PIN.RELAY_TF_PRIMARY, GPIO.LOW)
    sleep(3)
    
    GPIO.output(PIN.RELAY_5V, GPIO.LOW)
    sleep(3)
    
    GPIO.cleanup()