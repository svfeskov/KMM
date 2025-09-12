import matplotlib.pyplot as plt
import numpy as np
import matplotlib.animation as animation

# физические параметры модели
g = 9.81        # ускорение свободного падения [m/s^2]
m = 1.00        # масса тела [kg]
v_0 = 12.0      # начальная скорость [m/s]
th_0 = 45.0     # угол вылета [grad]
x_0 = 0.0       # начальное значение х [m]
y_0 = 0.0       # начальное значение y [m]
k2 = 0.03        # коэффициент вязкого трения [kg/m]
u = -20         # скорость бокового ветра [m/s]

# вычислительные параметры
num_steps = 1000
t_max = 1.7
x_max = 16.0
y_max = 4.0
A = k2 / m
theta_0 = th_0 * np.pi / 180
v_x0 = v_0 * np.cos(theta_0)
v_y0 = v_0 * np.sin(theta_0)
dt = t_max / num_steps

# переменные для хранения текущих значений физических величин
t = 0                      # текущее время
x, y = x_0, y_0            # текущие координаты
v_x, v_y = v_x0, v_y0      # текущая скорость

# формируем массивы для аналитического решения (точки на графике)
t_a = np.linspace(0, t_max, 21)
x_a = v_x0 * t_a                   # используем известное аналитическое решение
y_a = v_y0 * t_a - g * t_a**2 / 2  # для заполнения массивов x и y

# формируем массивы для численного решения (сплошная линия на графике)
t_n = np.linspace(0, t_max, num_steps + 1)
x_n = 0 * t_n                      # вначале массивы x и y заполняем нулями
y_n = 0 * t_n

# создаем объекты для прорисовки графиков
fig, ax = plt.subplots()
line_n = ax.plot(x_n[0], y_n[0], linewidth=3, color="black", label='numerical')[0]
line_a = ax.scatter(x_a, y_a, color="blue", s=15, label='analytical')
scat_b = ax.scatter(x_n[0], y_n[0], color="magenta", edgecolor="black", s=200)
text_t = ax.text(0.05, 0.95, 't = 0', transform=ax.transAxes)
ax.set(xlim=[0, x_max], ylim=[0, y_max], xlabel='X [m]', ylabel='Y [m]')
ax.legend()

def init():
    """ Функция для инициализации анимационной картинки.
    Сбрасывает все переменные до начальных значений """
    global v_x, v_y, x, y, t
    v_x, v_y = v_x0, v_y0
    x, y = x_0, y_0
    t = 0.0
    text_t.set_text("t = 0.0")
    return line_n, scat_b, text_t

def update(step):
    """ Функция update_func() используется для анимации движения тела.
    Прорисовывает очередной кадр анимации, причем номер кадра
    передается в функцию как параметр (step).
    Данная реализация функции рассчитывает координаты тела на
    очередном шаге по времени и обновляет координаты на графике """

    # выводим на график текущие значения
    global v_x, v_y, x, y, t
    x_n[step] = x
    y_n[step] = y
    pos = np.stack([x, y]).T
    scat_b.set_offsets(pos)
    line_n.set_xdata(x_n[:step])
    line_n.set_ydata(y_n[:step])
    text_t.set_text(f't = {t:.2f}, x = {y:.3f}, y = {y:.3f}')
    # затем рассчитываем значения (x,y,t) на следующем шаге dt
    v = np.sqrt((v_x-u)**2 + v_y**2)
    f_x = 0.0 - A * v * (v_x - u)
    f_y = - g - A * v * v_y
    v_x += f_x * dt
    v_y += f_y * dt
    x += v_x * dt
    y += v_y * dt
    t += dt
    return line_n, scat_b, text_t


ani = animation.FuncAnimation(fig=fig, func=update, init_func=init,
                              blit=True, frames=num_steps+1, interval=5)
plt.show()
