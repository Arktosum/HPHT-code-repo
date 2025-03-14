import time
import pyvisa

class NanoVoltmeter:
    def __init__(self, rm, GPIB):
        self.rm = rm

        # Connect Device
        self.device = self.rm.open_resource(GPIB)
        # Reset Device
        self.device.write('*RST')
        # Set Nanovoltmeter to sense voltage
        self.device.write(
            ":SENS:FUNC 'VOLT'; :SENS:CHAN 1;:SENS:VOLT:RANG:AUTO ON")

        self.device_name = self.device.query("*IDN?")
        print(self.device_name, ' has been connected!')

    def measure_voltage(self):
        voltage = float(self.device.query(":READ?"))
        time.sleep(0.5)
        return voltage


class SourceMeter:
    def __init__(self, rm, GPIB):
        self.rm = rm
        # Connect instrument
        self.device = self.rm.open_resource(GPIB)
        self.device.write('*RST')  # Reset Nanovoltmeter
        # Set device to source current.
        self.device_name = self.device.query("*IDN?")
        print(self.device_name, ' has been connected!')
        
        self.device.write(":SOURce:FUNCtion CURRent")
        

    def set_current(self, current):
        self.device.write(f":SOUR:CURR {current}")
        self.device.write(f":OUTP ON")

    def measure_voltage(self):
        self.device.write(":SOURce:FUNCtion CURRent")
        voltage = float(self.device.query(":MEASure:VOLTage?"))
        time.sleep(0.2)
        return voltage
