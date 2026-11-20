import csv
import math as mt

import click
import matplotlib.pyplot as plt
import numpy as np

from pythondaq.arduino_device import list_resources
from pythondaq.diode_experiment import ArduinoDevice, DiodeExperiment, list_resources

conversie = 1023 / 3.3  # van voltage naar ADC


@click.group()
def cmd_group():
    pass


@cmd_group.command("list")
def list():
    print(list_resources())


@cmd_group.command("scan")
@click.option(
    "-sa",
    "--start",
    type=click.FloatRange(0, 3.3),
    default=0,
    help="Lowest voltage tested in the experiment",
)
@click.option(
    "-so",
    "--stop",
    type=click.FloatRange(0, 3.3),
    default=3.3,
    help="Highest voltage tested in the experiment",
)
@click.option(
    "-o",
    "--output",
    default="measurements",
    help="Name of the csv file that the measurements will be saved in",
)
@click.option(
    "-r",
    "--repeat",
    default=1,
    help="How many times the experiment has to be ran before a graph gets made.",
)
@click.option(
    "--stepsize",
    default=3.3 / 1023,
    type=click.FloatRange(3.3 / 1023, 3.3),
    help="How big voltage difference should be between measurements. Given in Volts, automatically recalculated to ADC values",
)
def scan(start, stop, output, repeat, stepsize):
    # originele functie ging met ADC waardes
    stepsize_converted = stepsize * conversie
    print(stepsize_converted)
    scanresult = DiodeExperiment.scan(
        int(start * conversie), int(stop * conversie), repeat, stepsize_converted
    )
    L_voltage_AVG = scanresult[0]
    L_current_AVG = scanresult[1]
    L_STD_V = scanresult[2]
    L_STD_I = scanresult[3]
    L_voltage_tot = scanresult[4]
    L_current_tot = scanresult[5]

    # nieuwe CSV-file gemaakt, sinds de "mock-arduino" niet echte metingen zijn
    with open(f"{output}.csv", "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(
            ["Voltage [V]", "Error Voltage +/-", "Current [A]", "Error Current +/-"]
        )
        for a, b, c, d in zip(L_voltage_AVG, L_STD_V, L_current_AVG, L_STD_I):
            writer.writerow([a, b, c, d])

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
