# моделирование системы Солнце + Земля

import matplotlib.pyplot as plt
from s2_01_bodies import PlanetarySystem, Star, Planet

T_m = 8.640e+4      # масштаб времени в секундах (здесь - сутки)
R_m = 1.496e+11     # масштаб пространства в метрах (здесь - расстояние от Земли до Солнца)
M_m = 5.973e+24     # масштаб массы в килограммах (здесь - масса Земли)
G_0 = 6.674e-11     # гравитационная постоянная в системе СИ

view_size = 2.5                                     # размер области отображения в единицах R_m
solar_sys = PlanetarySystem()                       # создаем объект класса PlanetarySystem
solar_sys.G_1 = G_0 * M_m * T_m**2 / R_m**3         # рассчитываем G в новой системе единиц
solar_sys.dT = 1.0                                  # шаг по времени
shadow = True                                       # включаем "тени" объектов на визуализации

sun = Star(solar_sys, mass=332940)                  # помещаем Солнце в центр

earth = Planet(                                     # помещаем Землю на круговую орбиту
        solar_sys,
        mass=1.0,
        position=(1, 0, 0),
        velocity=(0, 0.0172, 0),
        color=(0.0, 0.7, 0.0)
    )
solar_sys.selected = 1                              # следим за объектом под номером 1 (Земля)

fig = plt.figure()
ax = fig.add_subplot(projection='3d')


def set_view():
    ax.clear()
    ax.view_init(90, 0)  # уголы обзора в градусах
    fig.tight_layout()
    ax.set_xlim((-view_size / 2, view_size / 2))
    ax.set_ylim((-view_size / 2, view_size / 2))
    ax.set_zlim((-view_size / 2, view_size / 2))
    ax.xaxis.set_ticklabels([])
    ax.yaxis.set_ticklabels([])
    ax.zaxis.set_ticklabels([])
    r = solar_sys.bodies[solar_sys.selected].position
    v = solar_sys.bodies[solar_sys.selected].velocity
    t = solar_sys.T
    ax.text2D(0.05, 0.90,
              f't = {t:.1f}\nr = ({r[0]: .3f}, {r[1]: .3f}, {r[2]: .3f})\nv = ({v[0]: .3f}, {v[1]: .3f}, {v[2]: .3f})',
              transform=ax.transAxes)


def draw_body(body):
    ax.scatter(*body.position, marker="o",
               s=body.display_size1 * view_size,
               color=body.color)
    if shadow:
        pos = body.position
        ax.scatter(pos[0], pos[1], -view_size / 2, marker="o",
                   s=body.display_size1 * view_size,
                   color=(.7, .7, .7))


while True:
    solar_sys.calc_interactions()
    solar_sys.do_step()
    set_view()
    for single_body in solar_sys.bodies:
        draw_body(single_body)
    plt.pause(0.001)

