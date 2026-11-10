import time  # noqa: F401, I001, RUF100

import pyvisa  # pyright: ignore[reportMissingImports]

import matplotlib.pyplot as plt

import csv  # noqa: F401

import numpy as np

from arduino_device import ArduinoVISADevice, list_resources

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


def spanningstoename_LED():
    # conversiefactor die hetzelfde doet als ADC_to_Voltage(), voor overzichtelijkheid
    conversie = 3.3 / 1023

    # lijsten voor grafiek
    L_raw_LED = []
    L_V_LED = []

    L_raw_res = []
    L_V_res = []

    # stroomsterkte LED = stroomsterkte resistance
    L_I_res = []

    for x in range(0, 1024, 1):
        spanningsbron = int(device.query(f"OUT:CH0 {x}"))
        final_value = int(device.query("MEAS:CH1?"))
        Voltage = final_value * conversie

        L_raw_LED.append(final_value)
        L_V_LED.append(Voltage)

        final_value_resistance = int(device.query("MEAS:CH2?"))
        Voltage_resistance = final_value_resistance * conversie

        # Weerstand = 220 Ohm
        Current_resistance = Voltage_resistance / 220
        L_I_res.append(Current_resistance)

        L_raw_res.append(final_value_resistance)
        L_V_res.append(Voltage_resistance)

        # print statement voor opdracht start script. Ruwe waardes zijn de ADC waardes. Deze is later uitgeschakeld om de terminal niet vol te spammen
        # print(
        #     f"ruwe waarde spanning over LED = {final_value}, voltage over LED = {Voltage}V, ruwe waarde spanning over weerstand = {final_value_resistance}, voltage over weerstand = {Voltage_resistance}V"
        # )

    # uitzetten LED
    device.query("OUT:CH0 0")

    return L_raw_LED, L_V_LED, L_raw_res, L_V_res, L_I_res


# print(    f"final_value = {spanningstoename_LED()[0]}, Voltage = {spanningstoename_LED()[1]}, ruwe waarde spanning over weerstand")
def meerdere_metingen():

    L_Voltage_AVG = []
    L_Current_AVG = []

    # Lijsten die alle waarden opslaan voor het measurements-bestand
    L_Voltage_tot = []
    L_Current_tot = []

    L_STD_V = []
    L_STD_I = []

    for x in range(0, 1024, 1):
        # resetten van aantal metingen en spanning op lampje (range begint op 0)
        aantal_metingen = 0
        device.set_output_value(x)

        # tijdelijke lijsten voor het berekenen van de std en avg
        L_Voltage_temp = []
        L_Current_temp = []

        # onnodige values niet opnieuw aangeroepen, zoals raw data sum
        while aantal_metingen < 3:
            final_value1 = device.get_input_value(1)
            final_value_2 = device.get_input_value(2)

            # met behulp van TA gekeken naar schakeling en de correcte spanning over LED opgevraagd
            Voltage = (final_value1 - final_value_2) / conversie
            L_Voltage_temp.append(Voltage)
            L_Voltage_tot.append(Voltage)

            Voltage_resistance = final_value_2 / conversie
            # I = U/R
            Current_resistance = Voltage_resistance / 220
            L_Current_temp.append(Current_resistance)
            L_Current_tot.append(Current_resistance)

            aantal_metingen += 1

        Voltage_AVG = np.mean(L_Voltage_temp)
        L_Voltage_AVG.append(Voltage_AVG)

        L_STD_V.append(std(L_Voltage_temp))

        Current_AVG = np.mean(L_Current_temp)
        L_Current_AVG.append(Current_AVG)

        L_STD_I.append(std(L_Current_temp))

        aantal_metingen = 0

    # Na de metingen de spanningsbron uitzetten
    device.set_output_value(0)

    with open("measurements.csv", "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Voltage", "Current"])
        for a, b in zip(L_Voltage_tot, L_Current_tot):
            writer.writerow([a, b])

    return L_Voltage_AVG, L_Current_AVG, L_STD_V, L_STD_I


# np.std ontweken en in plaats daarvan deze gebruikt. Hierdoor wordt namelijk de steekproef-standaardafwijking berekend in plaats van de populatie-standaardafwijking
def std(L_values):
    if len(L_values) < 2:
        return 0.0
    return np.std(L_values, ddof=1)


device = ArduinoVISADevice(port="ASRL4::INSTR")

# Slechts de belangrijke lines aangelaten, deze hierna uitgezet naarmate de opdracht verder ging
# output = spanningstoename_LED()
# L_raw_LED = output[0]
# L_V_LED = output[1]
# L_raw_res = output[2]
# L_V_res = output[3]
# L_I_res = output[4]

output = meerdere_metingen()
L_voltage_AVG = output[0]
L_current_AVG = output[1]
L_STD_V = output[2]
L_STD_I = output[3]


plt.errorbar(
    L_voltage_AVG,
    L_current_AVG,
    xerr=L_STD_V,
    yerr=L_STD_I,
    label="Errorbars",
    fmt="",
    markersize=0,
)

# data zit verstopt achter errorbars door hoge concentratie punten
plt.plot(L_voltage_AVG, L_current_AVG, label="Data", markersize=3)

plt.legend()
plt.show()
