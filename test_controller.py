import numpy as np
import pyvisa

conversie = 1023 / 3.3  # van voltage naar ADC


def list_resources():
    rm = pyvisa.ResourceManager("@py")
    ports = rm.list_resources()
    return ports


class ArduinoVISADevice:
    def __init__(self, port):
        self.port = port
        rm = pyvisa.ResourceManager("@py")
        self.device = rm.open_resource(
            self.port, read_termination="\r\n", write_termination="\n"
        )

    def get_identification(self):
        identification = self.device.query("*IDN?")
        self.idenfication = identification
        return self.idenfication

    def set_output_value(self, value):
        final_value = self.device.query(f"OUT:CH0 {value}")
        return final_value

    def set_output_voltage(self, voltage):
        converted_voltage = int(voltage * conversie)
        final_value = self.device.query(f"OUT:CH0 {converted_voltage}")
        return final_value

    # measure the voltage on INPUT channel 2 in ADC values (0 - 1023)
    def get_output_value(self):
        final_value = self.device.query("MEAS:CH0?")
        return final_value

    def get_output_voltage(self):
        final_voltage = self.device.query("MEAS:CH0?") / conversie
        return final_voltage

    def get_input_value(self, channel):
        channel_ADC = int(self.device.query(f"MEAS:CH{channel}?"))
        return channel_ADC

    def get_input_voltage(self, channel):
        channel_voltage = int(self.device.query(f"MEAS:CH{channel}?")) / conversie
        return channel_voltage


# get available ports
print(list_resources())

# create an instance for the Arduino on port "ASRL4::INSTR" (dit is mijn port uit print(list_resources())
device = ArduinoVISADevice(port="ASRL4::INSTR")

# print identification string
identification = device.get_identification()
print(identification)

# set OUTPUT voltage on channel 0 in Volt (0 - 3.3 V)
response = device.set_output_voltage(voltage=3.3)
print(f"{response=}")

# set OUTPUT voltage on channel 0 in ADC values (0 - 1023)
device.set_output_value(value=828)

# measure the voltage on INPUT channel 2 in ADC values (0 - 1023)
ch2_value = device.get_input_value(channel=2)
print(f"{ch2_value=}")

# measure the voltage on INPUT channel 2 in Volt (0 - 3.3 V)
ch2_voltage = device.get_input_voltage(channel=2)
print(f"{ch2_voltage=}")

# get the previously set OUTPUT voltage on channel 0 in ADC values (0 - 1023)
ch0_value = device.get_output_value()
print(f"{ch0_value=}")

# turn of the LED
device.set_output_voltage(voltage=0)
