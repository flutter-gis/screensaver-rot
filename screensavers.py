import pygame
import random
import math
import colorsys
from typing import List, Tuple

# Import ScreenSaver class and screen dimensions
from base_screensaver import ScreenSaver, SCREEN_WIDTH, SCREEN_HEIGHT

class DNAHelix(ScreenSaver):
    def __init__(self):
        super().__init__("DNA Helix", 7000)
        self.strands = 2
        self.points_per_strand = 100

    def update(self):
        self.phase += 0.02

    def draw(self, surface):
        center_x, center_y = SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2
        
        for strand in range(self.strands):
            strand_offset = strand * math.pi
            for i in range(self.points_per_strand):
                t = i / self.points_per_strand * 4 * math.pi + self.phase
                x = center_x + 100 * math.cos(t + strand_offset)
                y = center_y + 50 * math.sin(t) + (i - self.points_per_strand/2) * 3
                
                hue = (i * 3.6 + self.phase * 50) % 360
                rgb = colorsys.hsv_to_rgb(hue/360, 0.8, 1.0)
                color = tuple(int(c * 255) for c in rgb)
                
                pygame.draw.circle(surface, color, (int(x), int(y)), 3)

class VortexWhirl(ScreenSaver):
    def __init__(self):
        super().__init__("Vortex Whirl", 6000)
        self.particles = []
        self.generate_particles()

    def generate_particles(self):
        for _ in range(200):
            particle = {
                'angle': random.uniform(0, 2 * math.pi),
                'radius': random.uniform(10, 400),
                'speed': random.uniform(0.01, 0.05),
                'color': random.choice(self.colors)
            }
            self.particles.append(particle)

    def update(self):
        self.phase += 0.03
        for particle in self.particles:
            particle['angle'] += particle['speed']
            particle['radius'] = max(10, particle['radius'] - 0.5)
            if particle['radius'] <= 10:
                particle['radius'] = 400

    def draw(self, surface):
        center_x, center_y = SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2
        
        for particle in self.particles:
            x = center_x + particle['radius'] * math.cos(particle['angle'])
            y = center_y + particle['radius'] * math.sin(particle['angle'])
            size = max(1, particle['radius'] / 50)
            pygame.draw.circle(surface, particle['color'], (int(x), int(y)), int(size))

class CrystalGrowth(ScreenSaver):
    def __init__(self):
        super().__init__("Crystal Growth", 8000)
        self.crystals = []
        self.generate_crystals()

    def generate_crystals(self):
        for _ in range(15):
            crystal = {
                'x': random.randint(50, SCREEN_WIDTH - 50),
                'y': random.randint(50, SCREEN_HEIGHT - 50),
                'size': random.uniform(5, 30),
                'color': random.choice(self.colors),
                'growth_rate': random.uniform(0.1, 0.5),
                'max_size': random.uniform(20, 60)
            }
            self.crystals.append(crystal)

    def update(self):
        self.phase += 0.02
        for crystal in self.crystals:
            crystal['size'] = min(crystal['max_size'], 
                                crystal['size'] + crystal['growth_rate'] * math.sin(self.phase))

    def draw(self, surface):
        for crystal in self.crystals:
            points = []
            for i in range(6):
                angle = i * math.pi / 3 + self.phase
                x = crystal['x'] + crystal['size'] * math.cos(angle)
                y = crystal['y'] + crystal['size'] * math.sin(angle)
                points.append((x, y))
            
            if len(points) >= 3:
                pygame.draw.polygon(surface, crystal['color'], points)

class PlasmaField(ScreenSaver):
    def __init__(self):
        super().__init__("Plasma Field", 7000)
        self.field_size = 50
        self.field = [[random.uniform(0, 2 * math.pi) for _ in range(self.field_size)] 
                     for _ in range(self.field_size)]

    def update(self):
        self.phase += 0.05
        for i in range(self.field_size):
            for j in range(self.field_size):
                self.field[i][j] += 0.1

    def draw(self, surface):
        cell_width = SCREEN_WIDTH / self.field_size
        cell_height = SCREEN_HEIGHT / self.field_size
        
        for i in range(self.field_size):
            for j in range(self.field_size):
                value = math.sin(self.field[i][j] + self.phase)
                hue = (value * 180 + 180) % 360
                rgb = colorsys.hsv_to_rgb(hue/360, 0.8, 1.0)
                color = tuple(int(c * 255) for c in rgb)
                
                rect = pygame.Rect(i * cell_width, j * cell_height, cell_width, cell_height)
                pygame.draw.rect(surface, color, rect)

class QuantumDots(ScreenSaver):
    def __init__(self):
        super().__init__("Quantum Dots", 6000)
        self.dots = []
        self.generate_dots()

    def generate_dots(self):
        for _ in range(100):
            dot = {
                'x': random.randint(0, SCREEN_WIDTH),
                'y': random.randint(0, SCREEN_HEIGHT),
                'size': random.uniform(2, 8),
                'color': random.choice(self.colors),
                'pulse': random.uniform(0, 2 * math.pi),
                'speed': random.uniform(0.02, 0.08)
            }
            self.dots.append(dot)

    def update(self):
        self.phase += 0.02
        for dot in self.dots:
            dot['pulse'] += dot['speed']
            dot['size'] = 2 + 6 * math.sin(dot['pulse'])

    def draw(self, surface):
        for dot in self.dots:
            pygame.draw.circle(surface, dot['color'], 
                             (int(dot['x']), int(dot['y'])), int(dot['size']))

class FractalTree(ScreenSaver):
    def __init__(self):
        super().__init__("Fractal Tree", 8000)
        self.max_depth = 8

    def draw_branch(self, surface, x, y, length, angle, depth, color):
        if depth > self.max_depth:
            return
            
        end_x = x + length * math.cos(angle)
        end_y = y + length * math.sin(angle)
        
        # Draw branch
        pygame.draw.line(surface, color, (x, y), (end_x, end_y), max(1, 5 - depth))
        
        # Draw leaves at the end
        if depth == self.max_depth:
            pygame.draw.circle(surface, color, (int(end_x), int(end_y)), 3)
        
        # Recursive branches
        if depth < self.max_depth:
            new_length = length * 0.7
            new_angle1 = angle + 0.5 + math.sin(self.phase + depth) * 0.3
            new_angle2 = angle - 0.5 + math.sin(self.phase + depth) * 0.3
            
            hue = (depth * 30 + self.phase * 50) % 360
            rgb = colorsys.hsv_to_rgb(hue/360, 0.8, 1.0)
            new_color = tuple(int(c * 255) for c in rgb)
            
            self.draw_branch(surface, end_x, end_y, new_length, new_angle1, depth + 1, new_color)
            self.draw_branch(surface, end_x, end_y, new_length, new_angle2, depth + 1, new_color)

    def update(self):
        self.phase += 0.01

    def draw(self, surface):
        start_x = SCREEN_WIDTH // 2
        start_y = SCREEN_HEIGHT - 50
        initial_length = 100
        initial_angle = -math.pi / 2
        
        hue = (self.phase * 50) % 360
        rgb = colorsys.hsv_to_rgb(hue/360, 0.8, 1.0)
        color = tuple(int(c * 255) for c in rgb)
        
        self.draw_branch(surface, start_x, start_y, initial_length, initial_angle, 0, color)

class MagneticField(ScreenSaver):
    def __init__(self):
        super().__init__("Magnetic Field", 7000)
        self.poles = []
        self.generate_poles()

    def generate_poles(self):
        for _ in range(6):
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

class SolarSystem(ScreenSaver):
    def __init__(self):
        super().__init__("Solar System", 9000)
        self.planets = []
        self.generate_planets()

    def generate_planets(self):
        for i in range(8):
            planet = {
                'distance': 50 + i * 80,
                'angle': random.uniform(0, 2 * math.pi),
                'speed': random.uniform(0.005, 0.02),
                'size': random.uniform(5, 20),
                'color': random.choice(self.colors),
                'moons': random.randint(0, 3)
            }
            self.planets.append(planet)

    def update(self):
        self.phase += 0.01
        for planet in self.planets:
            planet['angle'] += planet['speed']

    def draw(self, surface):
        center_x, center_y = SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2
        
        # Draw sun
        pygame.draw.circle(surface, (255, 255, 0), (center_x, center_y), 30)
        
        # Draw planets
        for planet in self.planets:
            x = center_x + planet['distance'] * math.cos(planet['angle'])
            y = center_y + planet['distance'] * math.sin(planet['angle'])
            
            pygame.draw.circle(surface, planet['color'], (int(x), int(y)), int(planet['size']))
            
            # Draw moons
            for i in range(planet['moons']):
                moon_angle = planet['angle'] + (i + 1) * math.pi / 2 + self.phase
                moon_x = x + 20 * math.cos(moon_angle)
                moon_y = y + 20 * math.sin(moon_angle)
                pygame.draw.circle(surface, (200, 200, 200), (int(moon_x), int(moon_y)), 2)

class LavaLamp(ScreenSaver):
    def __init__(self):
        super().__init__("Lava Lamp", 6000)
        self.blobs = []
        self.generate_blobs()

    def generate_blobs(self):
        for _ in range(10):
            blob = {
                'x': random.randint(100, SCREEN_WIDTH - 100),
                'y': random.randint(SCREEN_HEIGHT - 200, SCREEN_HEIGHT - 50),
                'size': random.uniform(20, 60),
                'color': random.choice(self.colors),
                'speed': random.uniform(0.5, 2.0),
                'direction': random.uniform(-1, 1)
            }
            self.blobs.append(blob)

    def update(self):
        self.phase += 0.02
        for blob in self.blobs:
            blob['y'] -= blob['speed']
            blob['x'] += blob['direction'] * 0.5
            
            # Reset when blob reaches top
            if blob['y'] < 50:
                blob['y'] = SCREEN_HEIGHT - 50
                blob['x'] = random.randint(100, SCREEN_WIDTH - 100)

    def draw(self, surface):
        # Draw lamp base
        lamp_rect = pygame.Rect(SCREEN_WIDTH//2 - 100, SCREEN_HEIGHT - 100, 200, 100)
        pygame.draw.rect(surface, (50, 50, 50), lamp_rect)
        
        # Draw blobs
        for blob in self.blobs:
            pygame.draw.circle(surface, blob['color'], 
                             (int(blob['x']), int(blob['y'])), int(blob['size']))

class DigitalRainbow(ScreenSaver):
    def __init__(self):
        super().__init__("Digital Rainbow", 7000)
        self.columns = SCREEN_WIDTH // 20
        self.drops = []
        self.generate_drops()

    def generate_drops(self):
        for i in range(self.columns):
            drop = {
                'x': i * 20,
                'y': random.randint(-SCREEN_HEIGHT, 0),
                'speed': random.uniform(1, 5),
                'length': random.randint(10, 30),
                'hue': random.uniform(0, 360)
            }
            self.drops.append(drop)

    def update(self):
        for drop in self.drops:
            drop['y'] += drop['speed']
            drop['hue'] = (drop['hue'] + 1) % 360
            
            if drop['y'] > SCREEN_HEIGHT + drop['length'] * 10:
                drop['y'] = random.randint(-SCREEN_HEIGHT, 0)

    def draw(self, surface):
        for drop in self.drops:
            for i in range(drop['length']):
                y = drop['y'] - i * 10
                if 0 <= y < SCREEN_HEIGHT:
                    hue = (drop['hue'] + i * 10) % 360
                    rgb = colorsys.hsv_to_rgb(hue/360, 0.8, 1.0)
                    color = tuple(int(c * 255) for c in rgb)
                    pygame.draw.circle(surface, color, (drop['x'], int(y)), 2)

# Add all the new screen savers to the main list
additional_savers = [
    DNAHelix(),
    VortexWhirl(),
    CrystalGrowth(),
    PlasmaField(),
    QuantumDots(),
    FractalTree(),
    MagneticField(),
    SolarSystem(),
    LavaLamp(),
    DigitalRainbow()
]

# Create variations for each new saver
for i in range(20):  # 20 variations per new saver = 200 more
    for base_saver in additional_savers:
        new_saver = type(f"{base_saver.__class__.__name__}Variation{i}", 
                        (base_saver.__class__,), {})()
        new_saver.name = f"{base_saver.name} Variation {i+1}"
        new_saver.duration = random.randint(3000, 10000)
        additional_savers.append(new_saver) 