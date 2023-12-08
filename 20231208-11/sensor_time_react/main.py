from pyautd3 import AUTD3, Controller, Silencer
from pyautd3.link.soem import SOEM, OnErrFunc
from pyautd3.gain import Bessel
from pyautd3.gain import Null
from pyautd3.modulation import Sine

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
    
    f = 0.1
    port_ad = 'COM3'
    port_num = 9600
    ser = serial.Serial(port_ad, port_num)#ポートの情報(str, int)
    csv_file = "20231208_react_time"

    Lx = 10.16*18#https://shinolab.github.io/autd3/book/jp/Users_Manual/concept.html
    focus_point = (autd.geometry.center + np.array([0, 0, 200]))
    n_vector = np.array([0, 0, 1])
    theata = math.atan2(Lx/2, 200)
    m = Sine(150)



    g = Null()
    interval = 30
    autd.send((m, g))
    start_time = time.time()
    for i in range(int(interval/f)):
        value = float(ser.readline().decode('utf-8').rstrip('\n'))
        with open(f"{csv_file}_1.csv", 'a', newline='') as file:
            file.writerow(value)
        time.sleep(f)
    end_time = time.time()
    #autd.close()
    with open(f"{csv_file}_1.csv", 'a', newline='') as file:
        file.writerow(end_time - start_time)
    
    g = Bessel(focus_point, n_vector, theata)
    interval = 30
    autd.send((m, g))
    start_time = time.time()
    for i in range(int(interval/f)):
        value = float(ser.readline().decode('utf-8').rstrip('\n'))
        with open(f"{csv_file}_2.csv", 'a', newline='') as file:
            file.writerow(value)
        time.sleep(f)
    end_time = time.time()
    #autd.close()
    with open(f"{csv_file}_2.csv", 'a', newline='') as file:
        file.writerow(end_time - start_time)

    g = Null()
    interval = 60*9
    autd.send((m, g))
    start_time = time.time()
    for i in range(int(interval/f)):
        value = float(ser.readline().decode('utf-8').rstrip('\n'))
        with open(f"{csv_file}_3.csv", 'a', newline='') as file:
            file.writerow(value)
        time.sleep(f)
    end_time = time.time()
    #autd.close()
    with open(f"{csv_file}_3.csv", 'a', newline='') as file:
        file.writerow(end_time - start_time)
    
    autd.close()

    import winsound
    winsound.Beep(2000, 500)
