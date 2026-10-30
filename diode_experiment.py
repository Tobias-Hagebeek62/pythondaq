import time  # noqa: F401, I001, RUF100

import pyvisa  # pyright: ignore[reportMissingImports]

import matplotlib.pyplot as plt

rm = pyvisa.ResourceManager("@py")

ports = rm.list_resources()

device = rm.open_resource(
    "ASRL4::INSTR", read_termination="\r\n", write_termination="\n"
)


def ADC_to_Voltage(ADC):
    Maximale_voltage = 3.3
    Aantal_stappen = 1023
    Stapsgrootte = Maximale_voltage / Aantal_stappen
    Voltage = ADC * Stapsgrootte

    return Voltage


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
    aantal_metingen = 0
    conversie = 3.3 / 1023

    L_Voltage_AVG = []
    L_Current_AVG = []

    L_Voltage = []
    L_Current = []

    L_STD_V = []
    L_STD_I = []

    for x in range(0, 1024, 1):
        # resetten van sommen
        Voltage_sum = 0
        Current_resistance_sum = 0

        # onnodige values niet opnieuw aangeroepen, zoals raw data sum
        while aantal_metingen < 3:
            spanningsbron = int(device.query(f"OUT:CH0 {x}"))
            final_value = int(device.query("MEAS:CH1?"))

            Voltage = final_value * conversie
            Voltage_sum += Voltage
            L_Voltage.append(Voltage)

            final_value_resistance = int(device.query("MEAS:CH2?"))

            Voltage_resistance = final_value_resistance * conversie
            Current_resistance = Voltage_resistance / 220
            L_Current.append(Current_resistance)

            Current_resistance_sum += Current_resistance

            device.query("OUT:CH0 0")
            aantal_metingen += 1

        Voltage_AVG = Voltage_sum / aantal_metingen
        L_Voltage_AVG.append(Voltage_AVG)

        L_STD_V.append(std(L_Voltage, Voltage_AVG))

        Current_AVG = Current_resistance_sum / aantal_metingen
        L_Current_AVG.append(Current_AVG)

        L_STD_I.append(std(L_Current_AVG, Current_AVG))

        aantal_metingen = 0

    return L_Voltage_AVG, L_Current_AVG, L_STD_V, L_STD_I


def std(L_values, avg):
    steps = 0
    while steps < len(L_values):
        # element is 1 punt in de sum
        L_element = []
        L_element.append((((L_values[0] - avg) ** 2) / len(L_values)) ** 0.5)

        steps += 1
    std = sum(L_element)
    return std


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


plt.plot(
    L_voltage_AVG,
    L_current_AVG,
)
plt.errorbar(
    L_voltage_AVG, L_current_AVG, xerr=L_STD_V, yerr=L_STD_I, label="Errorbars", fmt="o"
)
plt.legend()
plt.show()
