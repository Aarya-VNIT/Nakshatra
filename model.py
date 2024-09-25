from typing import *
from time import sleep

from RPi import GPIO

from pins import Pin
from motor import Motor
from nakshatra import Nakshatra
from arduino import Arduino

from utils import *
from log import Logger, DataLog

log = Logger.get_logger()

class Model:
    
    __SLEEP_TIME = 1800 # 30 * 60 seconds
    
    def __init__(self, motor: Motor, nks: Nakshatra, ard: Arduino):
        
        self.motor = motor
        self.nakshatra = nks
        self.arduino = ard        
    
        self.__initialize_board()
        
        self.fan_state = True
    
    def __initialize_board(self):
        
        log.info('Initializing Raspberry Pi Board ...')
        
        GPIO.setmode(GPIO.BCM)
        
        GPIO.setup(Pin.MOTOR_PUL, GPIO.OUT, initial = GPIO.LOW)        
        GPIO.setup(Pin.MOTOR_ENA, GPIO.OUT, initial = GPIO.LOW)        
        GPIO.setup(Pin.MOTOR_DIR, GPIO.OUT, initial = GPIO.LOW)   
         
        GPIO.setup(Pin.RELAY_TF_PRIMARY, GPIO.OUT, initial=GPIO.LOW)
        GPIO.setup(Pin.RELAY_TF_SECONDARY, GPIO.OUT, initial=GPIO.LOW)
        GPIO.setup(Pin.RELAY_5V, GPIO.OUT, initial=GPIO.LOW)
        GPIO.setup(Pin.RELAY_FAN, GPIO.OUT, initial=GPIO.LOW)
        
        GPIO.setup(Pin.STATUS_RELAY_5V, GPIO.IN)
        GPIO.setup(Pin.STATUS_RELAY_TF_PRIMARY, GPIO.IN)
    
    def __toggle_fan(self):
        '''
        Toggle the fan state from HIGH->LOW or LOW->HIGH eveytime this function is called.
        '''
        self.fan_state = not self.fan_state
        GPIO.output(Pin.RELAY_FAN, GPIO.HIGH if self.fan_state else GPIO.LOW)
    
    def __adjust_motor(self, target_angle: float):
        
        same_counter = 100
        
        # Calculate actual/current angle
        actual_angle = self.arduino.get_angle()
        initial_angle = actual_angle

        if actual_angle < 0:
            log.error("Unable to read Sensor Angle")
            
        else:
            
            log.info(f"Target Angle {target_angle:.4f} | Current Angle : {actual_angle:.4f}")
                        
            if not is_within_tolerance(actual_angle, target_angle):
                
                # Switch on primary transformer
                GPIO.output(Pin.RELAY_TF_PRIMARY, GPIO.HIGH)
                log.debug('Switching on : "Relay Transformer Primary"')
                sleep(2)
                
                # Read if the Primary Transformer is switched on
                relay_tf_primary = GPIO.input(Pin.STATUS_RELAY_TF_PRIMARY)
                val_msg = "SWITCHED ON" if relay_tf_primary == 1 else "SWITCHED OFF"
                log.debug(f"Relay TF Primary shows '{val_msg}'")
                
                if relay_tf_primary == 0:
                    log.error("Failed to switch on Transformer Power Supply")
                
                else:
                    # Switch on secondary transformer
                    GPIO.output(Pin.RELAY_TF_SECONDARY, GPIO.HIGH)
                    log.debug('Switching on : "Relay Transformer Secondary"')
                    sleep(2)
                
                prev_angle = actual_angle
                
                try:
                    # Move the motor to withing the tolerance region
                    while relay_tf_primary == 1 and not is_within_tolerance(actual_angle, target_angle):
                        
                        # Get the direction to move the needle
                        isReverse = get_direction(actual_angle, target_angle)
                        
                        # Move the motor
                        if isReverse:
                            self.motor.reverse()
                        else:
                            self.motor.forward()
                        
                        # Read the new current angle
                        actual_angle = self.arduino.get_angle()
                        
                        if actual_angle == -1:
                            log.warning("Error while reading angle in between the run")
                            break
                        
                        # Logic to stop the motor after some time, (in a scenario if motor is stuck in rotation)
                        if is_within_tolerance(actual_angle, prev_angle):
                            same_counter -= 1
                            
                        else:
                            same_counter = 100
                            
                        if same_counter == 0:
                            break
                        
                    if same_counter == 0:
                        log.warning("Motor NOT RUNNING!!")
                        
                    increment = (actual_angle - initial_angle)
                    error = (target_angle - actual_angle)

                    log.info(f"Target Angle {target_angle:.4f} | Current Angle : {actual_angle:.4f}")
                    log.info(f"Increment : {increment:.4f} | Error : {error:.4f}")
                
                    DataLog.debug(f'{increment:.3f},{error:.3f}')

            
                except KeyboardInterrupt:
                    log.warning("Keyboard Interrupt detected!!!")
                    log.warning("Ending current run.... Please wait!!!!")
                    
                except Exception:
                    log.warning("An error occurred while moving the motor")
                    log.warning("Ending current run!!!")        
                
                finally:
                    # Switch off Secondary Transformer
                    GPIO.output(Pin.RELAY_TF_SECONDARY, GPIO.LOW)
                    log.debug('Switching off : "Relay Transformer Secondary"')
                    sleep(1)
                    
                    # Switch off Primary Transformer
                    GPIO.output(Pin.RELAY_TF_PRIMARY, GPIO.LOW)
                    log.debug('Switching off : "Relay Transformer Primary"')
                    sleep(3)
                    
                    # Read if the Primary Transformer is switched off
                    val = GPIO.input(Pin.STATUS_RELAY_TF_PRIMARY)
                    val_msg = "SWITCHED ON" if val == 1 else "SWITCHED OFF"
                    log.debug(f"Relay TF Primary shows '{val_msg}'")

    
    def step(self, target_angle = None):
        '''
        Rotates motor to the desired angle.
        
        It switches on related power supply, and then it will measure the desired
        and actual angles. It then rotates the motor to the desired angle.
        '''
        
        is_tf_primary_on = False
        
        # Switch on 5V supply
        GPIO.output(Pin.RELAY_5V, GPIO.HIGH)
        log.debug('Switching on : "Relay 5V Power Supply"')
        sleep(2)
        
        # Read if the relay is switched on
        relay_5v_status = GPIO.input(Pin.STATUS_RELAY_5V)
        val_msg = "SWITCHED ON" if relay_5v_status == 1 else "SWITCHED OFF"
        log.debug(f"Relay 5V shows '{val_msg}'")
                    
        # Calculate target angle
        if target_angle == None:
            target_angle = self.nakshatra.get_angle_wrt_moon()

        if relay_5v_status == 0:
            log.error("Failed to switch on 5v power supply")

        else:
            self.__adjust_motor(target_angle)

            # Log the Current Nakshatra and Pada
            nakshatra_info = self.nakshatra.info(target_angle)
            log.info(f"Current Nakshatra : {nakshatra_info['name']}, Pada : {nakshatra_info['pada']:.1f}")
                        
        # Switch off 5v Supply
        GPIO.output(Pin.RELAY_5V, GPIO.LOW)
        log.debug('Switching off : "Relay 5V Power Supply"')
        sleep(3)
    
        # Read if the relay is switched on
        val = GPIO.input(Pin.STATUS_RELAY_5V)
        val_msg = "SWITCHED ON" if val == 1 else "SWITCHED OFF"
        log.debug(f"Relay 5V is '{val_msg}'")
        
        if is_tf_primary_on:

            log.debug("Waiting for Transformer Secondary Voltage Sensor to be discharged!!!")
            sleep(30)

            # Read if the Primary Transformer is switched off
            val = GPIO.input(Pin.STATUS_RELAY_TF_PRIMARY)
            val_msg = "SWITCHED ON" if val == 1 else "SWITCHED OFF"
            log.debug(f"Finally Relay TF Primary shows '{val_msg}'")

        
    def run(self, repeat_every = None):
        '''
        Corrects the needle to it's appropriate position. 
        It repeats this process for every `repeat_every` seconds later.
        
        Default: `repeat_every` = 30 mins (1800 seconds)
        '''
        
        if repeat_every == None:
            repeat_every = Model.__SLEEP_TIME
        
        while True:
            
            # If the date changes, this will return new logger
            log = Logger.get_logger()
            
            log.info(f'Starting Cycle {Logger.CYCLE_COUNT} ...')
            
            # Check and update the needle angle based on nakshatra
            self.step()

            # TODO: Write logic for calulcating angle of Tithi
            # Currently, we are just logging.

            angle, tithi = self.nakshatra.get_tithi_and_angle()
            log.info(f"Target Tithi Angle : {angle:4f} and Current Tithi : {tithi}")



            log.info('Completed Cycle!!!')
            log.info(f'Sleeping for {repeat_every} seconds')

            Logger.CYCLE_COUNT += 1
            
            # Toggle fan after every run
            self.__toggle_fan()
            
            # Upload the file to the cloud
            try:
                file_name = Logger.file_handler.baseFilename
                
                if Logger.uploader.upload_file(file_name):
                    Logger.log.debug(f"Log file {file_name} has been uploaded!")
                else:
                    Logger.log.debug(f"Log file {file_name} was not uploaded to the cloud!!")
            except Exception as e:
                Logger.log.error("Error occurred while uploading log file")

            log.info('--------------------------------------------------')

            # Sleep until next cycle
            sleep(repeat_every)