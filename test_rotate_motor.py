from RPi import GPIO
from time import sleep

from pins import Pin as PIN
from motor import Motor
from arduino import Arduino

GPIO.setmode(GPIO.BCM)

GPIO.setup(PIN.MOTOR_ENA, GPIO.OUT)
GPIO.setup(PIN.MOTOR_DIR, GPIO.OUT)
GPIO.setup(PIN.MOTOR_PUL, GPIO.OUT)

GPIO.setup(PIN.RELAY_5V, GPIO.OUT)
GPIO.setup(PIN.RELAY_TF_PRIMARY, GPIO.OUT)
GPIO.setup(PIN.RELAY_TF_SECONDARY, GPIO.OUT)

GPIO.setup(PIN.RELAY_SENSOR_SWITCH, GPIO.OUT, initial = GPIO.LOW)
GPIO.setup(PIN.RELAY_MOTOR_SWITCH, GPIO.OUT, initial = GPIO.LOW)

motor = Motor()
nano = Arduino()

TOGGLE_MOTOR = False

try:
    
    GPIO.output(PIN.RELAY_5V, GPIO.HIGH)
    sleep(3)
    
    # GPIO.output(PIN.RELAY_MOTOR_SWITCH, GPIO.HIGH)
    # sleep(1)
    # input()
    
    GPIO.output(PIN.RELAY_TF_PRIMARY, GPIO.HIGH)
    sleep(3)
    
    GPIO.output(PIN.RELAY_TF_SECONDARY, GPIO.HIGH)
    sleep(3)
    
    # for __ in range(10):

    prev_angle = -1
    while True:

        nano.clear_buffer()

        angle = nano.get_angle()
        print("Prev angle : ", prev_angle, 'Angle :', angle)

        prev_angle = angle

        angle = int(input("Input Angle: "))
        forward = input("Enter 'y' for forward : ")

        for pulse_count in range(angle):            
            print(pulse_count)
            if forward[0] == 'y':
                motor.forward()
            else:
                motor.reverse()
        


        # TOGGLE_MOTOR = not TOGGLE_MOTOR
        
        # GPIO.output(PIN.RELAY_MOTOR_SWITCH, GPIO.HIGH if TOGGLE_MOTOR else GPIO.LOW)
        # sleep(2)
        
    # angle = nano.get_angle()
    # print('After Angle :', angle)
    
    GPIO.output(PIN.RELAY_TF_SECONDARY, GPIO.LOW)
    sleep(3)

    GPIO.output(PIN.RELAY_TF_PRIMARY, GPIO.LOW)
    sleep(3)
    
    GPIO.output(PIN.RELAY_MOTOR_SWITCH, GPIO.LOW)
    sleep(1)
    
    GPIO.output(PIN.RELAY_5V, GPIO.LOW)
    sleep(1)

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