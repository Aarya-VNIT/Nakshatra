from typing import *
from time import sleep, time

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
        
        self.system_state_sensor = False
        self.system_state_motor = False
    
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
        
        GPIO.setup(Pin.RELAY_SENSOR_SWITCH, GPIO.OUT, initial = GPIO.LOW)
        GPIO.setup(Pin.RELAY_MOTOR_SWITCH, GPIO.OUT, initial = GPIO.LOW)
        
        GPIO.setup(Pin.STATUS_RELAY_5V, GPIO.IN)
        GPIO.setup(Pin.STATUS_RELAY_TF_PRIMARY, GPIO.IN)
    
    def __toggle_fan(self):
        '''
        Toggle the fan state from HIGH->LOW or LOW->HIGH eveytime this function is called.
        '''
        self.fan_state = not self.fan_state
        GPIO.output(Pin.RELAY_FAN, GPIO.HIGH if self.fan_state else GPIO.LOW)
    
    def step(self, target_angle = None):
        '''
        Rotates motor to the desired angle.
        
        It switches on related power supply, and then it will measure the desired
        and actual angles. It then rotates the motor to the desired angle.
        '''
        
        same_counter = 100

        is_tf_primary_on = False
        
        # Switch on 5V supply
        GPIO.output(Pin.RELAY_5V, GPIO.HIGH)
        log.debug('Switching on : "Relay 5V Power Supply"')
        sleep(2)
        
        # Read if the relay is switched on
        relay_5v_status = GPIO.input(Pin.STATUS_RELAY_5V)
        val_msg = "SWITCHED ON" if relay_5v_status == 1 else "SWITCHED OFF"
        log.debug(f"Relay 5V shows '{val_msg}'")
    
        GPIO.output(Pin.RELAY_SENSOR_SWITCH, GPIO.HIGH)
        sleep(2)
        
        # Calculate actual/current angle
        actual_angle = self.arduino.get_angle()
        initial_angle = actual_angle
            
        # Calculate target angle
        if target_angle == None:
            target_angle = self.nakshatra.get_angle_wrt_moon()

        if relay_5v_status == 0:
            log.error("Failed to switch on 5v power supply")

        elif actual_angle < 0:
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
                
                is_tf_primary_on = True
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
                        
                        # print(f"Actual Angle : {actual_angle} - Target Angle : {target_angle} - Previous Angle : {prev_angle} - Same counter : {same_counter}")
                        
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

                    # Log the Current Nakshatra and Pada
                    nakshatra_info = self.nakshatra.info(actual_angle)
                    log.info(f"Current Nakshatra : {nakshatra_info['name']}, Pada : {nakshatra_info['pada']:.1f}")
            
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

    def __toggle_system(self):
        '''
            Toggles System from Nakshatra to Tithi
            
            system_state = False -> Nakshatra
            system_state = True -> Tithi
        '''
        
        self.system_state_sensor = not self.system_state_sensor
        self.system_state_motor = not self.system_state_motor
        
        GPIO.output(Pin.RELAY_SENSOR_SWITCH, GPIO.HIGH if self.system_state_sensor else GPIO.LOW)
        GPIO.output(Pin.RELAY_MOTOR_SWITCH, GPIO.HIGH if self.system_state_motor else GPIO.LOW)

    def step2(self):
                
        # Switch on 5V supply
        GPIO.output(Pin.RELAY_5V, GPIO.HIGH)
        log.debug('Switching on : "Relay 5V Power Supply"')
        sleep(2)
        
        # Read if the relay is switched on
        relay_5v_status = GPIO.input(Pin.STATUS_RELAY_5V)
        val_msg = "SWITCHED ON" if relay_5v_status == 1 else "SWITCHED OFF"
        log.debug(f"Relay 5V shows '{val_msg}'")
        
        if relay_5v_status == 0:
            log.error("Failed to switch on 5v power supply")
            raise Exception("Failed to switch on 5v power supply")
        
        self.arduino.clear_buffer(5)
        
        # ----------------- Nakshatra Step -----------------------
        
        nakshatra_target_angle = self.nakshatra.get_angle_wrt_moon()
        self.__rotate_motor(nakshatra_target_angle)
        # sleep(3)
        
        current_sensor_angle = self.arduino.get_angle()
        nakshatra_info = self.nakshatra.info(current_sensor_angle)
        
        log.info(f"Nakshatra Angle : {current_sensor_angle:.4f} | Current Nakshatra : {nakshatra_info['name']} | Current Pada : {nakshatra_info['pada']:.1f}")
        log.info('Nakshatra Cycle Complete!!!')
        
        # ----------------- Switch Systems -----------------------
        

        self.arduino.clear_buffer(5)
        
        # ----------------- Tithi Step ---------------------------
        tithi_target_angle, tithi = self.nakshatra.get_tithi_and_angle()
        self.__rotate_motor(tithi_target_angle)
        # sleep(3)
        
        current_sensor_angle = self.arduino.get_angle()
        
        log.info(f'Tithi Angle : {current_sensor_angle:.4f} | Current Tithi : {tithi}')
        log.info('Tithi Cycle Complete!!!')
        
        self.__toggle_system()
        
        # Switch off 5v Supply
        GPIO.output(Pin.RELAY_5V, GPIO.LOW)
        log.debug('Switching off : "Relay 5V Power Supply"')
        sleep(3)
    
        # Read if the relay is switched on
        val = GPIO.input(Pin.STATUS_RELAY_5V)
        val_msg = "SWITCHED ON" if val == 1 else "SWITCHED OFF"
        log.debug(f"Relay 5V is '{val_msg}'")
        
        is_tf_primary_on = GPIO.input(Pin.STATUS_RELAY_TF_PRIMARY)
        
        if is_tf_primary_on == 1:

            log.debug("Waiting for Transformer Secondary Voltage Sensor to be discharged!!!")
            sleep(30)

            # Read if the Primary Transformer is switched off
            val = GPIO.input(Pin.STATUS_RELAY_TF_PRIMARY)
            val_msg = "SWITCHED ON" if val == 1 else "SWITCHED OFF"
            log.debug(f"Finally Relay TF Primary shows '{val_msg}'")

    def __rotate_motor(self, target_angle: float, timeout: int = 10):
                
        same_counter = 250

        # Calculate actual/current angle
        actual_angle = self.arduino.get_angle()
        initial_angle = actual_angle
                
        log.info(f"Target Angle {target_angle:.4f} | Current Angle : {actual_angle:.4f}")
                    
        if not is_within_tolerance(actual_angle, target_angle):
                        
            prev_angle = actual_angle
            start_time = time()

            try:
                # Move the motor to withing the tolerance region
                while not is_within_tolerance(actual_angle, target_angle):
                    
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
                    if is_within_tolerance(actual_angle, prev_angle, 1):
                        same_counter -= 1
                        # print('Same Counter', same_counter)
                        
                    else:
                        same_counter = 250
                        prev_angle = actual_angle
                        # print('Same Counter', same_counter)
                        # print('Outside Tolerance!! Modified initial angle to ', prev_angle)
                        
                    # print(f'Start Time : {start_time} ~ Current Time : {time()}')
                    # print(f'Current Angle : {actual_angle}')

                    if (time() - start_time) > timeout and same_counter <= 0:
                        log.warning(f"Warning: Motor is moving continuously for more than {timeout} seconds!!")
                        log.warning(f"Stopping Motor!!! Contact Technical Assisstance!!!")
                        break

                    if same_counter <= 0:
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
            
    def step3(self):
        
        # Switch on 5V supply
        GPIO.output(Pin.RELAY_TF_PRIMARY, GPIO.HIGH)
        sleep(2)
        

        # Nakshatra Cycle

        GPIO.output(Pin.RELAY_5V, GPIO.HIGH)
        sleep(2)

        self.arduino.clear_buffer(5)
        sleep(2)

        actual_angle = self.arduino.get_angle()
        initial_angle = actual_angle
        
        nakshatra_target_angle = self.nakshatra.get_angle_wrt_moon()

        log.info(f"Nakshatra Angle : {nakshatra_target_angle} --- Current Angle : {actual_angle}")

        if not is_within_tolerance(actual_angle, nakshatra_target_angle):
            
            GPIO.output(Pin.RELAY_TF_SECONDARY, GPIO.HIGH)
            sleep(2)
            
            self.__rotate_motor(nakshatra_target_angle)

            GPIO.output(Pin.RELAY_TF_SECONDARY, GPIO.LOW)
            sleep(2)

        GPIO.output(Pin.RELAY_5V, GPIO.LOW)
        sleep(2)


        # Tithi Cycle
        GPIO.output(Pin.RELAY_5V, GPIO.HIGH)
        sleep(2)

        GPIO.output(Pin.RELAY_SENSOR_SWITCH, GPIO.HIGH)
        sleep(1)

        self.arduino.clear_buffer(5)

        actual_angle = self.arduino.get_angle()
        initial_angle = actual_angle
        
        tithi_angle, tithi = self.nakshatra.get_tithi_and_angle()

        log.info(f"Tithi Angle : {tithi_angle} --- Current Angle : {actual_angle}")

        if not is_within_tolerance(actual_angle, tithi_angle):
            
            GPIO.output(Pin.RELAY_MOTOR_SWITCH, GPIO.HIGH)
            sleep(1)

            GPIO.output(Pin.RELAY_TF_SECONDARY, GPIO.HIGH)
            sleep(2)

            for _ in range(20):
                self.motor.forward()
            
            # self.__rotate_motor(tithi_angle)

            GPIO.output(Pin.RELAY_TF_SECONDARY, GPIO.LOW)
            sleep(2)

            GPIO.output(Pin.RELAY_MOTOR_SWITCH, GPIO.LOW)
            sleep(1)

        GPIO.output(Pin.RELAY_SENSOR_SWITCH, GPIO.LOW)
        sleep(1)
    

        GPIO.output(Pin.RELAY_5V, GPIO.LOW)
        sleep(2)
        

        GPIO.output(Pin.RELAY_TF_PRIMARY, GPIO.LOW)
        sleep(2)
    
        is_tf_primary_on = GPIO.input(Pin.STATUS_RELAY_TF_PRIMARY)
        
        if is_tf_primary_on == 1:

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
            try:
                # self.step()
                self.step3()
                
            except Exception as e:
                log.error("Error Occurred in this cycle")

            # # TODO: Write logic for calulcating angle of Tithi
            # # Currently, we are just logging.

            # angle, tithi = self.nakshatra.get_tithi_and_angle()
            # log.info(f"Target Tithi Angle : {angle:4f} and Current Tithi : {tithi}")

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
            