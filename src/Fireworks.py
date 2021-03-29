import pygame
from random import randint, uniform, choice
import math

class Trail:

    def __init__(self, n, size, dynamic, vector):
        self.vector = vector
        self.pos_in_line = n
        self.pos = self.vector(-10, -10)
        self.dynamic = dynamic
        trail_colours = [(45, 45, 45), (60, 60, 60), (75, 75, 75), (125, 125, 125), (150, 150, 150)]

        if self.dynamic:
            self.colour = trail_colours[n]
            self.size = int(size - n / 2)
        else:
            self.colour = (255, 255, 200)
            self.size = size - 2
            if self.size < 0:
                self.size = 0

    def get_pos(self, x, y):
        self.pos = self.vector(x, y)

    def show(self, win):
        pygame.draw.circle(win, self.colour, (int(self.pos.x), int(self.pos.y)), self.size)


class Particle:

    def __init__(self, x, y, firework, colour, vector):
        self.firework = firework
        self.vector = vector
        self.pos = self.vector(x, y)
        self.origin = self.vector(x, y)
        self.radius = 20
        self.remove = False
        self.explosion_radius = randint(5, 18)
        self.life = 0
        self.acc = self.vector(0, 0)
        self.trails = []  
        self.prev_posx = [-10] * 10  
        self.prev_posy = [-10] * 10  
        self.dynamic_offset = 1
        self.static_offset = 5

        if self.firework:
            self.vel = self.vector(0, -randint(17, 20))
            self.size = 5
            self.colour = colour
            for i in range(5):
                self.trails.append(Trail(i, self.size, True, self.vector))
        else:
            self.vel = self.vector(uniform(-1, 1), uniform(-1, 1))
            self.vel.x *= randint(7, self.explosion_radius + 2)
            self.vel.y *= randint(7, self.explosion_radius + 2)
            self.size = randint(2, 4)
            self.colour = choice(colour)
            for i in range(5):
                self.trails.append(Trail(i, self.size, False, self.vector))

    def apply_force(self, force):
        self.acc += force

    def move(self):
        if not self.firework:
            self.vel.x *= 0.8
            self.vel.y *= 0.8

        self.vel += self.acc
        self.pos += self.vel
        self.acc *= 0

        if self.life == 0 and not self.firework:  
            distance = math.sqrt((self.pos.x - self.origin.x) ** 2 + (self.pos.y - self.origin.y) ** 2)
            if distance > self.explosion_radius:
                self.remove = True

        self.decay()

        self.trail_update()

        self.life += 1

    def show(self, win):
        pygame.draw.circle(win, (self.colour[0], self.colour[1], self.colour[2], 0), (int(self.pos.x), int(self.pos.y)),
                           self.size)

    def decay(self):  
        if 50 > self.life > 10:  
            ran = randint(0, 30)
            if ran == 0:
                self.remove = True
        elif self.life > 50:
            ran = randint(0, 5)
            if ran == 0:
                self.remove = True

    def trail_update(self):
        self.prev_posx.pop()
        self.prev_posx.insert(0, int(self.pos.x))
        self.prev_posy.pop()
        self.prev_posy.insert(0, int(self.pos.y))

        for n, t in enumerate(self.trails):
            if t.dynamic:
                t.get_pos(self.prev_posx[n + self.dynamic_offset], self.prev_posy[n + self.dynamic_offset])
            else:
                t.get_pos(self.prev_posx[n + self.static_offset], self.prev_posy[n + self.static_offset])

class Firework:

    def __init__(self, WIDTH, HEIGHT):
        self.vector = pygame.math.Vector2
        self.colour = (randint(0, 255), randint(0, 255), randint(0, 255))
        self.colours = (
        (randint(0, 255), randint(0, 255), randint(0, 255)), (randint(0, 255), randint(0, 255), randint(0, 255)),
        (randint(0, 255), randint(0, 255), randint(0, 255)))
        self.firework = Particle(randint(0, WIDTH), HEIGHT, True,
                                 self.colour, self.vector)
        self.exploded = False
        self.particles = []
        self.min_max_particles = self.vector(100, 225)
        self.gravity = self.vector(0, 0.3)
        

    def update(self, win):  
        if not self.exploded:
            self.firework.apply_force(self.gravity)
            self.firework.move()
            for tf in self.firework.trails:
                tf.show(win)

            self.show(win)

            if self.firework.vel.y >= 0:
                self.exploded = True
                self.explode()
        else:
            for particle in self.particles:
                particle.apply_force(self.vector(self.gravity.x + uniform(-1, 1) / 20, self.gravity.y / 2 + (randint(1, 8) / 100)))
                particle.move()
                for t in particle.trails:
                    t.show(win)
                particle.show(win)

    def explode(self):
        amount = randint(self.min_max_particles.x, self.min_max_particles.y)
        for i in range(amount):
            self.particles.append(Particle(self.firework.pos.x, self.firework.pos.y, False, self.colours, self.vector))

    def show(self, win):
        pygame.draw.circle(win, self.colour, (int(self.firework.pos.x), int(self.firework.pos.y)), self.firework.size)

    def remove(self):
        if self.exploded:
            for p in self.particles:
                if p.remove is True:
                    self.particles.remove(p)

            if len(self.particles) == 0:
                return True
            else:
                return False





def update(win, fireworks):
    for fw in fireworks:
        fw.update(win)
        if fw.remove():
            fireworks.remove(fw)

    pygame.display.update()

