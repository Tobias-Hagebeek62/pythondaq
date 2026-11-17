import math as mt

import click
import numpy as np

from pythondaq.arduino_device import list_resources


@click.group()
def cmd_group():
    pass


@cmd_group.command("list")
def list():
    print("Work in progress, list devices")
    pass


@cmd_group.command("scan")
def scan():
    print("Work in progress, scan LED")
    pass
