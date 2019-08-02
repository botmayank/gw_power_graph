#!/usr/bin/python

# Power supply control for GW-Instek supplies

import gpd3303s
import time

PORT = '/dev/ttyUSB0'
# PORT = 'COM12'

CHANNEL = 1
VOLTAGE_SET = 5.01
CURRENT_LIMIT = 1.5

SAMPLING_INTERVAL = 0.1  # Seconds
gpd = gpd3303s.GPD3303S()


def init_supply(channel, port):
    gpd.open(port)

    # Switch off power supply output
    gpd.enableOutput(False)
    gpd.setVoltage(channel, VOLTAGE_SET)
    gpd.setCurrent(channel, CURRENT_LIMIT)
    time.sleep(1)

    # Switch on power supply output
    gpd.enableBeep(True)
    gpd.enableOutput(True)


if __name__ == '__main__':
    print("Initializing Supply!")
    init_supply(CHANNEL, PORT)
