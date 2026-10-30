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
def meerdere_functies():
    aantal_metingen = 0
    while aantal_metingen < 3:
        output = spanningstoename_LED()

        aantal_metingen += 1


# Slechts de belangrijke lines aangelaten
output = spanningstoename_LED()
# L_raw_LED = output[0]
L_V_LED = output[1]
# L_raw_res = output[2]
# L_V_res = output[3]
L_I_res = output[4]


def meerdere_functies():
    aantal_metingen = 0
    L_gem_spanning = []
    L_gem_stroom = []

    while aantal_metingen < 3:
        output = spanningstoename_LED()
        aantal_metingen += 1


plt.plot(L_V_LED, L_I_res)
plt.show()
