class Pin:
    '''
    Pin mappings for the given Raspberry Pi board
    '''
    
    # Motor PINS
    MOTOR_DIR: int = 17
    MOTOR_PUL: int = 27
    MOTOR_ENA: int = 22
    
    # Relay PINS
    RELAY_5V: int = 5
    RELAY_TF_PRIMARY: int = 6
    RELAY_TF_SECONDARY: int = 26
    RELAY_FAN: int = 16
    
    STATUS_RELAY_5V: int = 23
    STATUS_RELAY_TF_PRIMARY: int = 24
    
    RELAY_SENSOR_SWITCH: int = 20
    RELAY_MOTOR_SWITCH: int = 21
    
    # RX Pin for Arduino reading
    RX: int = 15 # Not needed, or use
    
    def get_mappings():
        return list(filter(lambda i: not (i[0].startswith('__')) and not (i[0] == 'get_mappings')  ,Pin.__dict__.items()))