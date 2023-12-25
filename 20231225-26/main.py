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


def p_p_d(x_1, y_1, x_2, y_2):
    return math.sprt(((x_1 - x_2)**2) + ((y_1 - y_2)**2))

def cosine_theorem(a, b, c):
    rad_b_c = math.acos( ( (b**2) + (c**2) - (a**2) ) / (2*b*c) )
    return rad_b_c


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
        L_y = 10.16*14

        r_A = 200#右側(1)
        theat_x_A = 0#degree，反時計回りが正，フェーズドアレイから垂直方向が0．
        #theat_x_A = -20, -10, 0, 10
        center_x_A = L_x / 6
        center_y_A = L_y / 2
        x_F_A = r_A*math.cos(math.radians(theat_x_A))
        y_F_A = center_y_A
        z_F_A = r_A*math.sin(math.radians(theat_x_A))

        r_B = 400#左側(2)
        theat_x_B = 60#degree，反時計回りが正，フェーズドアレイから垂直方向が0．
        center_x_B = 2*L_x / 3
        center_y_B = L_y / 2
        x_F_B = r_B*math.cos(math.radians(theat_x_B))
        y_F_B = center_y_B
        z_F_B = r_B*math.sin(math.radians(theat_x_B))
        

        f = 0.1
        port_ad = "COM3"
        port_num = 9600
        ser = serial.Serial(port_ad, port_num)#ポートの情報(str, int)
        csv_file = f"20231225_theat={theat_x_A}_with.csv"
        #csv_file = f"20231225_theat={theat_x_A}_without.csv"
        #csv_file = f"20231225_only.csv"


        first_argument_A = np.array([x_F_A + center_x_A, y_F_A, z_F_A])
        second_argument_A = [math.cos(math.radians(theat_x_A)),0,math.sin(math.radians(theat_x_A))]
        third_argument_A = cosine_theorem(center_x_A, r_A, p_p_d(0, 0, x_F_A + center_x_A, z_F_A))

        first_argument_B = np.array([x_F_B + center_x_B, y_F_B, z_F_B])
        second_argument_B = [math.cos(math.radians(theat_x_B)),0,math.sin(math.radians(theat_x_B))]
        third_argument_B = cosine_theorem(L_x - center_x_B, r_B, p_p_d(L_x, 0, x_F_B + center_x_B, z_F_B))

        bessel_vibrator = []
        non_vibrator = []
        for i in range(0, 18*14):
            if i == 19 or i == 20 or i == 34:
                pass
            elif (i%18) >= (11):#後ろから見て左側(2)
                bessel_vibrator.append(i)
            else:#右側(1)
                non_vibrator.append(i)
                

        bessel_vibrator_B = adjustment(bessel_vibrator)
        bessel_vibrator_A= adjustment(non_vibrator)
###########################
        g_bessel_A = Bessel(first_argument_A, second_argument_A, third_argument_A)
        #g_bessel_A = Null()
        g_bessel_B = Bessel(first_argument_B, second_argument_B, third_argument_B)
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
            if i == 19 or i == 20 or i == 34:
                print("X", end="")
            elif bessel_vibrator[i] == i:
                print("A", end="")
            else:
                print("B", end="")
            if i%18 == 17:
                print("\n")
        print(f"ファイル名：{csv_file}")

if __name__ == "__main__":
    asyncio.run(main())
