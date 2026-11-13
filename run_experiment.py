import matplotlib.pyplot as plt
import numpy as np

from diode_experiment import ArduinoDevice, DiodeExperiment, list_resources

# Deze activeren als geen arduino beschikbaar is
# device = ArduinoDevice(port="SIM")

output = DiodeExperiment.scan(0, 1023, 3)
L_voltage_AVG = output[0]
L_current_AVG = output[1]
L_STD_V = output[2]
L_STD_I = output[3]

# In de voorbeeldcode van de opdracht wordt gevraagd om de voltage en current +- de onzekerheid te printen, ik snap hier niet per se de meerwaarde van, en sinds ik het met lijsten heb gedaan moet het met een lelijke for-loop :(
L_Voltage_AVG_with_STD = []
L_Current_AVG_with_STD = []
for x in range(len(L_current_AVG)):
    L_Voltage_AVG_with_STD.append(L_voltage_AVG[x] - L_STD_V[x])
    L_Current_AVG_with_STD.append(L_current_AVG[x] - L_STD_I[x])
print(L_Current_AVG_with_STD)
print(L_Voltage_AVG_with_STD)


# CSV-file al gemaakt in diode_experiment, snap niet waarom hij dan hier gemaakt moet worden als het daar al in de functie zit

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
