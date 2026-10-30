import math as mt  # noqa: F401


# overbodig
def L_ADC():
    L_ADC = []
    for x in range(1, 1024):
        L_ADC.append(x)  # noqa: PERF402
    return L_ADC


# overbodig
def L_voltage():
    L_voltage = []
    for x in range(0, 3.3, 0.003):
        L_voltage.append(x)  # noqa: PERF402
    return L_voltage


def ADC_to_Voltage(ADC):
    Maximale_voltage = 3.3
    Aantal_stappen = 1023
    Stapsgrootte = Maximale_voltage / Aantal_stappen
    Voltage = ADC * Stapsgrootte

    return Voltage


def Voltage_to_ADC(Voltage):
    Maximale_ADC = 1023
    Maximale_Voltage = 3.3
    Stapsgrootte = Maximale_ADC / Maximale_Voltage
    ADC = Voltage * Stapsgrootte

    return ADC


print(f"{ADC_to_Voltage(700)}V")
print(f"{Voltage_to_ADC(2.28)}")
