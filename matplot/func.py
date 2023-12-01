import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np


def func(x):#両対数における折れ線近似
    if x < 100:
        return 101*(x**(-0.85))
    else:
        return 35*(x**(-0.62))


background_image = mpimg.imread('b.png')#画像の読み込み

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
x_values = np.logspace(1, 4, 100000)
y_values = []
for i in x_values:
    y_values.append(func(i))
ax_log.plot(x_values, y_values, label='func', color='blue', linestyle='--')

ax_log.grid(True)

#axの軸の数値を非表示
ax.set_xticks([])
ax.set_yticks([])

# グラフの表示
plt.show()
