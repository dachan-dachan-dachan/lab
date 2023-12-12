import asyncio
import ctypes
import os
from typing import NoReturn

import numpy as np
from pyautd3 import AUTD3, Controller, Silencer
from pyautd3.gain import Focus
from pyautd3.gain import Bessel
from pyautd3.gain import Plane
from pyautd3.link.soem import SOEM, OnErrFunc
from pyautd3.modulation import Sine

from pyautd3.gain import Focus, Group, Null


import time
import math

import serial
import csv


def on_lost(msg: ctypes.c_char_p) -> NoReturn:
    print(msg.decode("utf-8"), end="")
    os._exit(-1)


def on_err(msg: ctypes.c_char_p) -> None:
    print(msg.decode("utf-8"), end="")


def element_vector(vector):#ベクトルはを入れると，その単位ベクトルを返す
    return (vector / math.sqrt(np.dot(vector, vector)))


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
#############################
        #フェーズドアレイの幅
        L_x = 10.16*18#https://shinolab.github.io/autd3/book/jp/Users_Manual/concept.html

        #フェーズドアレイの法線とのなす角[degree]
        phi = 15

        #センサの位置
        x_S = 0
        y_S = 0
        z_S = 400

        #始点
        x_L = 0
        y_L = 0
        z_L = 0

        #焦点の位置
        y_F = 0
        z_F = 200
        x_F = z_F*math.tan()

        f = 0.1
        port_ad = "COM3"
        port_num = 9600
        ser = serial.Serial(port_ad, port_num)#ポートの情報(str, int)
        csv_file = f"20231210_{phi}.csv"


        n_vector = np.array([x_F, y_F, z_F])
        r_vector = np.array([x_F - (- L_x/2), y_F, z_F])
        l_vector = np.array([x_F - (L_x/2), y_F, z_F])
        first_argument = autd.geometry.center + np.array([x_F, y_F, z_F])
        second_argument = element_vector(n_vector)
        third_argument = min(math.acos(np.dot(element_vector(r_vector), element_vector(n_vector))), math.acos(np.dot(element_vector(l_vector), element_vector(n_vector))))

        
        g_bessel = Bessel(first_argument, second_argument, third_argument)
        g = g_bessel
        m = Sine(150)

        print("照射を開始")
        start_time = time.time()
        for i in range(int(10/f)):
            value = float(ser.readline().decode("utf-8").rstrip("\n"))
            with open(csv_file, "a", newline="") as file:
                print('{}'.format(int(value)),file=file)
            time.sleep(f)
        
        await autd.send_async(m, g)
        for i in range(int(90/f)):
            value = float(ser.readline().decode("utf-8").rstrip("\n"))
            with open(csv_file, "a", newline="") as file:
                print('{}'.format(int(value)),file=file)
            time.sleep(f)

        await autd.close_async()
        for i in range(int(60/f)):
            value = float(ser.readline().decode("utf-8").rstrip("\n"))
            with open(csv_file, "a", newline="") as file:
                print('{}'.format(int(value)),file=file)
            time.sleep(f)

        end_time = time.time()
        #autd.close()
        print("照射が終了")
        print(f"実際にかかった時間は{end_time - start_time}秒です")

if __name__ == "__main__":
    asyncio.run(main())
