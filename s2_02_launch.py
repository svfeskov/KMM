import matplotlib.pyplot as plt
import numpy as np
import matplotlib.animation as animation

# параметры матмодели (в единицах СИ)
dt = 0.2        # расчетный шаг по времени [s]
g = 9.81        # ускорение свободного падения [m/s^2]
R = 6.378e+6    # радиус Земли [m]
m_0 = 12500.0   # масса ракеты с топливом [kg]
m_1 = 4000.0    # масса ракеты с топливом [kg]
t_0 = 65.0      # время работы двигателя [s]
u = 2050.0      # скорость выброса реактивной струи [m/s]
D = 1.65        # диаметр корпуса корабля [m]
L = 14.03       # длина корпуса корабля [m]
F = 0.50        # коэффициент лобового сопротивления для конуса [1]
rho_0 = 1.225   # плотность воздуха на поверхности Земли [kg/m^3]
H_n = 10400     # высота атмосферы в экспоненциальной модели [m]
theta_0 = 0.0   # угол тяги [grad]

# начальные условия
h_0 = 0.0       # стартовая высота [m]
v_0 = 0.001     # стартовая скорость корабля [m/s]
alpha_0 = 0.0   # ориентация корабля [grad] {0.5; 1.0}

# границы области отображения (в км)
x_min = -10.0
x_max = +10.0
y_min = 0.0
y_max = 25.0

# вспомогательные параметры
C = (m_0 - m_1) / t_0
S = np.pi * D**2 / 2
k2_0 = 0.5 * F * S * rho_0
al_0 = alpha_0 * np.pi / 180.0
th_0 = theta_0 * np.pi / 180.0

# динамические величины c инициализацией
t = 0                               # время [s]
m = m_0                             # масса корабля [kg]
x = 0.0                             # x-координата [m]
y = h_0                             # y-координата [m]
v_x = v_0 * np.sin(al_0)            # x-компонента скорости [m/s]
v_y = v_0 * np.cos(al_0)            # y-компонента скорости [m/s]

# массивы для сохранения траектории корабля
x_array = []
y_array = []

# создаем объекты для прорисовки
fig, ax = plt.subplots()
line_1 = ax.plot(x, y, linewidth=2, color="blue")[0]
scat_1 = ax.scatter(x, y, color="red", edgecolor="grey", s=200)
text_1 = ax.text(0.05, 0.90, 't = 0, r = (0,0),\nm = 0, v = (0,0)', fontsize=12, transform=ax.transAxes)
text_2 = ax.text(0.05, 0.05, 'гравитация: a1 = (0,0),\nтрение a2 = (0,0),\nтяга a3 = (0,0)', fontsize=12, transform=ax.transAxes)
ax.set(xlim=[x_min, x_max], ylim=[y_min, y_max])
fig.set_size_inches(10,7)


def update(step):
    # эта функция вызывается на каждом шаге dt
    global v_x, v_y, x, y, m, t
    x_array.append(x / 1000)                # добавляем новую точку (x,y)
    y_array.append(y / 1000)
    v = np.sqrt(v_x**2 + v_y**2)
    pos = np.stack([x_array[step], y_array[step]]).T
    scat_1.set_offsets(pos)                 # обновляем положение корабля и его траекторию
    line_1.set_xdata(x_array)
    line_1.set_ydata(y_array)               # обновляем числовые данные на форме
    text_1.set_text(f't = {t:.2f} с, r = ({x_array[step]:.1f}, {y_array[step]:.1f}) км,\nm = {m:.0f} кг, v = ({v_x:.1f}, {v_y:.1f}) м/с')
    if t < t_0:                             # текущая масса корабля и реактивная тяга
        fc = C
        m = m_0 - C * t
    else:
        fc = 0
        m = m_1
        scat_1.set_facecolor("black")
    # k2 = 0.0                        # модель без атмосферы
    # k2 = k2_0 * np.exp(- y / H_n)   # модель с экспоненциальной плотностью атмосферы
    k2 = k2_0                       # модель с постоянной плотностью атмосферы
    theta = th_0                    # постоянный угол тяги
    # theta = - 10. * np.pi / 180.0 * np.sin( 2 * np.pi * t / 10.0 ) # переменный угол тяги
    a_1x = 0.0                      # рассчитываем ускорение, обусловленное гравитацией
    a_1y = -g / (1 + y / R)**2
    a_2x = -k2 / m * v * v_x        # рассчитываем ускорение, обусловленное сопротивлением воздуха
    a_2y = -k2 / m * v * v_y
    a_3x = fc / m * u * (v_x * np.cos(theta) - v_y * np.sin(theta)) / v   # рассчитываем ускорение,
    a_3y = fc / m * u * (v_x * np.sin(theta) + v_y * np.cos(theta)) / v   #  обусловленное реактивной тягой
    a_x = a_1x + a_2x + a_3x        # суммарное ускорение корабля
    a_y = a_1y + a_2y + a_3y
    v_x += a_x * dt                 # вычисляем значение скорости v = (v_x, v_y) на следующем шаге
    v_y += a_y * dt                 #    (явная схема Эйлера)
    x += v_x * dt                   # вычисляем значения координат r = (x, y) на следующем шаге
    y += v_y * dt                   #    (явная схема Эйлера)
    t += dt                         # увеличиваем текущее время
    text_2.set_text(f'гравитация: a1 = (0,{a_1y:.1f}),\nтрение: a2 = ({a_2x:.1f}, {a_2y:.1f}),\nтяга: a3 = ({a_3x:.1f}, {a_3y:.1f})')
    return line_1, scat_1, text_1, text_2


ani = animation.FuncAnimation(fig=fig, func=update, blit=True, cache_frame_data=False, interval=50)
plt.show()
