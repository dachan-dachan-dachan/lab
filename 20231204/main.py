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

    interval = 60*10
    x = 0.0
    y = 0.0
    z = 150.0
    nx = 0
    ny = 0
    nz = 1
    Lx = 192

    f = 0.1
    port_ad = 'COM3'
    port_num = 9600
    ser = serial.Serial(port_ad, port_num)#ポートの情報(str, int)

    csv_file = "20231204_straight.csv"
    #csv_file = "20231204_oblique.csv"
    
    theta = math.atan2(Lx/2, z)
    g = Bessel((autd.geometry.center + np.array([x, y, z])), [nx, ny, nz], theta)
    #g = Null()
    
    m = Sine(150)
    autd.send((m, g))
    print(f"z={z}で{interval}秒の照射を開始")

    start_time = time.time()
    for i in range(int(interval/f)):
        value = float(ser.readline().decode('utf-8').rstrip('\n'))
        with open(csv_file, 'a', newline='') as file:
            writer.writerow(value)
        time.sleep(f)
    end_time = time.time()
    autd.close()
    print(f"z={z}で{interval}秒の照射が終了")
    with open(csv_file, 'r') as file:
        reader = csv.reader(file)
        row = sum(1 for row in reader)
    print(f"{interval}秒で設定して{f}秒ごとにデータを取り，csvファイルには{row}個のデータが格納された")
    print(f"実際にかかった時間は{end_time - start_time}秒です")
    
    import winsound
    winsound.Beep(2000, 1000)

