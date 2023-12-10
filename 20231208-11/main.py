from pyautd3 import AUTD3, Controller, Silencer
from pyautd3.link.soem import SOEM, OnErrFunc
from pyautd3.gain import Bessel
from pyautd3.gain import Focus
from pyautd3.gain import Null
from pyautd3.modulation import Sine
#from pyautd3 import AUTD3, Gain, Focus, BesselBeam

import numpy as np

import os
import ctypes

import time
import math

import serial
import csv


def on_lost(msg: ctypes.c_char_p):
    print(msg.decode("utf-8"), end="")
    os._exit(-1)


if __name__ == "__main__":
    on_lost_func = OnErrFunc(on_lost)

    autd = (
        Controller.builder()
        .add_device(AUTD3.from_euler_zyz([0.0, 0.0, 0.0], [0.0, 0.0, 0.0]))
        .open_with(SOEM.builder().with_on_lost(on_lost_func))
    )

    firm_info_list = autd.firmware_info_list()
    print("\n".join([f"[{i}]: {firm}" for i, firm in enumerate(firm_info_list)]))

    autd.send(Silencer())

    interval = 60*3
    x = 0.0
    y = 0.0
    z = 200
    d = 50
    Lx = 10.16*18#https://shinolab.github.io/autd3/book/jp/Users_Manual/concept.html

    f = 0.1
    port_ad = "COM3"
    port_num = 9600
    ser = serial.Serial(port_ad, port_num)#ポートの情報(str, int)

    csv_file = f"20231210_z={z}_d={d}.csv"
    
    theta = math.atan2(Lx/2, z)
    bessel_beam_even = Bessel((autd.geometry.center + np.array([x, y, z + d])), [0, 0, 1], theta)
    #bessel_beam_even = BesselBeam(np.array([0, 0, 150.0]), 30000.0, 0)
    autd.append_gain(bessel_beam_even, range(1, autd.num_devices, 2))

    focus_odd = Focus(autd.geometry.center + np.array([x, y, z]))
    autd.append_gain(focus_odd, range(0, autd.num_devices, 2))

    #m = Sine(150)
    #autd.send((m, g))
    #autd.send()

    with open(csv_file, "a", newline="") as file:
        value = f"Bessel:{bessel_beam_even}\nFocus:{focus_odd}\nd:{d}"
        file.writerow(value)

    print("照射を開始")

    start_time = time.time()

    for i in range(int(30/f)):
        value = float(ser.readline().decode("utf-8").rstrip("\n"))
        with open(csv_file, "a", newline="") as file:
            file.writerow(value)
        time.sleep(f)
    
    autd.send()
    for i in range(int(90/f)):
        value = float(ser.readline().decode("utf-8").rstrip("\n"))
        with open(csv_file, "a", newline="") as file:
            file.writerow(value)
        time.sleep(f)

    autd.close()
    for i in range(int(90/f)):
        value = float(ser.readline().decode("utf-8").rstrip("\n"))
        with open(csv_file, "a", newline="") as file:
            file.writerow(value)
        time.sleep(f)

    end_time = time.time()
    #autd.close()
    print("照射が終了")
    print(f"実際にかかった時間は{end_time - start_time}秒です")

    with open(csv_file, "a", newline="") as file:
        value = end_time - start_time
        file.writerow(value)
    

    import winsound
    winsound.Beep(2000, 500)
