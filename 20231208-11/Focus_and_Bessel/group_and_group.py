import asyncio
import ctypes
import os
from typing import NoReturn

from pyautd3 import AUTD3, Controller, Silencer
from pyautd3.gain import Focus
from pyautd3.gain import Bessel
from pyautd3.gain import Plane
from pyautd3.link.soem import SOEM, OnErrFunc
from pyautd3.modulation import Sine

from pyautd3.gain import Focus, Group, Null

import numpy as np
import math

import time
import serial
import csv


def on_lost(msg: ctypes.c_char_p) -> NoReturn:
    print(msg.decode("utf-8"), end="")
    os._exit(-1)


def on_err(msg: ctypes.c_char_p) -> None:
    print(msg.decode("utf-8"), end="")


async def main() -> None:
    on_lost_func = OnErrFunc(on_lost)
    on_err_func = OnErrFunc(on_err)

    with await (
        Controller.builder()
        .add_device(AUTD3([0.0, 0.0, 0.0]))
        .open_with_async(
            SOEM.builder().with_on_lost(on_lost_func).with_on_err(on_err_func)
        )
    ) as autd:
        firm_info_list = await autd.firmware_info_list_async()
        print("\n".join([f"[{i}]: {firm}" for i, firm in enumerate(firm_info_list)]))

        await autd.send_async(Silencer())



        ############################準備
        f = 0.1#サンプリング周期

        #センサの位置
        x_S = 0
        y_S = 0
        z_S = 400
        #焦点の位置
        x_F = 0
        y_F = 0
        z_F = 200

        d = 0#フォーカスの焦点がベクトルの集合よりどれくらい後ろにするか

        L_x = 10.16*18#https://shinolab.github.io/autd3/book/jp/Users_Manual/concept.html
        
        x_L = (L_x*z_F)/(2*z_S)#ベッセルビームとフォーカスの境界線

        port_ad = "COM3"
        port_num = 9600
        ser = serial.Serial(port_ad, port_num)#ポートの情報(str, int)
        csv_file = f"20231210-z_S={z_S}-z_F={z_F}.csv"
        #csv_file = f"20231210-z_S={z_S}-z_F={z_F}_bessel_only.csv"
        #csv_file = "20231210_non_ethanol.csv"
        
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
        g_1 = Bessel(autd.geometry.center + np.array([x_S, y_S, z_S]), [0, 0, 1], theta)
        g_2 = Focus(autd.geometry.center + np.array([x_F, y_F, z_F - d]))
        g = (Group(lambda _, tr: "b" if tr.idx in bessel_vibrator else "f").set_gain("b", g_1).set_gain("f", g_2))
        #g = Bessel(autd.geometry.center + np.array([x_F, y_F, z_F]), [0, 0, 1], theta)
        m = Sine(150)
        ############################準備終了

        ############################サンプリング開始
        print("照射を開始")
        interval_time = []
        start_time = time.time()
        for i in range(int(30/f)):
            value = float(ser.readline().decode("utf-8").rstrip("\n"))
            with open(csv_file, "a", newline="") as file:
                print('{}'.format(int(value)),file=file)
            time.sleep(f)
        end_time = time.time()
        interval_time.append(end_time - start_time)

        start_time = time.time()
        await autd.send_async(m, g)
        for i in range(int(90/f)):
            value = float(ser.readline().decode("utf-8").rstrip("\n"))
            with open(csv_file, "a", newline="") as file:
                print('{}'.format(int(value)),file=file)
            time.sleep(f)
        end_time = time.time()
        interval_time.append(end_time - start_time)

        start_time = time.time()
        await autd.close_async()
        for i in range(int(90/f)):
            value = float(ser.readline().decode("utf-8").rstrip("\n"))
            with open(csv_file, "a", newline="") as file:
                print('{}'.format(int(value)),file=file)
            time.sleep(f)
        end_time = time.time()
        interval_time.append(end_time - start_time)

        print("照射が終了")
        print(f"Bessel：Focus={len(bessel_vibrator)}：{len(focus_vibrator)}")
        max_time = 0
        for i in range(len(interval_time)):
            max_time += interval_time[i]
        print(f"{interval_time},{max_time}")
        ############################サンプリング終了
        


if __name__ == "__main__":
    asyncio.run(main())
