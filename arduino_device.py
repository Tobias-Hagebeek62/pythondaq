import numpy as np

# nodig voor de "mock-arduino"
import pandas as pd
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


# Zat een college thuis en moet dus zonder Arduino tests doen. Hierom een "mock-arduino" opgevraagd zodat er in ieder geval een resultaat is en de code gecheckt kan worden
class ArduinoVISADeviceMock:
    def __init__(self, port):
        self.port = port
        self.is_simulated = port == "SIM"

        if self.is_simulated:
            print("[MOCK] Draait in simulatiemodus (thuis zonder hardware).")
            self.current_x = 0
            self.measurement_counter = {}
            try:
                self.df_mock = pd.read_csv("measurements.csv")
            except Exception:
                self.df_mock = None
        else:
            rm = pyvisa.ResourceManager("@py")
            self.device = rm.open_resource(
                self.port, read_termination="\r\n", write_termination="\n"
            )

    def get_identification(self):
        if self.is_simulated:
            return "Arduino Mock Device, Diode Experiment"
        return self.device.query("*IDN?")

    def set_output_value(self, value):
        self.current_x = int(value)
        if self.is_simulated:
            if self.current_x not in self.measurement_counter:
                self.measurement_counter[self.current_x] = 0
            return str(value)
        else:
            return self.device.query(f"OUT:CH0 {value}")

    def set_output_voltage(self, voltage):
        converted_voltage = int(voltage * conversie)
        return self.set_output_value(converted_voltage)

    def get_output_value(self):
        if self.is_simulated:
            return str(self.current_x)
        return self.device.query("MEAS:CH0?")

    def get_output_voltage(self):
        return float(self.get_output_value()) / conversie

    def get_input_value(self, channel):
        if self.is_simulated:
            conversie_val = 1023 / 3.3
            if self.df_mock is not None and len(self.df_mock) >= 3072:
                idx_base = self.current_x * 3
                sub_idx = self.measurement_counter.get(self.current_x, 0) % 3
                row_idx = min(idx_base + sub_idx, len(self.df_mock) - 1)
                self.measurement_counter[self.current_x] = sub_idx + 1

                row = self.df_mock.iloc[row_idx]
                voltage_led = row["Voltage"]
                current_res = row["Current"]
                v_res = current_res * 220

                if channel == 1:
                    val = (voltage_led + v_res) * conversie_val
                elif channel == 2:
                    val = v_res * conversie_val
                else:
                    val = 0
                return int(np.clip(val, 0, 1023))
            return 0
        else:
            return int(self.device.query(f"MEAS:CH{channel}?"))

    def get_input_voltage(self, channel):
        return self.get_input_value(channel) / conversie
