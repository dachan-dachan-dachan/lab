from pyautd3 import AUTD3, Controller, Silencer
from pyautd3.link.soem import SOEM, OnErrFunc
from pyautd3.gain import Focus
from pyautd3.gain import Bessel
from pyautd3.gain import Plane
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

    interval = 60
    x = 0.0
    y = 0.0
    z = 150.0
    nx = 0
    ny = 0
    nz = 1
    Lx = 192
    beam_of_kind = int(input("0:bessel,1:focus,2:plane,3:null ："))
    if beam_of_kind == 3:
        z = 0
    else:
        z = float(input("焦点の位置を入力："))
    alc = float(input("アルコールの位置を入力："))
    
    

    f = 0.1
    port_ad = 'COM3'
    port_num = 9600
    ser = serial.Serial(port_ad, port_num)#ポートの情報(str, int)

    csv_file = "20231130.csv"
        
    if beam_of_kind == 0:
        theta = math.atan2(Lx/2, z)
        g = Bessel((autd.geometry.center + np.array([x, y, z])), [nx, ny, nz], theta)
    elif beam_of_kind == 1:
        g = Focus((autd.geometry.center + np.array([x, y, z])))
    elif beam_of_kind == 2:
        g = Plane([nx, ny, nz])
    elif beam_of_kind == 3:
        g = Null()
    
    m = Sine(150)
    autd.send((m, g))
    print(f"z={z}で{interval}秒の照射を開始")

    max_value = 0.0
    min_value = 1023.0
    max_value_increased = 0.0
    before_value = 1023.0

    for i in range(int(interval/f)):
        value = float(ser.readline().decode('utf-8').rstrip('\n'))
        if max_value < value:
            max_value = value
        if min_value > value:
            min_value = value
        if max_value_increased < value - before_value:
            max_value_increased = value - before_value
        before_value = value
        time.sleep(f)

    autd.close()
    print(f"z={z}で{interval}秒の照射が終了")
    print(f'最大値：{max_value}、最大増加量：{max_value_increased}')

    with open(csv_file, 'a', newline='') as file:
        writer = csv.writer(file)
        #writer.writerow([f"{z},{max_value},{max_value_increased}"])
        date = []
        date.append(beam_of_kind)
        date.append(float(z))
        date.append(float(alc))
        date.append(int(min_value))
        date.append(int(max_value))
        date.append(int(max_value_increased))
        writer.writerow(date)

    while True:
        value = float(ser.readline().decode('utf-8').rstrip('\n'))
        print(value)
        time.sleep(f)
