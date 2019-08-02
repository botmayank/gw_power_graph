#!/usr/bin/python

# Power supply control for GW-Instek supplies

import gpd3303s
import time
from datetime import datetime
import matplotlib.pyplot as plt
import numpy as np
import os

if not os.path.isdir("logs"):
    os.mkdir("logs")

CSV_FILE = "logs/Power_Test_" + str(datetime.now()) + ".csv"

PORT = '/dev/ttyUSB0'

CHANNEL = 1
VOLTAGE_SET = 5.01
CURRENT_LIMIT = 1.5

SAMPLING_INTERVAL = 0.05  # Seconds
gpd = gpd3303s.GPD3303S()


def init_supply(channel, port):
    gpd.open(port)

def get_voltage_reading(channel):
    return gpd.getVoltageOutput(channel)


def get_current_reading(channel):
    return gpd.getCurrentOutput(channel)


voltage_reading = []
current_reading = []
time_samples = []
combined_reading = []

CSV_HEADER = "Time, Current, Voltage"


def psp_plot():
    plt.ion()

    fig, ax1 = plt.subplots()
    ax1.set_xlabel("Time")
    ax1.set_ylabel("Voltage (V)", color='tab:blue')

    ax1.set_ylim(0, VOLTAGE_SET + 2)

    line1, = ax1.plot(time_samples, voltage_reading)
    plt.gca().xaxis.grid(True)

    ax2 = ax1.twinx()
    ax2.set_ylabel("Current (Amp)", color='tab:red')
    ax2.set_ylim(0, CURRENT_LIMIT + 0.5)

    line2, = ax2.plot(time_samples, current_reading, 'r')
    plt.grid(color='#808080', linestyle='-', linewidth=1, axis='y', alpha=0.5)
    plt.yticks(np.arange(0, CURRENT_LIMIT + 2, step=0.125))

    time_step = 0

    while True:
        try:
            time_samples.append(time_step)

            voltage_reading.append(get_voltage_reading(CHANNEL))

            line1.set_xdata(time_samples)
            line1.set_ydata(voltage_reading)

            current_reading.append(get_current_reading(CHANNEL))
            line2.set_xdata(time_samples)
            line2.set_ydata(current_reading)

            time_step += SAMPLING_INTERVAL
            time_step = round(time_step, 3)

            ax1.relim()
            ax1.autoscale_view()

            fig.canvas.draw()
            fig.canvas.flush_events()
            combined_reading.append([time_samples[-1], current_reading[-1], voltage_reading[-1]])

            time.sleep(SAMPLING_INTERVAL)

        except KeyboardInterrupt:
            gpd.close()
            print("Exiting...")
            print("Saving final readings to ", CSV_FILE)
            np.savetxt(CSV_FILE, combined_reading, delimiter=", ", fmt="%s", header=CSV_HEADER)


if __name__ == '__main__':
    init_supply(CHANNEL, PORT)
    psp_plot()
