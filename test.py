# Based on: https://www.raspberrypi.org/forums/viewtopic.php?t=242928\.
#
# Software to drive 4 wire stepper motor using a TB6600 Driver
# PRi - RPi 3B
#
# Route 3.3 VDC to the controller "+" input for each: ENA, PUL, and DIR
#
# Connect GPIO pins as shown below) to the "-" input for each: ENA, PUL, and DIR
#
#
from time import sleep
import RPi.GPIO as GPIO
# from AS5600 import AS5600
# from nakshatra_degree import getDegree
# import requests

#
PUL = 27  # Stepper Drive Pulses
DIR = 17  # Controller Direction Bit (High for Controller default / LOW to Force a Direction Change).
ENA = 22  # Controller Enable Bit (High to Enable / LOW to Disable).

RLY1 = 26

# DIRI = 14  # Status Indicator LED - Direction
# ENAI = 15  # Status indicator LED - Controller Enable
#
# NOTE: Leave DIR and ENA disconnected, and the controller WILL drive the motor in Default direction if PUL is applied.
# 
GPIO.setmode(GPIO.BCM)
# GPIO.setmode(GPIO.BOARD) # Do NOT use GPIO.BOARD mode. Here for comparison only. 
#
GPIO.setup(PUL, GPIO.OUT)
GPIO.setup(DIR, GPIO.OUT)
GPIO.setup(ENA, GPIO.OUT)
GPIO.setup(RLY1, GPIO.OUT)
# GPIO.setup(DIRI, GPIO.OUT)
# GPIO.setup(ENAI, GPIO.OUT)
#
print('PUL = GPIO 17 - RPi 3B-Pin #11')
print('DIR = GPIO 27 - RPi 3B-Pin #13')
print('ENA = GPIO 22 - RPi 3B-Pin #15')
# print('ENAI = GPIO 14 - RPi 3B-Pin #8')
# print('DIRI = GPIO 15 - RPi 3B-Pin #10')

#
print('Initialization Completed')
#
# Could have usesd only one DURATION constant but chose two. This gives play options.
durationFwd = 10 # This is the duration of the motor spinning. used for forward direction
durationBwd = 10 # This is the duration of the motor spinning. used for reverse direction
print('Duration Fwd set to ' + str(durationFwd))
print('Duration Bwd set to ' + str(durationBwd))
#
delay = 0.00001 # This is actualy a delay between PUL pulses - effectively sets the mtor rotation speed.
print('Speed set to ' + str(delay))
#
cycles = 1000 # This is the number of cycles to be run once program is started.
cyclecount = 0 # This is the iteration of cycles to be run once program is started.
print('number of Cycles to Run set to ' + str(cycles))
#
#
def forward(delay2):
    GPIO.output(ENA, GPIO.HIGH)
    # GPIO.output(ENAI, GPIO.HIGH)
    # print('ENA set to HIGH - Controller Enabled')
    #
    sleep(delay2) # pause due to a possible change direction
    GPIO.output(DIR, GPIO.LOW)
    # GPIO.output(DIRI, GPIO.LOW)
    # print('DIR set to LOW - Moving Forward at ' + str(delay))
    # print('Controller PUL being driven.')
    for x in range(durationFwd): 
        GPIO.output(PUL, GPIO.HIGH)
        sleep(delay)
        GPIO.output(PUL, GPIO.LOW)
        sleep(delay)
    GPIO.output(ENA, GPIO.LOW)
    # GPIO.output(ENAI, GPIO.LOW)
    # print('ENA set to LOW - Controller Disabled')
    sleep(delay2) # pause for possible change direction
    return
#
#
def reverse(delay2):
    GPIO.output(ENA, GPIO.HIGH)
    # GPIO.output(ENAI, GPIO.HIGH)
    # print('ENA set to HIGH - Controller Enabled')
    #
    sleep(delay2) # pause due to a possible change direction
    GPIO.output(DIR, GPIO.HIGH)
    # GPIO.output(DIRI, GPIO.HIGH)
    # print('DIR set to HIGH - Moving Backward at ' + str(delay))
    # print('Controller PUL being driven.')
    #
    for y in range(durationBwd):
        GPIO.output(PUL, GPIO.HIGH)
        sleep(delay)
        GPIO.output(PUL, GPIO.LOW)
        sleep(delay)
        
    # GPIO.output(DIR, GPIO.LOW)
    GPIO.output(ENA, GPIO.LOW)
    # GPIO.output(ENAI, GPIO.LOW)
    # print('ENA set to LOW - Controller Disabled')
    sleep(delay2) # pause for possible change direction
    return

# import logging

# logger = logging.getLogger(__name__)

# logging.basicConfig(filename='tmp.log', filemode='a', format='%(asctime)s - %(levelname)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S', encoding='utf-8', level=logging.DEBUG)
# # logging.warning('This will get logged to a file')
# import keyboard
# import sys

# bus = 1  # I2C bus number
# AS5600_id = 0x36  # Device ID

# sensor = AS5600(bus, AS5600_id)
# # The API endpoint
# url = "https://rus00.pythonanywhere.com/upload"

def withinnn_tolerance(curr_angle, target, tolerance=0.05):
    diff = abs((target - curr_angle + 180) % 360 - 180)
    return diff <= tolerance

def getDirection(curr_angle, target):
    diff = (target - curr_angle + 360) % 360
    if(diff > 180):
        return 0 # reverse
    else:
        return 1 # forward
try:
    while True:
        # curr_angle = sensor.get_angle_degrees()
        # target = getDegree()
        target = 90
        print('Target Angle: ' + "{:.2f}".format(target))
        # logger.info("Target: %s", str(target))
        # print('Current Angle: ' + "{:.2f}".format(curr_angle))
        # logger.info("Current Angle: %s", str(curr_angle))

        forDir = True
        
        GPIO.output(RLY1, GPIO.HIGH)
        sleep(2)

        # while (not withinnn_tolerance(curr_angle, target)):
        while cyclecount <= 100:
            delay2 = 0.05
            
            # delay = 0.1
            # if(withinnn_tolerance(curr_angle, target, 1)):
            #     delay = 0.05
            
            # direction = getDirection(curr_angle, target)
            # if( direction == 0):
            #     reverse(delay)
            #     cyclecount = (cyclecount - 1)
            # else:
            #     forward(delay)
            #     cyclecount = (cyclecount + 1)
            # if forDir:
            #     forward(delay2)
            # else:
            #     reverse(delay2)

            # if (cyclecount % 50) == 0:
            #     forDir = not forDir
            
            # forward(delay2)
            reverse(delay2)
            cyclecount = (cyclecount + 1)

            # curr_angle = sensor.get_angle_degrees()
            print('Number of cycles completed: ' + str(cyclecount))
            # logger.info("Number of cycles completed: %s", str(cyclecount))
            # print('Current Angle: ' + "{:.2f}".format(curr_angle))
            # logger.info("Current Angle: %s", str(curr_angle))

        # PARAMS = {"degree":"{:.2f}".format(curr_angle), "target":"{:.2f}".format(target)}
        # try:
        #     requests.get(url, params=PARAMS)
        # except:
        #     print("Network not available")
        #     # logger.warning('Network not available for feedback upload')
            
        GPIO.output(RLY1, GPIO.LOW)
        print('Phase Completed')
        # logger.info("Phase Completed")
        sleep(1800)
except KeyboardInterrupt:
    pass
#
finally:
    GPIO.cleanup()
#
