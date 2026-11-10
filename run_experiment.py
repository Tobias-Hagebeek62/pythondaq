import matplotlib.pyplot as plt
import numpy as np

from diode_experiment import ArduinoDevice, list_resources, meerdere_metingen

# Deze activeren op locatie
# device = ArduinoDevice(port="ASRL4::INSTR")

# Deze activeren als geen arduino beschikbaar is
device = ArduinoDevice(port="SIM")

output = meerdere_metingen()
L_voltage_AVG = output[0]
L_current_AVG = output[1]
L_STD_V = output[2]
L_STD_I = output[3]
