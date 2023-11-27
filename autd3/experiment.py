from pyautd3 import AUTD3, Controller, Silencer
from pyautd3.link.soem import SOEM, OnErrFunc
#from pyautd3.gain import Focus
from pyautd3.gain import Bessel
#from pyautd3.gain import Plane
from pyautd3.modulation import Sine

import numpy as np

import os
import ctypes

import time
import math


def z_route(now, start, end, velocity, f):
    if start <= end:
        if now < end:
            now += velocity*f
        else:
            now = start
    else:
        if end < now:
            now -= velocity*f
        else:
            now = start
    return now


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

    interval = 0.5# 0.5 sごとに周期を回す
    
    x = 0.0
    y = 0.0
    z = 0.0
    nx = 0
    ny = 0
    nz = 1
    Lx = 192# 横幅(mm)
    start = 0# 0 mm スタート
    end = 3000# 3000 mm 終了(センサの位置)
    velocity = 10# 10 mm/s (焦点の移動する速度)
    theta = math.atan2(Lx/2, z)
    _ = input()
    print("start")
        while True:
            theta = math.atan2(Lx/2, z)
            z = z_route(z, start, end, velocity, interval)
            g = Bessel([x, y, z], [nx, ny, nz], theta)
            m = Sine(150)
            autd.send((m, g))
            time.sleep(interval)
    autd.close()
