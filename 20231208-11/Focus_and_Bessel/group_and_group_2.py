from pyautd3 import AUTD3, Controller, Silencer
from pyautd3.link.soem import SOEM, OnErrFunc
from pyautd3.gain import Bessel
from pyautd3.gain import Focus
from pyautd3.gain import Null
from pyautd3.gain import Group
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
    
    #センサの位置
    x_S = 0
    y_S = 0
    z_S = 400

    #焦点の位置
    x_F = 0
    y_F = 0
    z_F = 200

    #フェーズドアレイの幅
    L_x = 10.16*18#https://shinolab.github.io/autd3/book/jp/Users_Manual/concept.html


    #ベッセルビームとフォーカスの境界線
    x_L = (L_x*z_F)/(2*z_S)



    f = 0.1
    port_ad = "COM3"
    port_num = 9600
    ser = serial.Serial(port_ad, port_num)#ポートの情報(str, int)

    csv_file = f"20231210-z_S={z_S}-z_F={z_F}.csv"
    

    bessel_vibrator = []
    focus_vibrator = []
    for i in range(0, 18*14):
        if i == 19 or i == 20 or i == 34:
            pass
        elif ((i%18) < 17*(((L_x/2) - x_L)/L_x)) or ((i%18) > 17*(((L_x/2) + x_L)/L_x)):#外側
            bessel_vibrator.append(i)
        else:#内側
            focus_vibrator.append(i)

    for i in range(len(bessel_vibrator)):#ネジの分ずらす
        if (bessel_vibrator[i] > 20) and (bessel_vibrator[i] < 34):
            bessel_vibrator[i] -= 2
        elif bessel_vibrator[i] > 34:
            bessel_vibrator[i] -= 3
    
    for i in range(len(focus_vibrator)):#ネジの分ずらす
        if (focus_vibrator[i] > 20) and (focus_vibrator[i] < 34):
            focus_vibrator[i] -= 2
        elif focus_vibrator[i] > 34:
            focus_vibrator[i] -= 3


    theta = math.atan2(L_x/2, z_S)
    g = (Group(lambda _, tr: bessel_vibrator if tr.idx in bessel_vibrator else focus_vibrator)
    .set_gain(bessel_vibrator, Bessel((autd.geometry.center + np.array([x_S, y_S, z_S])), [0, 0, 1], theta))
    .set_gain(focus_vibrator, Focus(autd.geometry.center + np.array([x_F, y_F, z_F]))))

    m = Sine(150)

    print("照射を開始")

    start_time = time.time()

    for i in range(int(30/f)):
        value = float(ser.readline().decode("utf-8").rstrip("\n"))
        with open(csv_file, "a", newline="") as file:
            file.writerow(value)
        time.sleep(f)
    
    autd.send((m, g))
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
    print(f"Bessel：Focus={len(bessel_vibrator)}：{len(focus_vibrator)}")

    with open(csv_file, "a", newline="") as file:
        value = end_time - start_time
        file.writerow(value)
    

    import winsound
    winsound.Beep(2000, 500)
