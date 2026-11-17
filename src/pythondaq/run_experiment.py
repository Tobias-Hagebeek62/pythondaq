import csv

import matplotlib.pyplot as plt
import numpy as np

from pythondaq.diode_experiment import ArduinoDevice, DiodeExperiment, list_resources

# Deze activeren als geen arduino beschikbaar is
# device = ArduinoDevice(port="SIM")

output = DiodeExperiment.scan(0, 1023, 3)
L_voltage_AVG = output[0]
L_current_AVG = output[1]
L_STD_V = output[2]
L_STD_I = output[3]

# nieuwe CSV-file gemaakt, sinds de "mock-arduino" niet echte metingen zijn
with open("measurements.csv", "w", newline="") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(
        ["Voltage [V]", "Error Voltage +/-", "Current [A]", "Error Current +/-"]
    )
    for a, b, c, d in zip(L_voltage_AVG, L_STD_V, L_current_AVG, L_STD_I):
        writer.writerow([a, b, c, d])

# In de voorbeeldcode van de opdracht wordt gevraagd om de voltage en current +- de onzekerheid te printen, ik snap hier niet per se de meerwaarde van, en sinds ik het met lijsten heb gedaan moet het met een lelijke for-loop :(
L_Voltage_AVG_with_STD = []
L_Current_AVG_with_STD = []
for x in range(len(L_current_AVG)):
    L_Voltage_AVG_with_STD.append(L_voltage_AVG[x] - L_STD_V[x])
    L_Current_AVG_with_STD.append(L_current_AVG[x] - L_STD_I[x])
print(L_Current_AVG_with_STD)
print(L_Voltage_AVG_with_STD)


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


def main() -> None:
    """External commando

    Function that allows the file to be run via external software, like command prompt. Module can be ran by typing pythondaq in command prompt
    """
    pass


if __name__ == "__main__":
    main()
