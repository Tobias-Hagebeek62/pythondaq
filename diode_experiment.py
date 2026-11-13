"""Module that allows to run a diode experiment multiple times

This module allows the user to easily utilize the functions from arduino_device by just having to input the start and stop ADC values, and how many times the experiment needs to be ran before making graphs.
"""

import time  # noqa: F401, I001, RUF100

import pyvisa  # pyright: ignore[reportMissingImports]

import matplotlib.pyplot as plt

import csv  # noqa: F401

import numpy as np

# Deze activeren als arduino niet beschikbaar is
# from arduino_device import ArduinoVISADeviceMock as ArduinoDevice, list_resources

# Deze activeren op locatie
from arduino_device import ArduinoVISADevice as ArduinoDevice, list_resources

conversie = 1023 / 3.3  # van voltage naar ADC


class DiodeExperiment:
    """In this class, we use multiple functions from the class ArduinoDevice, imported from another file in this folder.

    This class simulates an experiment that contains a LED-light and a resistance, supported by multiple voltage-measurers and an Arduino device
    """

    def scan(start, stop, repeat):
        """This function allows the user to run the diode experiment over a customized range of ADC-values.

        These automatically get tested and the values get returned in voltage, which is more useful for physicists.
        These automatically get saved in a csv-file, which updates every time this function is called

        Args:
            start (Integer): The user can fill in what the lowest ADC value is that should be tested
            stop (Integer): The user can fill in what the highest ADC value is that should be tested
            repeat (Integer): The user can fill in how many times they want the experiment to run, giving more consistent average values

        Returns:
            L_Voltage_AVG: Returns the average voltage value over the LED, based on the different measurements on the same corresponding ADC value
            L_Current_AVG: Returns the average current value over the LED, same as above
            L_STD_V: Returns the standard deviation on the corresponding average, which can be used for errorbars in graphs
            L_STD_I: Same as above, but for the current
        """
        L_Voltage_AVG = []
        L_Current_AVG = []

        # Lijsten die alle waarden opslaan voor het measurements-bestand
        L_Voltage_tot = []
        L_Current_tot = []

        L_STD_V = []
        L_STD_I = []

        # stop +1 zodat de maximale ADC waarde 1023 is en de for-loop 1 verder moet
        for x in range(start, stop + 1, 1):
            # resetten van aantal metingen en spanning op lampje (range begint op 0)
            aantal_metingen = 0
            device.set_output_value(x)

            # tijdelijke lijsten voor het berekenen van de std en avg
            L_Voltage_temp = []
            L_Current_temp = []

            # onnodige values niet opnieuw aangeroepen, zoals raw data sum
            while aantal_metingen < repeat:
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

            L_STD_V.append(np.std(L_Voltage_temp))

            Current_AVG = np.mean(L_Current_temp)
            L_Current_AVG.append(Current_AVG)

            L_STD_I.append(np.std(L_Current_temp))

            aantal_metingen = 0

        # Na de metingen de spanningsbron uitzetten
        device.set_output_value(0)

        # nieuwe CSV-file gemaakt, sinds de "mock-arduino" niet echte metingen zijn
        with open("measurements.csv", "w", newline="") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(
                ["Voltage [V]", "Error Voltage +/-", "Current [A]", "Error Current +/-"]
            )
            for a, b, c, d in zip(L_Voltage_tot, L_STD_V, L_Current_tot, L_STD_I):
                writer.writerow([a, b, c, d])

        return L_Voltage_AVG, L_Current_AVG, L_STD_V, L_STD_I


# Deze activeren op locatie
device = ArduinoDevice(port="ASRL5::INSTR")

# Deze activeren als geen arduino beschikbaar is
# device = ArduinoDevice(port="SIM")

output = DiodeExperiment.scan(0, 1023, 3)
L_voltage_AVG = output[0]
L_current_AVG = output[1]
L_STD_V = output[2]
L_STD_I = output[3]


# Volgens voorbeeldcode moet de plot in run_experiment.py

# plt.errorbar(
#     L_voltage_AVG,
#     L_current_AVG,
#     xerr=L_STD_V,
#     yerr=L_STD_I,
#     label="Errorbars",
#     fmt="",
#     markersize=0,
# )

# # data zit verstopt achter errorbars door hoge concentratie punten
# plt.scatter(L_voltage_AVG, L_current_AVG, label="Data", s=10, alpha=0.7)

# plt.legend()
# plt.show()
