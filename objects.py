import pygame
import math

def add_vectors(angle1, length1, angle2, length2):
    x = math.sin(angle1) * length1 + math.sin(angle2) * length2
    y = math.cos(angle1) * length1 + math.cos(angle2) * length2
    length = math.hypot(x, y)
    angle = 0.5 * math.pi - math.atan2(y, x)
    return angle, length

def find_ball(particles, x, y):
    for p in particles:
        if math.hypot(p.x-x, p.y-y) <= p.size:
            return p
    return None


class Ball():

    def __init__(self, x, y, size, color):
        self.x = x
        self.y = y
        self.size = size
        self.color = color
        self.speed = 0.01
        self.angle = 0
        self.surface = pygame.display.get_surface()
        self.drag = 0.98
        self.elasticity = 0.8
    
    def display(self):
        pygame.draw.circle(self.surface, self.color, (self.x, self.y), self.size)
    
    def move(self):
        self.x += math.sin(self.angle) * self.speed
        self.y -= math.cos(self.angle) * self.speed
        # self.angle, self.speed = add_vectors(self.angle, self.speed, self.gravity[0], self.gravity[1])
        self.speed *= self.drag
    
    def bounce(self):
        width, height = self.surface.get_size()
        if self.x > width - self.size:
            self.x = 2 * (width - self.size) - self.x
            self.angle = - self.angle
            self.speed *= self.elasticity
        elif self.x < self.size:
            self.x = 2 * self.size - self.x
            self.angle = - self.angle
            self.speed *= self.elasticity
        if self.y > height - self.size:
            self.y = 2 * (height - self.size) - self.y
            self.angle = math.pi - self.angle
            self.speed *= self.elasticity
        elif self.y < self.size:
            self.y = 2 * self.size - self.y
            self.angle = math.pi - self.angle
            self.speed *= self.elasticity
    
    def collide(self, b2):
        dx = self.x - b2.x
        dy = self.y - b2.y
        
        distance = math.hypot(dx, dy)
        if distance < self.size + b2.size:
            tangent = math.atan2(dy, dx)
            self.angle = 2 * tangent - self.angle
            b2.angle = 2 * tangent - b2.angle
            self.speed, b2.speed = b2.speed+(self.speed*self.elasticity/2), self.speed
            self.speed *= b2.elasticity
            b2.speed *= self.elasticity
            angle = 0.5 * math.pi + tangent
            self.x += math.sin(angle)
            self.y -= math.cos(angle)
            b2.x -= math.sin(angle)
            b2.y += math.cos(angle)


class Hole():

    def __init__(self, x, y, size):
        self.x = x
        self.y = y
        self.size = size
        self.surface = pygame.display.get_surface()
        self.color = (0,0,0)
    
    def display(self):
        pygame.draw.circle(self.surface, self.color, (self.x, self.y), self.size)
    
    def isInHole(self, ball):
        if math.hypot(self.x-ball.x, self.y-ball.y) <= self.size:
            return True
        else:
            return False