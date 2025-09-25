# определения классов PlanetarySystem, CelestialBody, Star, Planet

import math
from s2_01_vector import Vector


class PlanetarySystem:
    def __init__(self):
        self.bodies = []
        self.G_1 = 1.0      # гравитационная постоянная в пользовательской системе единиц
        self.T = 0.0        # текущее время в пользовательской системе единиц (в единицах T_m)
        self.dT = 1.0       # расчетный шаг по времени в пользовательской системе единиц (в единицах T_m)
        self.selected = -1  # индекс "выделенного" объекта

    def add_body(self, body):
        self.bodies.append(body)

    def do_step(self):
        for body in self.bodies:
            body.move()
        self.T += self.dT

    def calc_interactions(self):
        bodies_copy = self.bodies.copy()
        for idx, first in enumerate(bodies_copy):
            for second in bodies_copy[idx + 1:]:
                first.calc_acceleration(second)


class CelestialBody:
    min_display_size = 50
    display_log_base = 1.1

    def __init__(
        self,
        planetary_system,
        mass,
        position=(0, 0, 0),
        velocity=(0, 0, 0),
        color=(0, 0, 0)
    ):
        self.planetary_system = planetary_system
        self.mass = mass
        self.position = position
        self.velocity = Vector(*velocity)
        self.display_size0 = max(
            math.log(self.mass, self.display_log_base),
            self.min_display_size,
        )
        self.display_size1 = self.display_size0 + self.position[0]
        self.color = color
        self.planetary_system.add_body(self)

    def move(self):
        dt = self.planetary_system.dT
        self.position = (
            self.position[0] + self.velocity[0] * dt,
            self.position[1] + self.velocity[1] * dt,
            self.position[2] + self.velocity[2] * dt,
        )
        self.display_size1 = self.display_size0 + self.position[0]

    def calc_acceleration(self, other):
        dt = self.planetary_system.dT
        g_1 = self.planetary_system.G_1
        dr = Vector(*other.position) - Vector(*self.position)
        dr_mag = dr.get_magnitude()

        force_mag = g_1 * self.mass * other.mass / (dr_mag ** 2)
        force = dr.normalize() * force_mag

        reverse = 1
        for body in self, other:
            acceleration = force / body.mass
            body.velocity += acceleration * reverse * dt
            reverse = -1


class Star(CelestialBody):
    def __init__(
        self,
        planetary_system,
        mass=10_000,
        position=(0, 0, 0),
        velocity=(0, 0, 0),
        color=(1, 0, 0)
    ):
        super(Star, self).__init__(planetary_system, mass, position, velocity)
        self.color = color


class Planet(CelestialBody):
    def __init__(
        self,
        planetary_system,
        mass=10,
        position=(0, 0, 0),
        velocity=(0, 0, 0),
        color=(0, 1, 0)
    ):
        super(Planet, self).__init__(planetary_system, mass, position, velocity)
        self.color = color
