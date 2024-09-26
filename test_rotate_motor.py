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

GPIO.setup(PIN.RELAY_MOTOR_SWITCH, GPIO.OUT)

motor = Motor()

TOGGLE_MOTOR = False

try:
    
    GPIO.output(PIN.RELAY_5V, GPIO.HIGH)
    sleep(3)
    
    GPIO.output(PIN.RELAY_TF_PRIMARY, GPIO.HIGH)
    sleep(3)
    
    GPIO.output(PIN.RELAY_TF_SECONDARY, GPIO.HIGH)
    sleep(3)
    
    for __ in range(10):
        
        for _ in range(100):            
            # motor.forward()
            motor.reverse()
        
        TOGGLE_MOTOR = not TOGGLE_MOTOR
        
        GPIO.output(PIN.RELAY_MOTOR_SWITCH, GPIO.HIGH if TOGGLE_MOTOR else GPIO.LOW)
        sleep(2)
        
    
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