from RPi import GPIO
from time import sleep, time

from pins import Pin as PIN
from motor import Motor
from arduino import Arduino

GPIO.setmode(GPIO.BCM)

GPIO.setup(PIN.MOTOR_ENA, GPIO.OUT)
GPIO.setup(PIN.MOTOR_DIR, GPIO.OUT)
GPIO.setup(PIN.MOTOR_PUL, GPIO.OUT)

GPIO.setup(PIN.RELAY_FAN, GPIO.OUT)
GPIO.setup(PIN.RELAY_5V, GPIO.OUT)
GPIO.setup(PIN.RELAY_TF_PRIMARY, GPIO.OUT)
GPIO.setup(PIN.RELAY_TF_SECONDARY, GPIO.OUT)

GPIO.setup(PIN.RELAY_MOTOR_SWITCH, GPIO.OUT, initial = GPIO.LOW)
GPIO.setup(PIN.RELAY_SENSOR_SWITCH, GPIO.OUT, initial = GPIO.LOW)

motor = Motor()
nano = Arduino()

GPIO.output(PIN.RELAY_FAN, GPIO.HIGH)

SYSTEM_B = False

def switch_systems():
    
    global SYSTEM_B
    
    SYSTEM_B = not SYSTEM_B
    # GPIO.output(PIN.RELAY_MOTOR_SWITCH, GPIO.HIGH if SYSTEM_B else GPIO.LOW)
    GPIO.output(PIN.RELAY_SENSOR_SWITCH, GPIO.HIGH if SYSTEM_B else GPIO.LOW)

try:
    
    for __ in range(3):
    
        GPIO.output(PIN.RELAY_5V, GPIO.HIGH)
        sleep(1)    
        GPIO.output(PIN.RELAY_TF_PRIMARY, GPIO.HIGH)    
        sleep(1)    
        GPIO.output(PIN.RELAY_TF_SECONDARY, GPIO.HIGH)    
        sleep(1)    
        
        nano.clear_buffer(5)

        for _ in range(10):
            
            # nano.clear_buffer()
            
            angle = nano.get_angle()
            print(f"System A : {angle}")
            sleep(1)
        
        GPIO.output(PIN.RELAY_TF_SECONDARY, GPIO.LOW)    
        sleep(1)    

        GPIO.output(PIN.RELAY_5V, GPIO.LOW)    
        sleep(3)
        
            
        GPIO.output(PIN.RELAY_5V, GPIO.HIGH)
        sleep(1)    

        switch_systems()
        sleep(2)
        
        nano.clear_buffer(5)
        
        GPIO.output(PIN.RELAY_TF_SECONDARY, GPIO.HIGH)    
        sleep(1)    

        for _ in range(10):
            
            # nano.clear_buffer()
            
            angle = nano.get_angle()
            print(f"System B : {angle}")
            sleep(1)
            
        for _ in range(20):
            motor.forward()
        
        GPIO.output(PIN.RELAY_TF_SECONDARY, GPIO.LOW)    
        sleep(1)    
        
        switch_systems()
        sleep(1)
        
        GPIO.output(PIN.RELAY_TF_PRIMARY, GPIO.LOW)    
        sleep(1)    
        GPIO.output(PIN.RELAY_5V, GPIO.LOW)    
        sleep(1)    
        
    
    
    
    # for i in range(10):
        
    #     GPIO.output(PIN.RELAY_5V, GPIO.HIGH)    
    #     sleep(1)    
        
    #     switch_systems()
        
    #     GPIO.output(PIN.RELAY_TF_PRIMARY, GPIO.HIGH)    
    #     sleep(1)    
    #     GPIO.output(PIN.RELAY_TF_SECONDARY, GPIO.HIGH)    
    #     sleep(1)
        
    #     print(f"System : {'B' if SYSTEM_B else 'A'}")
        
    #     nano.clear_buffer()
    #     sleep(0.2)
    #     angle = nano.get_angle()
        
    #     print(f"Before Angle : {angle}")
    #     sleep(2)
        
    #     for __ in range(100):
    #         if (i % 2) == 0:
    #             motor.forward()
    #         else:
    #             motor.reverse()
        
    #     nano.clear_buffer()
    #     sleep(0.2)
    #     angle = nano.get_angle()
        
    #     print(nano.ser.in_waiting)
    #     nano.clear_buffer()
    #     print(nano.ser.in_waiting)
        
    #     print(f"After Angle : {angle}")
            
    #     print(f"-------------------------")
            
    #     GPIO.output(PIN.RELAY_TF_SECONDARY, GPIO.LOW)
    #     sleep(1)    
    #     GPIO.output(PIN.RELAY_TF_PRIMARY, GPIO.LOW)    
    #     sleep(1)    
    #     GPIO.output(PIN.RELAY_5V, GPIO.LOW)    
    #     sleep(1)
        
    #     sleep(5)    
    
    #     GPIO.output(PIN.RELAY_5V, GPIO.HIGH)    
    #     sleep(1)    
        
    #     switch_systems()
        
    #     GPIO.output(PIN.RELAY_TF_PRIMARY, GPIO.HIGH)    
    #     sleep(1)    
    #     GPIO.output(PIN.RELAY_TF_SECONDARY, GPIO.HIGH)    
    #     sleep(1)
        
    #     print(f"System : {'B' if SYSTEM_B else 'A'}")
        
    #     nano.clear_buffer()
    #     sleep(0.2)
    #     angle = nano.get_angle()
        
    #     print(f"Before Angle : {angle}")
    #     sleep(2)
        
    #     for __ in range(100):
    #         if (i % 2) == 0:
    #             motor.forward()
    #         else:
    #             motor.reverse()
        
    #     nano.clear_buffer()
    #     sleep(0.2)
    #     angle = nano.get_angle()
    #     print(f"After Angle : {angle}")
            
    #     print(f"-------------------------")
            
    #     GPIO.output(PIN.RELAY_TF_SECONDARY, GPIO.LOW)
    #     sleep(1)    
    #     GPIO.output(PIN.RELAY_TF_PRIMARY, GPIO.LOW)    
    #     sleep(1)    
    #     GPIO.output(PIN.RELAY_5V, GPIO.LOW)    
    #     sleep(5)    
    
except KeyboardInterrupt:
    pass

finally:
    
    
    GPIO.output(PIN.RELAY_FAN, GPIO.LOW)
    
    GPIO.output(PIN.RELAY_TF_SECONDARY, GPIO.LOW)
    sleep(2)    
    GPIO.output(PIN.RELAY_TF_PRIMARY, GPIO.LOW)    
    sleep(2)    
    GPIO.output(PIN.RELAY_5V, GPIO.LOW)    
    sleep(2)    
    
    GPIO.cleanup()