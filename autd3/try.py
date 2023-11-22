from pyautd3 import AUTD3, Controller, Silencer
from pyautd3.link.soem import SOEM, OnErrFunc
from pyautd3.gain import Focus
from pyautd3.modulation import Sine

import numpy as np

import os
import ctypes

import time
import math

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

    t = 0
    omega = 0.01
    r = 50
    x = 0.0
    y = 0.0
    z = 150.0
    z_0 = 150.0
    time = 0.0
    while True:
        start_time = time.perf_counter()
        t += omega
        
        z = 100*(1+math.sin(t))
        x = r*math.cos(t)
        y = r*math.sin(t)
        
        time.sleep(omega)
        print(f"t={t},x={x},y={y},z={z},time={time}")

        g = Focus(autd.geometry.center + np.array([x, y, z]))
        m = Sine(150)
        autd.send((m, g))

        end_time = time.perf_counter()
        time += (end_time - start_time)

    _ = input()

    autd.close()
