import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np
import math


def func(x):#両対数軸に描画する関数
    return np.sqrt(x)


background_image = mpimg.imread('a.png')#画像の読み込み

fig, ax = plt.subplots()

ax.set_xlim(0, 100)
ax.set_ylim(0, 100)

ax.set_aspect('equal', adjustable='box')

ax.imshow(background_image, extent=[0, 100, 0, 100], aspect='auto', alpha=0.5)#画像を背景に設定

ax.grid(True)

#両対数軸を追加
ax_log = fig.add_axes(ax.get_position(), frameon=False)
ax_log.set_xscale('log')
ax_log.set_yscale('log')
ax_log.set_xlim(10, 10000)
ax_log.set_ylim(0.1, 100)


#関数を描写
x_values = np.logspace(np.log10(10), np.log10(10000), 1000)
y_values = func(x_values)
ax_log.plot(x_values, y_values, label='func(x) = sqrt(x)', color='blue')

ax_log.grid(True)

#axの軸の数値を非表示
ax.set_xticks([])
ax.set_yticks([])

# グラフの表示
plt.show()
