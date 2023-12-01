import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np


def func(x):#両対数軸に描画する関数
    #return 80*(x**(-0.8)) + 0.08
    return 40*(x**(-0.65))#全体的に近い直線
    #return 100*(x**(-0.85))#先頭が正確
    #return 30*(x**(-0.6))#後ろが正確
    #return 3*(10*(x**(-0.85)) + 8*(x**(-0.6)))
    
"""def func_2(x):#両対数における折れ線近似
    if x < 100:
        return 100*(x**(-0.85))
    elif 100 <= x < 200:
        return 40*(x**(-0.65))
        #return 39*(x**(-0.65))
    elif 200 <= x < 1000:
        return 35*(x**(-0.62))
        #return 32*(x**(-0.61))
        #return 35*(x**(-0.63))
        #return 37*(x**(-0.63))
    elif 1000 <= x:
        #return 30*(x**(-0.6))
        #return 32*(x**(-0.61))
        return 35*(x**(-0.62))"""

def func_2(x):#両対数における折れ線近似
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
x_values = np.logspace(np.log10(10), np.log10(10000), 1000)
y_values = func(x_values)
#####
y_values = []
for i in x_values:
    y_values.append(func_2(i))
#####
ax_log.plot(x_values, y_values, label='func(x) = sqrt(x)', color='blue')

ax_log.grid(True)

#axの軸の数値を非表示
ax.set_xticks([])
ax.set_yticks([])

# グラフの表示
plt.show()
