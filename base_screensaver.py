import pygame
import random
import math
import time
import colorsys

class ScreenSaver:
    def __init__(self, name: str, duration: int = 5000):
        self.name = name
        self.duration = duration
        self.start_time = time.time()
        self.particles = []
        self.objects = []
        self.phase = 0
        self.colors = []
        self.generate_colors()

    def generate_colors(self):
        """Generate vibrant, ADHD-friendly colors"""
        self.colors = []
        for i in range(20):
            hue = (i * 18) % 360
            saturation = random.uniform(0.7, 1.0)
            value = random.uniform(0.8, 1.0)
            rgb = colorsys.hsv_to_rgb(hue/360, saturation, value)
            self.colors.append(tuple(int(c * 255) for c in rgb))

    def is_finished(self):
        return time.time() - self.start_time > self.duration / 1000

    def update(self):
        pass

    def draw(self, surface):
        pass

class Particle:
    def __init__(self, x, y, color, velocity, size=2):
        self.x = x
        self.y = y
        self.color = color
        self.velocity = velocity
        self.size = size
        self.life = 255
        self.decay = random.uniform(1, 3)

    def update(self):
        self.x += self.velocity[0]
        self.y += self.velocity[1]
        self.life -= self.decay
        self.size = max(0, self.size - 0.1)

    def draw(self, surface):
        if self.life > 0:
            alpha = int(self.life)
            color_with_alpha = (*self.color, alpha)
            pygame.draw.circle(surface, color_with_alpha, (int(self.x), int(self.y)), int(self.size)) 