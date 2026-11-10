import time  # noqa: F401, I001, RUF100

import pyvisa  # pyright: ignore[reportMissingImports]

import matplotlib.pyplot as plt

import csv  # noqa: F401

import numpy as np

# Deze activeren als arduino niet beschikbaar is
from arduino_device import ArduinoVISADeviceMock as ArduinoDevice, list_resources

# Deze activeren op locatie
# from arduino_device import ArduinoVISADevice as ArduinoDevice, list_resources

conversie = 1023 / 3.3  # van voltage naar ADC


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

    # nieuwe CSV-file gemaakt, sinds de "mock-arduino" niet echte metingen zijn
    with open("measurements2.csv", "w", newline="") as csvfile:
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


# Deze activeren op locatie
# device = ArduinoDevice(port="ASRL4::INSTR")

# Deze activeren als geen arduino beschikbaar is
device = ArduinoDevice(port="SIM")

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
plt.scatter(L_voltage_AVG, L_current_AVG, label="Data", s=10, alpha=0.7)

plt.legend()
plt.show()
