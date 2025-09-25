import matplotlib.pyplot as plt
import numpy as np
import matplotlib.animation as animation

# параметры матмодели
g = 9.81        # ускорение свободного падения [m/s^2]
R = 6.378e+6    # радиус Земли [m]
m_0 = 12500.0   # масса ракеты с топливом [kg]
m_1 = 4000.0    # масса ракеты с топливом [kg]
t_0 = 65.0      # время работы двигателя [s]
u = 2050.0      # скорость выброса реактивной струи [m/s]
D = 1.65        # диаметр корпуса корабля [m]
L = 14.03       # длина корпуса корабля [m]
F = 0.50        # коэффициент лобового сопротивления для конуса [1]
rho_0 = 1.204   # плотность воздуха на поверхности Земли [kg/m^3]

h_0 = 0.0       # начальная высота над поверхностью [m]
v_0 = 0.01      # начальная скорость корабля [m/s]
alpha_0 = 0.0   # направление начальной скорости [grad]
theta_0 = 0.0   # угол тяги [grad]

num_steps = 2000
t_max = 200.0
dt = t_max / num_steps
h_max = R
r_scale = 1000
x_min = -25.0  #(-R - h_max) / r_scale
x_max = +25.0  #(+R + h_max) / r_scale
y_min = R / r_scale #(-R - h_max) / r_scale
y_max = (R + 20000) / r_scale #(+R + h_max) / r_scale
C = (m_0 - m_1) / t_0
S = np.pi * D**2 / 2
k2 = 0.5 * F * S * rho_0
al_0 = alpha_0 * np.pi / 180.0
th_0 = theta_0 * np.pi / 180.0

# текущие значения динамических величин + инициализация
t = 0                               # время [s]
m = m_0                             # масса корабля [kg]
x = 0.0                             # [m]
y = R + h_0                         # [m]
v_x = v_0 * np.sin(al_0)            # [m/s]
v_y = v_0 * np.cos(al_0)            # [m/s]

# массивы для расчета траектории
t_array = np.linspace(0, t_max, num_steps + 1)
x_array = 0 * t_array
y_array = 0 * t_array
phi = np.linspace(0, 2 * np.pi, 361)
R_x = R * np.cos(phi) / r_scale
R_y = R * np.sin(phi) / r_scale

fig, ax = plt.subplots()
line_1 = ax.plot(R_x, R_y, linewidth=3, color="black")[0]
line_2 = ax.plot(x, y, linewidth=3, color="blue")[0]
scat_1 = ax.scatter(x, y, color="magenta", edgecolor="black", s=200)
text_1 = ax.text(0.05, 0.95, 't = 0, h = 0', transform=ax.transAxes)
text_2 = ax.text(0.05, 0.90, 'vx = 0, vy = 0', transform=ax.transAxes)
text_3 = ax.text(0.05, 0.05, 'a1x = 0, a1y = 0, a2x = 0, a2y = 0, a3x = 0, a3y = 0', transform=ax.transAxes)
ax.set(xlim=[x_min, x_max], ylim=[y_min, y_max])


def init():
    global v_x, v_y, x, y, m
    m = m_0
    x = 0.0
    y = R + h_0
    v_x = v_0 * np.sin(al_0)
    v_y = v_0 * np.cos(al_0)
    text_1.set_text("t = 0.0")
    return line_2, scat_1, text_1, text_2, text_3


def update(step):
    global v_x, v_y, x, y, m, t
    x_array[step] = x / r_scale
    y_array[step] = y / r_scale
    v = np.sqrt(v_x**2 + v_y**2)
    r = np.sqrt(x**2 + y**2)
    pos = np.stack([x_array[step], y_array[step]]).T
    scat_1.set_offsets(pos)
    line_2.set_xdata(x_array[:step])
    line_2.set_ydata(y_array[:step])
    text_1.set_text(f't = {t:.2f} с, x = {x/r_scale:.0f} км, y = {y/r_scale:.0f} км, m = {m:.0f} кг')
    text_2.set_text(f'h = {r-R:.0f} м, vx = {v_x:.0f} м/с, vy = {v_y:.0f} м/с')
    # рассчитываем значения (x,y,t) на следующем шаге dt
    gr = g * (R / r)**2
    if t < t_0:
        fc = C
        m = m_0 - C * t
    else:
        fc = 0
        m = m_1
    a_1x = -gr * x / r
    a_1y = -gr * y / r
    a_2x = -k2 / m * v * v_x
    a_2y = -k2 / m * v * v_y
    a_3x = fc / m * u * (v_x * np.cos(th_0) - v_y * np.sin(th_0)) / v
    a_3y = fc / m * u * (v_x * np.sin(th_0) + v_y * np.cos(th_0)) / v
    a_x = a_1x + a_2x + a_3x
    a_y = a_1y + a_2y + a_3y
    v_x += a_x * dt
    v_y += a_y * dt
    x += v_x * dt
    y += v_y * dt
    t += dt
    text_3.set_text(f'a1x = {a_1x:.0f}, a1y = {a_1y:.0f}, a2x = {a_2x:.0f}, a2y = {a_2y:.0f}, a3x = {a_3x:.0f}, a3y = {a_3y:.0f}')
    return line_2, scat_1, text_1, text_2, text_3


ani = animation.FuncAnimation(fig=fig, func=update, init_func=init,
                              blit=True, frames=num_steps+1, interval=100)
plt.show()
