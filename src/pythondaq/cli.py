import math as mt

import click
import numpy as np

from pythondaq.arduino_device import list_resources
from pythondaq.diode_experiment import ArduinoDevice, DiodeExperiment, list_resources


@click.group()
def cmd_group():
    pass


@cmd_group.command("list")
def list():
    print("Work in progress, list devices")
    pass


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
def scan():

    pass
