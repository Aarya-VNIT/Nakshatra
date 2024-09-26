import serial
from RPi import GPIO

from log import Logger

log = Logger.get_logger()

class Arduino:
    
    __MAX_BIT = (1 << 13) - 1
    __NO_OF_READINGS = 300

    def __init__(self) -> None:
        # Configure the serial port (UART)
        self.ser = serial.Serial('/dev/serial0', 9600, timeout=1)

    def __convert_to_angle(self, data: int, precision: int = 4):
        '''
        Reads the 'data' from the sensor and converts it into angle,
        with a given 'precision'.
        '''
        return round((data / Arduino.__MAX_BIT) * 360, precision)

    def clear_buffer(self):
        self.ser.reset_input_buffer()

    def get_angle(self):
        # Frequency Data
        # Stores the frequency of the angles
        freq_data = {}
        
        self.ser.reset_input_buffer()
        
        for _ in range(Arduino.__NO_OF_READINGS):
            
            if self.ser.in_waiting > 0:
                try:
                    line = self.ser.readline().rstrip()
                    if len(line) > 0:
                        line = line.decode('utf-8', errors='ignore')
                        # print(line)
                        angle = self.__convert_to_angle(int(line))
                        freq_data[angle] = (freq_data[angle] if angle in freq_data else 0) + 1
                except ValueError:
                    # If some unknown garbage value is being read,
                    # just skip and take the next readings
                    pass

        # Sort them based on frequency
        freq_data_items = sorted(freq_data.items(), key = lambda k: k[1], reverse=True)
        
        if len(freq_data_items) == 0:
            return -1
        
        if len(freq_data_items) == 1 and (freq_data_items[0][0] == 0.0 or freq_data_items[0][0] == 360.0):
            log.warning("Possible no supply for the sensor")
            return -1
        
        if len(freq_data_items) > 10:
            log.warning("Possible garbage values when reading sensor angle")
            print(len(freq_data_items))
            print(freq_data_items)
            return -1
        
        # Return the angle with highest frequency
        return freq_data_items[0][0]

    def __del__(self):
        self.ser.close()