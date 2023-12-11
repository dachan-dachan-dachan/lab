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

import math


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

        g_1 = Focus(autd.geometry.center + np.array([50, 0.0, 150.0]))
        g_2 = Focus(autd.geometry.center + np.array([-50, 0.0, 150.0]))
        g_2 = Bessel(autd.geometry.center + np.array([0, 0, 50]), [0, 0, 1], 0.5)
        

        g = (Group(lambda _, tr: "null" if tr.idx <= 100 else "focus").set_gain("null", g_2).set_gain("focus", g_1))


        x_S = 0
        y_S = 0
        z_S = 400
        x_F = 0
        y_F = 0
        z_F = 200
        L_x = 10.16*18#https://shinolab.github.io/autd3/book/jp/Users_Manual/concept.html
        x_L = (L_x*z_F)/(2*z_S)
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
        g_2 = Focus(autd.geometry.center + np.array([x_F, y_F, z_F]))
        #g = (Group(lambda _, tr: bessel_vibrator if tr.idx in bessel_vibrator else focus_vibrator).set_gain(bessel_vibrator, g_1).set_gain(focus_vibrator, g_2))
        g = (Group(lambda _, tr: "b" if tr.idx in bessel_vibrator else "f").set_gain("b", g_1).set_gain("f", g_2))


        m = Sine(150)
        await autd.send_async(m, g)

        _ = input()

        await autd.close_async()


if __name__ == "__main__":
    asyncio.run(main())
