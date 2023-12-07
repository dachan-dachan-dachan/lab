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

    interval = 60*3
    x = 0.0
    y = 0.0
    z = 400
    nx = 0
    ny = 0
    nz = 1
    Lx = 10.16*18#https://shinolab.github.io/autd3/book/jp/Users_Manual/concept.html


    height = 0
    x_M = Lx / 2
    rate_n_vector_x = 1.2
    

    #センサS
    x_S = 0
    y_S = height
    z_S = 400

    #第一引：数焦点F
    x_F = 60
    #x_F = -50#-60
    y_F = height
    z_F = 150#200

    #第二引数：円錐の中心の単位ベクトルn
    temp_vector = np.array([-x_F*rate_n_vector_x, height, z_S - z_F])
    n_vector = temp_vector / (math.sqrt(temp_vector.dot(temp_vector)))
    
    #母線の単位ベクトルm
    temp_vector = np.array([x_F - x_M, height, z_F])
    m_vector = temp_vector / (math.sqrt(temp_vector.dot(temp_vector)))
    
    #第三引数：θ
    theta = math.acos(n_vector.dot(m_vector))
    
    f = 0.1
    port_ad = 'COM3'
    port_num = 9600
    ser = serial.Serial(port_ad, port_num)#ポートの情報(str, int)

    csv_file = "l.csv"
    
    #theta = math.atan2(Lx/2, z)
    #g = Bessel((autd.geometry.center + np.array([x, y, z])), [nx, ny, nz], theta)
    g = Bessel((autd.geometry.center + np.array([x_F, height, z_F])), n_vector, theta)
    #g = Null()
    
    m = Sine(150)

    if (ser.readline().decode('UTF-8').rstrip('\n')).replace(',', ''):
        print("True")

    with open(csv_file, 'a', newline='') as file:
        print('{}'.format(f"{autd.geometry.center + np.array([x_F, height, z_F])},{n_vector},{theta}"),file=file)

    print(f"z={z}で{interval}秒の照射を開始")

    autd.send((m, g))
    start_time = time.time()
    for i in range(int(interval/f)):
        value = (ser.readline().decode('UTF-8').rstrip('\n')).replace(',', '')
        with open(csv_file, 'a', newline='') as file:
            print('{}'.format(int(value)),file=file)
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
    #winsound.Beep(2000, 1000)
