"""Pythondaq package

This package allows the user to run the Model (diode_experiment.py), Controller (arduino_device.py) and View (run_experiment.py) of a simulated experiment using an Arduino connected to an electric circuit.
This circuit contains a resistance of 220 ohm, an LED to emit light and multiple Voltage-meters.
The user can measure voltage and current with an ADC-value-range of their choice and how many times the experiment has to be ran before a graph is generated with the averages of the different measurements.

Along with this, the user can create multiple profiles to run multiple experiments at once, only requiring to set up multiple "devices" in the controller diode_experiment.py
"""


def main() -> None:
    print("Hello from pythondaq!")
