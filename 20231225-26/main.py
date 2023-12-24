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

from pyautd3.modulation import Static


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


def adjustment(list):#振動子のリストをネジの分ずらす調整をする
    re_list = []
    for i in range(len(list)):#ネジの分ずらす
        if (list[i] > 20) and (list[i] < 34):
            re_list.append(list[i] - 2)
        elif list[i] > 34:
            re_list.append(list[i] - 3)
        elif list[i] < 19:
            re_list.append(list[i])
    return re_list



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

        #センサの位置
        x_S = 0
        y_S = 0
        z_S = 400

        #始点
        x_L = L_x / 4
        y_L = 0
        z_L = 0

        #焦点の位置
        x_F = x_L
        y_F = 0
        z_F = 200

        f = 0.1
        port_ad = "COM3"
        port_num = 9600
        ser = serial.Serial(port_ad, port_num)#ポートの情報(str, int)
        csv_file = f"20231210-z_S={z_S}-z_F={z_F}.csv"


        #ベッセルビームとフォーカスの境界線
        #x_L = (L_x*z_F)/(2*z_S)

        bottom_line = min(math.fabs((L_x/2)-x_L), math.fabs(x_L+(L_x/2)))

        first_argument = autd.geometry.center + np.array([x_F, y_F, z_F])
        second_argument = [0,0,1]
        third_argument = math.atan2(z_F, bottom_line)

        bessel_vibrator = []
        non_vibrator = []
        for i in range(0, 18*14):
            if i == 19 or i == 20 or i == 34:
                pass
            elif (i%18) >= (18*2/3):#後ろから見て左側(2)
                bessel_vibrator.append(i)
            else:#右側(1)
                non_vibrator.append(i)
                

        bessel_vibrator_A = adjustment(bessel_vibrator)
        bessel_vibrator_B= adjustment(non_vibrator)
###########################
        g_bessel_A = Bessel(first_argument, second_argument, third_argument)
        #g_bessel_A = Null()
        g_bessel_B = Bessel(first_argument, second_argument, third_argument)
        #g_bessel_B = Null()
        
        g = (Group(lambda _, tr: "A" if tr.idx in bessel_vibrator_A else "B").set_gain("A", g_bessel_A).set_gain("B", g_bessel_B))
        #m = Sine(150)
        m = Static()#変調無し

        print("照射を開始")
        start_time = time.time()
        for i in range(int(10/f)):
            value = float(ser.readline().decode("utf-8").rstrip("\n"))
            with open(csv_file, "a", newline="") as file:
                print('{}'.format(int(value)),file=file)
            time.sleep(f)
        
        await autd.send_async(m, g)
        for i in range(int(40/f)):
            value = float(ser.readline().decode("utf-8").rstrip("\n"))
            with open(csv_file, "a", newline="") as file:
                print('{}'.format(int(value)),file=file)
            time.sleep(f)

        await autd.close_async()
        for i in range(int(10/f)):
            value = float(ser.readline().decode("utf-8").rstrip("\n"))
            with open(csv_file, "a", newline="") as file:
                print('{}'.format(int(value)),file=file)
            time.sleep(f)

        end_time = time.time()
        #autd.close()
        print("照射が終了")
        print(f"実際にかかった時間は{end_time - start_time}秒です")
        print(f"A：B={len(bessel_vibrator_A)}：{len(bessel_vibrator_B)}")
        for i in range(18*14 - 1, -1, -1):
            if i%18 == 17:
                print("\n")
                if i == 19 or i == 20 or i == 34:
                    print("X")
                elif bessel_vibrator[i] == i:
                    print("A")
                else:
                    print("B")
        print(f"ファイル名：{csv_file}")

if __name__ == "__main__":
    asyncio.run(main())
