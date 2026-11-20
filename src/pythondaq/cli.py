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
@click.option(
    "--search",
    "-s",
    help="The user can give a search-query, and the code automatically finds a corresponding device",
    default=None,
)
def list(search):
    """Prints connected devices (all, or query based), essential for DiodeExperiment as the right device has to be activated"""
    if search == None:
        print(list_resources())
    else:
        results = 0
        all_devices = list_resources()
        found_devices = []
        for x in range(len(all_devices)):
            if search in all_devices[x]:
                found_devices.append(all_devices[x])
                results += 1
        if results == 0:
            print("No devices found with query")
        else:
            print(found_devices)


@cmd_group.command("info")
@click.option(
    "--port",
    type=str,
    help="What port to get the identification string from. Useful when multiple devices are connected to the same device",
)
@click.option(
    "-qp",
    "--queryport",
    type=str,
    help="Allows user to get information of searched devices using a query, instead of requiring the exact name. Default-query is set to avoid errors as a mock-query that no real user would actually look for",
    default="6767676767676767",
)
def info(port, queryport):
    """Gets the complicated code-variant of the identification given with the subcommand list"""
    if queryport == "6767676767676767":
        print(ArduinoDevice(port).get_identification())
    else:
        found_devices = list(queryport)
        if len(found_devices) == 0:
            print("No devices found with query")
        else:
            print(f"{len(found_devices)} found, idenfication of all found devices:")
            for x in range(len(found_devices)):
                print(ArduinoDevice(found_devices[x]).get_identification())


@cmd_group.command("scan")
@click.option(
    "--port",
    type=str,
    help="What port the arduino is connected to. Use list to find name",
    required=True,
)
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
@click.option("--graph/--no-graph", default=False)
def scan(start, stop, output, repeat, stepsize, port, graph):
    """This function allows the user to run the diode experiment over a customized range of Volt-values.

    These automatically get tested and the values get returned in voltage, which is more useful for physicists.
    These automatically get saved in a csv-file, which updates every time this function is called

    PORT is the port that the user is required to give in order to examine the right arduino
    START is the lowest voltage level that has to be examined
    STOP is the highest voltage level that has to be examined
    OUTPUT is the name of the csv file (excluding .csv) where the measurements will be saved
    REPEAT is the amount of times the experiment gets ran before averages get taken and optionally a graph gets made
    STEPSIZE allows the user to tweak how specific the experiment is, with a smaller stepsize giving more detailed measurements with smaller steps in voltage inbetween
    GRAPH is a boolean that allows the user to toggle a graph. Default is set to no graph

    """
    # originele functie ging met ADC waardes
    measurements = DiodeExperiment(port)
    scanresult = measurements.scan(int(start), int(stop), repeat, stepsize)
    L_voltage_AVG = scanresult[0]
    L_current_AVG = scanresult[1]
    L_STD_V = scanresult[2]
    L_STD_I = scanresult[3]

    # nieuwe CSV-file gemaakt, sinds de "mock-arduino" niet echte metingen zijn
    with open(f"{output}.csv", "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(
            ["Voltage [V]", "Error Voltage +/-", "Current [A]", "Error Current +/-"]
        )
        for a, b, c, d in zip(L_voltage_AVG, L_STD_V, L_current_AVG, L_STD_I):
            writer.writerow([a, b, c, d])

    if graph == True:
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
