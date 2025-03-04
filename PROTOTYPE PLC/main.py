
TAGS = {
    "%1.0" : "E STOP AT PENDENT",
    "%1.1" : "ESTOP AT POWERPACK"
}
def GENERAL():
    
    return True
def BLOCK_CALLING():
    # WIP
    if GENERAL():
        SEMI_AUTO()
    MOTOR_CONTROLS()
    OUTPUTS()
    MANUAL()
    AUTO()
    PRODUCTION()
    ALARM()
    HOMING()
    DATE_AND_TIME()
    PROCESS_PARAMETER_CONTROL()
    if MODBUS_RTU():
        PROD_ENERGY_CALCULATION()
    if SHIFT_SELECTION():
        DATE_AND_TIME()
    POSITION_LOG()
    
    return


def SERVO():
    return True

def HEATER_CONTROL():
    return


def main():
    # WIP
    BLOCK_CALLING()
    
    if SERVO():
        HEATER_CONTROL()
        
while True:
    main()
