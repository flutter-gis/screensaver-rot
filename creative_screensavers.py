import pygame
import random
import math
import time
import colorsys
import numpy as np
from typing import List, Tuple, Dict, Any
from base_screensaver import ScreenSaver, Particle, SCREEN_WIDTH, SCREEN_HEIGHT

# Creative and themed screen savers
class SpaceWarp(ScreenSaver):
    def __init__(self):
        super().__init__("Space Warp", 8000)
        self.stars = []
        self.generate_stars()

    def generate_stars(self):
        for _ in range(200):
            star = {
                'x': random.uniform(-SCREEN_WIDTH, SCREEN_WIDTH * 2),
                'y': random.uniform(-SCREEN_HEIGHT, SCREEN_HEIGHT * 2),
                'z': random.uniform(0, 1000),
                'speed': random.uniform(1, 5),
                'color': random.choice(self.colors)
            }
            self.stars.append(star)

    def update(self):
        self.phase += 0.02
        for star in self.stars:
            star['z'] -= star['speed']
            if star['z'] < 1:
                star['z'] = 1000
                star['x'] = random.uniform(-SCREEN_WIDTH, SCREEN_WIDTH * 2)
                star['y'] = random.uniform(-SCREEN_HEIGHT, SCREEN_HEIGHT * 2)

    def draw(self, surface):
        center_x, center_y = SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2
        
        # Sort stars by Z for proper depth
        sorted_stars = sorted(self.stars, key=lambda s: s['z'], reverse=True)
        
        for star in sorted_stars:
            # 3D to 2D projection
            scale = 200 / star['z']
            x = center_x + (star['x'] - center_x) * scale
            y = center_y + (star['y'] - center_y) * scale
            
            if 0 <= x < SCREEN_WIDTH and 0 <= y < SCREEN_HEIGHT:
                size = max(1, 5 - star['z'] / 200)
                pygame.draw.circle(surface, star['color'], (int(x), int(y)), int(size))

class Fireworks(ScreenSaver):
    def __init__(self):
        super().__init__("Fireworks", 6000)
        self.fireworks = []
        self.particles = []

    def create_firework(self):
        x = random.randint(100, SCREEN_WIDTH - 100)
        y = random.randint(100, SCREEN_HEIGHT - 100)
        color = random.choice(self.colors)
        
        for _ in range(50):
            angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(2, 8)
            velocity = (speed * math.cos(angle), speed * math.sin(angle))
            self.particles.append(Particle(x, y, color, velocity, random.uniform(2, 6)))

    def update(self):
        self.phase += 0.02
        
        # Update particles
        for particle in self.particles[:]:
            particle.update()
            if particle.life <= 0:
                self.particles.remove(particle)
        
        # Create new fireworks
        if len(self.particles) < 20:
            self.create_firework()

    def draw(self, surface):
        for particle in self.particles:
            particle.draw(surface)

class ButterflyGarden(ScreenSaver):
    def __init__(self):
        super().__init__("Butterfly Garden", 9000)
        self.butterflies = []
        self.generate_butterflies()

    def generate_butterflies(self):
        for _ in range(15):
            butterfly = {
                'x': random.randint(50, SCREEN_WIDTH - 50),
                'y': random.randint(50, SCREEN_HEIGHT - 50),
                'vx': random.uniform(-1, 1),
                'vy': random.uniform(-1, 1),
                'color': random.choice(self.colors),
                'size': random.uniform(10, 25),
                'wing_angle': random.uniform(0, 2 * math.pi),
                'wing_speed': random.uniform(0.1, 0.3)
            }
            self.butterflies.append(butterfly)

    def update(self):
        self.phase += 0.02
        for butterfly in self.butterflies:
            butterfly['x'] += butterfly['vx']
            butterfly['y'] += butterfly['vy']
            butterfly['wing_angle'] += butterfly['wing_speed']
            
            # Bounce off walls
            if butterfly['x'] < 0 or butterfly['x'] > SCREEN_WIDTH:
                butterfly['vx'] *= -1
            if butterfly['y'] < 0 or butterfly['y'] > SCREEN_HEIGHT:
                butterfly['vy'] *= -1

    def draw_butterfly(self, surface, x, y, wing_angle, size, color):
        # Draw butterfly wings
        wing1_x = x + size * math.cos(wing_angle)
        wing1_y = y + size * math.sin(wing_angle)
        wing2_x = x + size * math.cos(wing_angle + math.pi)
        wing2_y = y + size * math.sin(wing_angle + math.pi)
        
        pygame.draw.circle(surface, color, (int(wing1_x), int(wing1_y)), int(size/2))
        pygame.draw.circle(surface, color, (int(wing2_x), int(wing2_y)), int(size/2))
        pygame.draw.circle(surface, color, (int(x), int(y)), 3)

    def draw(self, surface):
        for butterfly in self.butterflies:
            self.draw_butterfly(surface, butterfly['x'], butterfly['y'],
                              butterfly['wing_angle'], butterfly['size'], butterfly['color'])

class UnderwaterBubbles(ScreenSaver):
    def __init__(self):
        super().__init__("Underwater Bubbles", 7000)
        self.bubbles = []
        self.fish = []
        self.generate_underwater()

    def generate_underwater(self):
        # Generate bubbles
        for _ in range(30):
            bubble = {
                'x': random.randint(50, SCREEN_WIDTH - 50),
                'y': SCREEN_HEIGHT + random.randint(0, 100),
                'size': random.uniform(5, 20),
                'speed': random.uniform(1, 3),
                'color': (100, 150, 255)
            }
            self.bubbles.append(bubble)
        
        # Generate fish
        for _ in range(8):
            fish = {
                'x': random.randint(100, SCREEN_WIDTH - 100),
                'y': random.randint(100, SCREEN_HEIGHT - 100),
                'vx': random.uniform(-2, 2),
                'vy': random.uniform(-1, 1),
                'color': random.choice(self.colors),
                'size': random.uniform(10, 25)
            }
            self.fish.append(fish)

    def update(self):
        self.phase += 0.02
        
        # Update bubbles
        for bubble in self.bubbles:
            bubble['y'] -= bubble['speed']
            if bubble['y'] < -bubble['size']:
                bubble['y'] = SCREEN_HEIGHT + bubble['size']
                bubble['x'] = random.randint(50, SCREEN_WIDTH - 50)
        
        # Update fish
        for fish in self.fish:
            fish['x'] += fish['vx']
            fish['y'] += fish['vy']
            
            # Bounce off walls
            if fish['x'] < 0 or fish['x'] > SCREEN_WIDTH:
                fish['vx'] *= -1
            if fish['y'] < 0 or fish['y'] > SCREEN_HEIGHT:
                fish['vy'] *= -1

    def draw_fish(self, surface, x, y, size, color):
        # Draw fish body
        pygame.draw.ellipse(surface, color, (x - size, y - size/2, size * 2, size))
        
        # Draw tail
        tail_points = [(x - size, y), (x - size - 10, y - size/2), (x - size - 10, y + size/2)]
        pygame.draw.polygon(surface, color, tail_points)

    def draw(self, surface):
        # Draw underwater background
        surface.fill((0, 50, 100))
        
        # Draw bubbles
        for bubble in self.bubbles:
            pygame.draw.circle(surface, bubble['color'], 
                             (int(bubble['x']), int(bubble['y'])), int(bubble['size']))
        
        # Draw fish
        for fish in self.fish:
            self.draw_fish(surface, fish['x'], fish['y'], fish['size'], fish['color'])

class AbstractPainting(ScreenSaver):
    def __init__(self):
        super().__init__("Abstract Painting", 8000)
        self.brush_strokes = []
        self.generate_strokes()

    def generate_strokes(self):
        for _ in range(50):
            stroke = {
                'start_x': random.randint(0, SCREEN_WIDTH),
                'start_y': random.randint(0, SCREEN_HEIGHT),
                'end_x': random.randint(0, SCREEN_WIDTH),
                'end_y': random.randint(0, SCREEN_HEIGHT),
                'color': random.choice(self.colors),
                'width': random.randint(3, 15),
                'alpha': random.randint(100, 255)
            }
            self.brush_strokes.append(stroke)

    def update(self):
        self.phase += 0.01

    def draw(self, surface):
        for stroke in self.brush_strokes:
            # Animate stroke position
            offset_x = math.sin(self.phase + stroke['start_x'] * 0.01) * 10
            offset_y = math.cos(self.phase + stroke['start_y'] * 0.01) * 10
            
            start_x = stroke['start_x'] + offset_x
            start_y = stroke['start_y'] + offset_y
            end_x = stroke['end_x'] + offset_x
            end_y = stroke['end_y'] + offset_y
            
            pygame.draw.line(surface, stroke['color'], 
                           (start_x, start_y), (end_x, end_y), stroke['width'])

class DigitalRainbow(ScreenSaver):
    def __init__(self):
        super().__init__("Digital Rainbow", 6000)
        self.pixels = []
        self.generate_pixels()

    def generate_pixels(self):
        for x in range(0, SCREEN_WIDTH, 4):
            for y in range(0, SCREEN_HEIGHT, 4):
                pixel = {
                    'x': x,
                    'y': y,
                    'hue': random.uniform(0, 360),
                    'speed': random.uniform(0.5, 2.0)
                }
                self.pixels.append(pixel)

    def update(self):
        self.phase += 0.02
        for pixel in self.pixels:
            pixel['hue'] = (pixel['hue'] + pixel['speed']) % 360

    def draw(self, surface):
        for pixel in self.pixels:
            rgb = colorsys.hsv_to_rgb(pixel['hue']/360, 0.8, 1.0)
            color = tuple(int(c * 255) for c in rgb)
            pygame.draw.circle(surface, color, (pixel['x'], pixel['y']), 2)

class MagneticField(ScreenSaver):
    def __init__(self):
        super().__init__("Magnetic Field", 7000)
        self.poles = []
        self.generate_poles()

    def generate_poles(self):
        for _ in range(8):
            pole = {
                'x': random.randint(100, SCREEN_WIDTH - 100),
                'y': random.randint(100, SCREEN_HEIGHT - 100),
                'strength': random.uniform(0.5, 2.0),
                'type': random.choice(['north', 'south']),
                'color': random.choice(self.colors)
            }
            self.poles.append(pole)

    def update(self):
        self.phase += 0.03

    def draw(self, surface):
        # Draw field lines
        for x in range(0, SCREEN_WIDTH, 20):
            for y in range(0, SCREEN_HEIGHT, 20):
                force_x, force_y = 0, 0
                
                for pole in self.poles:
                    dx = x - pole['x']
                    dy = y - pole['y']
                    distance = math.sqrt(dx*dx + dy*dy) + 1
                    
                    if pole['type'] == 'north':
                        force_x -= pole['strength'] * dx / (distance * distance)
                        force_y -= pole['strength'] * dy / (distance * distance)
                    else:
                        force_x += pole['strength'] * dx / (distance * distance)
                        force_y += pole['strength'] * dy / (distance * distance)
                
                # Normalize and draw
                magnitude = math.sqrt(force_x*force_x + force_y*force_y)
                if magnitude > 0.1:
                    force_x /= magnitude
                    force_y /= magnitude
                    
                    hue = (magnitude * 100 + self.phase * 50) % 360
                    rgb = colorsys.hsv_to_rgb(hue/360, 0.8, 1.0)
                    color = tuple(int(c * 255) for c in rgb)
                    
                    end_x = x + force_x * 15
                    end_y = y + force_y * 15
                    pygame.draw.line(surface, color, (x, y), (end_x, end_y), 2)

class CrystalGrowth(ScreenSaver):
    def __init__(self):
        super().__init__("Crystal Growth", 10000)
        self.crystals = []
        self.generate_crystals()

    def generate_crystals(self):
        for _ in range(20):
            crystal = {
                'x': random.randint(100, SCREEN_WIDTH - 100),
                'y': random.randint(100, SCREEN_HEIGHT - 100),
                'size': random.uniform(5, 30),
                'color': random.choice(self.colors),
                'growth_rate': random.uniform(0.1, 0.5),
                'max_size': random.uniform(20, 60),
                'rotation': random.uniform(0, 2 * math.pi)
            }
            self.crystals.append(crystal)

    def update(self):
        self.phase += 0.02
        for crystal in self.crystals:
            crystal['size'] = min(crystal['max_size'], 
                                crystal['size'] + crystal['growth_rate'] * math.sin(self.phase))
            crystal['rotation'] += 0.01

    def draw_crystal(self, surface, x, y, size, rotation, color):
        points = []
        for i in range(6):
            angle = rotation + i * math.pi / 3
            px = x + size * math.cos(angle)
            py = y + size * math.sin(angle)
            points.append((px, py))
        
        if len(points) >= 3:
            pygame.draw.polygon(surface, color, points)
            pygame.draw.polygon(surface, (255, 255, 255), points, 2)

    def draw(self, surface):
        for crystal in self.crystals:
            self.draw_crystal(surface, crystal['x'], crystal['y'], 
                            crystal['size'], crystal['rotation'], crystal['color'])

class ParticleExplosion(ScreenSaver):
    def __init__(self):
        super().__init__("Particle Explosion", 5000)
        self.explosions = []
        self.particles = []

    def create_explosion(self):
        x = random.randint(100, SCREEN_WIDTH - 100)
        y = random.randint(100, SCREEN_HEIGHT - 100)
        color = random.choice(self.colors)
        
        for _ in range(30):
            angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(3, 10)
            velocity = (speed * math.cos(angle), speed * math.sin(angle))
            self.particles.append(Particle(x, y, color, velocity, random.uniform(2, 8)))

    def update(self):
        for particle in self.particles[:]:
            particle.update()
            if particle.life <= 0:
                self.particles.remove(particle)
        
        if len(self.particles) < 10:
            self.create_explosion()

    def draw(self, surface):
        for particle in self.particles:
            particle.draw(surface)

# Create all creative screen savers
creative_savers = [
    SpaceWarp(),
    Fireworks(),
    ButterflyGarden(),
    UnderwaterBubbles(),
    AbstractPainting(),
    DigitalRainbow(),
    MagneticField(),
    CrystalGrowth(),
    ParticleExplosion()
]

# Create variations for each creative saver
for i in range(10):  # 10 variations per creative saver = 90 more
    for base_saver in creative_savers:
        new_saver = type(f"{base_saver.__class__.__name__}Variation{i}", 
                        (base_saver.__class__,), {})()
        new_saver.name = f"{base_saver.name} Variation {i+1}"
        new_saver.duration = random.randint(3000, 10000)
        creative_savers.append(new_saver) 