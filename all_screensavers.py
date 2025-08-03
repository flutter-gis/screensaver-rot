import pygame
import random
import math
import time
import colorsys
import numpy as np
from typing import List, Tuple, Dict, Any

# Screen dimensions
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 800

# Import additional libraries for advanced effects
try:
    import cv2
    CV2_AVAILABLE = True
except ImportError:
    CV2_AVAILABLE = False

try:
    import matplotlib.pyplot as plt
    import matplotlib.animation as animation
    MATPLOTLIB_AVAILABLE = True
except ImportError:
    MATPLOTLIB_AVAILABLE = False

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
            color = tuple(max(0, min(255, int(c * 255))) for c in rgb)
            self.colors.append(color)
        return self.colors

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

# ===== BASIC SCREEN SAVERS =====

class CosmicDance(ScreenSaver):
    def __init__(self):
        super().__init__("Cosmic Dance", 8000)
        self.orbits = []
        for i in range(15):
            self.orbits.append({
                'angle': random.uniform(0, 2 * math.pi),
                'radius': random.uniform(50, 300),
                'speed': random.uniform(0.02, 0.08),
                'color': random.choice(self.colors),
                'size': random.uniform(5, 20)
            })

    def update(self):
        self.phase += 0.02
        for orbit in self.orbits:
            orbit['angle'] += orbit['speed']

    def draw(self, surface):
        center_x, center_y = SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2
        
        # Draw cosmic background
        for i in range(100):
            x = random.randint(0, SCREEN_WIDTH)
            y = random.randint(0, SCREEN_HEIGHT)
            brightness = int(50 + 100 * math.sin(self.phase + i * 0.1))
            color = (brightness, brightness, brightness + 50)
            # Ensure color values are within valid range
            color = tuple(max(0, min(255, c)) for c in color)
            pygame.draw.circle(surface, color, (x, y), 1)

        # Draw orbiting objects
        for orbit in self.orbits:
            x = center_x + orbit['radius'] * math.cos(orbit['angle'])
            y = center_y + orbit['radius'] * math.sin(orbit['angle'])
            pygame.draw.circle(surface, orbit['color'], (int(x), int(y)), int(orbit['size']))

class RainbowWaves(ScreenSaver):
    def __init__(self):
        super().__init__("Rainbow Waves", 6000)
        self.waves = []
        for i in range(8):
            self.waves.append({
                'amplitude': random.uniform(50, 200),
                'frequency': random.uniform(0.01, 0.03),
                'phase': random.uniform(0, 2 * math.pi),
                'color': random.choice(self.colors),
                'thickness': random.randint(3, 8)
            })

    def update(self):
        self.phase += 0.03

    def draw(self, surface):
        for wave in self.waves:
            points = []
            for x in range(0, SCREEN_WIDTH, 5):
                y = SCREEN_HEIGHT // 2 + wave['amplitude'] * math.sin(
                    wave['frequency'] * x + wave['phase'] + self.phase
                )
                points.append((x, y))
            
            if len(points) > 1:
                pygame.draw.lines(surface, wave['color'], False, points, wave['thickness'])

class ParticleExplosion(ScreenSaver):
    def __init__(self):
        super().__init__("Particle Explosion", 4000)
        self.explosions = []
        self.create_explosion()

    def create_explosion(self):
        x = random.randint(100, SCREEN_WIDTH - 100)
        y = random.randint(100, SCREEN_HEIGHT - 100)
        for _ in range(50):
            angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(2, 8)
            velocity = (speed * math.cos(angle), speed * math.sin(angle))
            color = random.choice(self.colors)
            self.particles.append(Particle(x, y, color, velocity, random.uniform(3, 8)))

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

class GeometricHypnosis(ScreenSaver):
    def __init__(self):
        super().__init__("Geometric Hypnosis", 7000)
        self.shapes = []
        self.generate_shapes()

    def generate_shapes(self):
        self.shapes = []
        for i in range(12):
            shape = {
                'type': random.choice(['circle', 'triangle', 'square', 'pentagon']),
                'x': random.randint(100, SCREEN_WIDTH - 100),
                'y': random.randint(100, SCREEN_HEIGHT - 100),
                'size': random.uniform(20, 80),
                'color': random.choice(self.colors),
                'rotation': random.uniform(0, 2 * math.pi),
                'rotation_speed': random.uniform(-0.05, 0.05)
            }
            self.shapes.append(shape)

    def update(self):
        self.phase += 0.02
        for shape in self.shapes:
            shape['rotation'] += shape['rotation_speed']
            shape['size'] = 20 + 60 * math.sin(self.phase + shape['rotation'])

    def draw(self, surface):
        for shape in self.shapes:
            if shape['type'] == 'circle':
                pygame.draw.circle(surface, shape['color'], 
                                 (int(shape['x']), int(shape['y'])), int(shape['size']))
            elif shape['type'] == 'square':
                rect = pygame.Rect(shape['x'] - shape['size'], shape['y'] - shape['size'],
                                 shape['size'] * 2, shape['size'] * 2)
                pygame.draw.rect(surface, shape['color'], rect)

class NeuralNetwork(ScreenSaver):
    def __init__(self):
        super().__init__("Neural Network", 9000)
        self.nodes = []
        self.connections = []
        self.generate_network()

    def generate_network(self):
        # Create nodes
        for i in range(20):
            node = {
                'x': random.randint(50, SCREEN_WIDTH - 50),
                'y': random.randint(50, SCREEN_HEIGHT - 50),
                'color': random.choice(self.colors),
                'size': random.uniform(5, 15),
                'pulse': random.uniform(0, 2 * math.pi)
            }
            self.nodes.append(node)

        # Create connections
        for i in range(len(self.nodes)):
            for j in range(i + 1, len(self.nodes)):
                if random.random() < 0.3:  # 30% chance of connection
                    self.connections.append((i, j))

    def update(self):
        self.phase += 0.03
        for node in self.nodes:
            node['pulse'] += 0.1
            node['size'] = 5 + 10 * math.sin(node['pulse'])

    def draw(self, surface):
        # Draw connections
        for i, j in self.connections:
            node1 = self.nodes[i]
            node2 = self.nodes[j]
            alpha = int(100 + 100 * math.sin(self.phase + i + j))
            color = (*node1['color'][:3], alpha)
            pygame.draw.line(surface, color, 
                           (node1['x'], node1['y']), (node2['x'], node2['y']), 2)

        # Draw nodes
        for node in self.nodes:
            pygame.draw.circle(surface, node['color'], 
                             (int(node['x']), int(node['y'])), int(node['size']))

class ColorfulBubbles(ScreenSaver):
    def __init__(self):
        super().__init__("Colorful Bubbles", 5000)
        self.bubbles = []
        self.generate_bubbles()

    def generate_bubbles(self):
        for _ in range(30):
            bubble = {
                'x': random.randint(50, SCREEN_WIDTH - 50),
                'y': random.randint(50, SCREEN_HEIGHT - 50),
                'radius': random.uniform(10, 50),
                'color': random.choice(self.colors),
                'speed': random.uniform(0.5, 2),
                'direction': random.uniform(0, 2 * math.pi)
            }
            self.bubbles.append(bubble)

    def update(self):
        self.phase += 0.02
        for bubble in self.bubbles:
            bubble['x'] += bubble['speed'] * math.cos(bubble['direction'])
            bubble['y'] += bubble['speed'] * math.sin(bubble['direction'])
            bubble['radius'] = 10 + 40 * math.sin(self.phase + bubble['x'] * 0.01)

            # Bounce off walls
            if bubble['x'] < bubble['radius'] or bubble['x'] > SCREEN_WIDTH - bubble['radius']:
                bubble['direction'] = math.pi - bubble['direction']
            if bubble['y'] < bubble['radius'] or bubble['y'] > SCREEN_HEIGHT - bubble['radius']:
                bubble['direction'] = -bubble['direction']

    def draw(self, surface):
        for bubble in self.bubbles:
            pygame.draw.circle(surface, bubble['color'], 
                             (int(bubble['x']), int(bubble['y'])), int(bubble['radius']))

class MatrixRain(ScreenSaver):
    def __init__(self):
        super().__init__("Matrix Rain", 6000)
        self.drops = []
        self.generate_drops()

    def generate_drops(self):
        for i in range(SCREEN_WIDTH // 20):
            drop = {
                'x': i * 20,
                'y': random.randint(-SCREEN_HEIGHT, 0),
                'speed': random.uniform(2, 8),
                'length': random.randint(5, 20),
                'color': random.choice(self.colors)
            }
            self.drops.append(drop)

    def update(self):
        for drop in self.drops:
            drop['y'] += drop['speed']
            if drop['y'] > SCREEN_HEIGHT + drop['length'] * 10:
                drop['y'] = random.randint(-SCREEN_HEIGHT, 0)

    def draw(self, surface):
        for drop in self.drops:
            for i in range(drop['length']):
                y = drop['y'] - i * 10
                if 0 <= y < SCREEN_HEIGHT:
                    alpha = 255 - (i * 255 // drop['length'])
                    color = (*drop['color'][:3], alpha)
                    pygame.draw.circle(surface, color, (drop['x'], int(y)), 2)

class SpiralGalaxy(ScreenSaver):
    def __init__(self):
        super().__init__("Spiral Galaxy", 8000)
        self.arms = 4
        self.particles_per_arm = 50

    def update(self):
        self.phase += 0.01

    def draw(self, surface):
        center_x, center_y = SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2
        
        for arm in range(self.arms):
            arm_angle = (2 * math.pi * arm) / self.arms
            for i in range(self.particles_per_arm):
                angle = arm_angle + (i * 0.1) + self.phase
                radius = 50 + i * 8
                x = center_x + radius * math.cos(angle)
                y = center_y + radius * math.sin(angle)
                
                # Color based on distance from center
                distance = math.sqrt((x - center_x)**2 + (y - center_y)**2)
                hue = (distance * 0.5 + self.phase * 50) % 360
                rgb = colorsys.hsv_to_rgb(hue/360, 0.8, 1.0)
                color = tuple(int(c * 255) for c in rgb)
                
                size = max(1, 5 - distance / 100)
                pygame.draw.circle(surface, color, (int(x), int(y)), int(size))

class FloatingIslands(ScreenSaver):
    def __init__(self):
        super().__init__("Floating Islands", 7000)
        self.islands = []
        self.generate_islands()

    def generate_islands(self):
        for _ in range(8):
            island = {
                'x': random.randint(100, SCREEN_WIDTH - 100),
                'y': random.randint(100, SCREEN_HEIGHT - 100),
                'size': random.uniform(30, 80),
                'color': random.choice(self.colors),
                'float_offset': random.uniform(0, 2 * math.pi),
                'rotation': random.uniform(0, 2 * math.pi),
                'rotation_speed': random.uniform(-0.02, 0.02)
            }
            self.islands.append(island)

    def update(self):
        self.phase += 0.02
        for island in self.islands:
            island['rotation'] += island['rotation_speed']
            island['y'] += 2 * math.sin(self.phase + island['float_offset'])

    def draw(self, surface):
        for island in self.islands:
            # Draw island base
            pygame.draw.circle(surface, island['color'], 
                             (int(island['x']), int(island['y'])), int(island['size']))
            
            # Draw floating particles around island
            for i in range(10):
                angle = (i * 36 + island['rotation'] * 180 / math.pi) * math.pi / 180
                radius = island['size'] + 20
                x = island['x'] + radius * math.cos(angle)
                y = island['y'] + radius * math.sin(angle)
                particle_color = random.choice(self.colors)
                pygame.draw.circle(surface, particle_color, (int(x), int(y)), 3)

class EnergyField(ScreenSaver):
    def __init__(self):
        super().__init__("Energy Field", 6000)
        self.field_points = []
        self.generate_field()

    def generate_field(self):
        for x in range(0, SCREEN_WIDTH, 40):
            for y in range(0, SCREEN_HEIGHT, 40):
                self.field_points.append({
                    'x': x,
                    'y': y,
                    'energy': random.uniform(0, 2 * math.pi),
                    'color': random.choice(self.colors)
                })

    def update(self):
        self.phase += 0.05
        for point in self.field_points:
            point['energy'] += 0.1

    def draw(self, surface):
        for point in self.field_points:
            energy = math.sin(point['energy'] + self.phase)
            size = max(1, 5 * energy)
            color = point['color']
            pygame.draw.circle(surface, color, (point['x'], point['y']), int(size))

# ===== 3D SCREEN SAVERS =====

class CubeField(ScreenSaver):
    def __init__(self):
        super().__init__("Cube Field", 6000)
        self.cubes = []
        self.generate_cubes()

    def generate_cubes(self):
        for _ in range(20):
            cube = {
                'x': random.randint(100, SCREEN_WIDTH - 100),
                'y': random.randint(100, SCREEN_HEIGHT - 100),
                'size': random.uniform(20, 60),
                'color': random.choice(self.colors),
                'rotation_x': random.uniform(0, 2 * math.pi),
                'rotation_y': random.uniform(0, 2 * math.pi),
                'rotation_z': random.uniform(0, 2 * math.pi),
                'speed_x': random.uniform(-0.05, 0.05),
                'speed_y': random.uniform(-0.05, 0.05),
                'speed_z': random.uniform(-0.05, 0.05)
            }
            self.cubes.append(cube)

    def update(self):
        self.phase += 0.02
        for cube in self.cubes:
            cube['rotation_x'] += cube['speed_x']
            cube['rotation_y'] += cube['speed_y']
            cube['rotation_z'] += cube['speed_z']

    def draw_cube_3d(self, surface, x, y, size, rot_x, rot_y, rot_z, color):
        # 3D cube vertices
        vertices = [
            [-size, -size, -size],
            [size, -size, -size],
            [size, size, -size],
            [-size, size, -size],
            [-size, -size, size],
            [size, -size, size],
            [size, size, size],
            [-size, size, size]
        ]
        
        # Apply rotations
        rotated_vertices = []
        for vertex in vertices:
            # Rotate around X axis
            y_rot = vertex[1] * math.cos(rot_x) - vertex[2] * math.sin(rot_x)
            z_rot = vertex[1] * math.sin(rot_x) + vertex[2] * math.cos(rot_x)
            
            # Rotate around Y axis
            x_rot = vertex[0] * math.cos(rot_y) + z_rot * math.sin(rot_y)
            z_rot = -vertex[0] * math.sin(rot_y) + z_rot * math.cos(rot_y)
            
            # Rotate around Z axis
            x_final = x_rot * math.cos(rot_z) - y_rot * math.sin(rot_z)
            y_final = x_rot * math.sin(rot_z) + y_rot * math.cos(rot_z)
            
            rotated_vertices.append([x_final, y_final, z_rot])
        
        # Project to 2D
        points_2d = []
        for vertex in rotated_vertices:
            # Simple perspective projection
            scale = 200 / (200 + vertex[2])
            px = x + vertex[0] * scale
            py = y + vertex[1] * scale
            points_2d.append((px, py))
        
        # Draw cube edges
        edges = [
            (0, 1), (1, 2), (2, 3), (3, 0),  # Bottom face
            (4, 5), (5, 6), (6, 7), (7, 4),  # Top face
            (0, 4), (1, 5), (2, 6), (3, 7)   # Connecting edges
        ]
        
        for edge in edges:
            start = points_2d[edge[0]]
            end = points_2d[edge[1]]
            pygame.draw.line(surface, color, start, end, 2)

    def draw(self, surface):
        for cube in self.cubes:
            self.draw_cube_3d(surface, cube['x'], cube['y'], cube['size'],
                             cube['rotation_x'], cube['rotation_y'], cube['rotation_z'],
                             cube['color'])

class ParticleSystem3D(ScreenSaver):
    def __init__(self):
        super().__init__("3D Particle System", 8000)
        self.particles_3d = []
        self.generate_particles()

    def generate_particles(self):
        for _ in range(100):
            particle = {
                'x': random.uniform(-200, 200),
                'y': random.uniform(-200, 200),
                'z': random.uniform(-200, 200),
                'vx': random.uniform(-2, 2),
                'vy': random.uniform(-2, 2),
                'vz': random.uniform(-2, 2),
                'color': random.choice(self.colors),
                'size': random.uniform(2, 8)
            }
            self.particles_3d.append(particle)

    def update(self):
        self.phase += 0.02
        for particle in self.particles_3d:
            particle['x'] += particle['vx']
            particle['y'] += particle['vy']
            particle['z'] += particle['vz']
            
            # Bounce off boundaries
            if abs(particle['x']) > 200:
                particle['vx'] *= -1
            if abs(particle['y']) > 200:
                particle['vy'] *= -1
            if abs(particle['z']) > 200:
                particle['vz'] *= -1

    def draw(self, surface):
        center_x, center_y = SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2
        
        # Sort particles by Z for proper depth ordering
        sorted_particles = sorted(self.particles_3d, key=lambda p: p['z'], reverse=True)
        
        for particle in sorted_particles:
            # 3D to 2D projection
            scale = 300 / (300 + particle['z'])
            x = center_x + particle['x'] * scale
            y = center_y + particle['y'] * scale
            size = particle['size'] * scale
            
            if 0 <= x < SCREEN_WIDTH and 0 <= y < SCREEN_HEIGHT:
                pygame.draw.circle(surface, particle['color'], (int(x), int(y)), int(size))

# ===== SCIENTIFIC SCREEN SAVERS =====

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

class FractalMandelbrot(ScreenSaver):
    def __init__(self):
        super().__init__("Mandelbrot Fractal", 10000)
        self.zoom = 1.0
        self.center_x = -0.5
        self.center_y = 0.0
        self.max_iter = 50

    def mandelbrot(self, x, y):
        c = complex(x, y)
        z = 0
        for i in range(self.max_iter):
            z = z * z + c
            if abs(z) > 2:
                return i
        return self.max_iter

    def update(self):
        self.phase += 0.01
        self.zoom = 1.0 + 0.5 * math.sin(self.phase)

    def draw(self, surface):
        width, height = SCREEN_WIDTH, SCREEN_HEIGHT
        
        for x in range(0, width, 4):
            for y in range(0, height, 4):
                # Map screen coordinates to complex plane
                real = (x - width/2) / (width/4 * self.zoom) + self.center_x
                imag = (y - height/2) / (height/4 * self.zoom) + self.center_y
                
                # Calculate Mandelbrot
                iterations = self.mandelbrot(real, imag)
                
                if iterations < self.max_iter:
                    # Color based on iterations
                    hue = (iterations * 10 + self.phase * 50) % 360
                    rgb = colorsys.hsv_to_rgb(hue/360, 0.8, 1.0)
                    color = tuple(int(c * 255) for c in rgb)
                    pygame.draw.circle(surface, color, (x, y), 2)

class QuantumEntanglement(ScreenSaver):
    def __init__(self):
        super().__init__("Quantum Entanglement", 9000)
        self.pairs = []
        self.generate_pairs()

    def generate_pairs(self):
        for _ in range(15):
            pair = {
                'x1': random.randint(50, SCREEN_WIDTH - 50),
                'y1': random.randint(50, SCREEN_HEIGHT - 50),
                'x2': random.randint(50, SCREEN_WIDTH - 50),
                'y2': random.randint(50, SCREEN_HEIGHT - 50),
                'color': random.choice(self.colors),
                'phase': random.uniform(0, 2 * math.pi),
                'size': random.uniform(5, 15)
            }
            self.pairs.append(pair)

    def update(self):
        self.phase += 0.02
        for pair in self.pairs:
            pair['phase'] += 0.05

    def draw(self, surface):
        for pair in self.pairs:
            # Draw entangled particles
            size1 = pair['size'] * (math.sin(pair['phase']) * 0.5 + 0.5)
            size2 = pair['size'] * (math.sin(pair['phase'] + math.pi) * 0.5 + 0.5)
            
            pygame.draw.circle(surface, pair['color'], 
                             (int(pair['x1']), int(pair['y1'])), int(size1))
            pygame.draw.circle(surface, pair['color'], 
                             (int(pair['x2']), int(pair['y2'])), int(size2))
            
            # Draw entanglement line
            pygame.draw.line(surface, pair['color'], 
                           (pair['x1'], pair['y1']), (pair['x2'], pair['y2']), 2)

# ===== CREATIVE SCREEN SAVERS =====

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

# ===== INTERACTIVE SCREEN SAVERS =====

class ConwayGameOfLife(ScreenSaver):
    def __init__(self):
        super().__init__("Game of Life", 10000)
        self.grid_size = 50
        self.grid = np.zeros((self.grid_size, self.grid_size), dtype=int)
        self.generate_initial_state()

    def generate_initial_state(self):
        for i in range(self.grid_size):
            for j in range(self.grid_size):
                if random.random() < 0.3:
                    self.grid[i][j] = 1

    def count_neighbors(self, i, j):
        count = 0
        for di in [-1, 0, 1]:
            for dj in [-1, 0, 1]:
                ni, nj = i + di, j + dj
                if (0 <= ni < self.grid_size and 0 <= nj < self.grid_size and 
                    not (di == 0 and dj == 0)):
                    count += self.grid[ni][nj]
        return count

    def update(self):
        self.phase += 0.01
        new_grid = np.zeros_like(self.grid)
        
        for i in range(self.grid_size):
            for j in range(self.grid_size):
                neighbors = self.count_neighbors(i, j)
                if self.grid[i][j] == 1:
                    if neighbors in [2, 3]:
                        new_grid[i][j] = 1
                else:
                    if neighbors == 3:
                        new_grid[i][j] = 1
        
        self.grid = new_grid

    def draw(self, surface):
        cell_width = SCREEN_WIDTH / self.grid_size
        cell_height = SCREEN_HEIGHT / self.grid_size
        
        for i in range(self.grid_size):
            for j in range(self.grid_size):
                if self.grid[i][j] == 1:
                    x = j * cell_width
                    y = i * cell_height
                    hue = (i * 7.2 + j * 7.2 + self.phase * 50) % 360
                    rgb = colorsys.hsv_to_rgb(hue/360, 0.8, 1.0)
                    color = tuple(int(c * 255) for c in rgb)
                    rect = pygame.Rect(x, y, cell_width, cell_height)
                    pygame.draw.rect(surface, color, rect)

class PlasmaEffect(ScreenSaver):
    def __init__(self):
        super().__init__("Plasma Effect", 6000)
        self.plasma = np.zeros((SCREEN_HEIGHT, SCREEN_WIDTH))

    def update(self):
        self.phase += 0.05
        for y in range(SCREEN_HEIGHT):
            for x in range(SCREEN_WIDTH):
                # Create plasma effect
                value = (math.sin(x * 0.01 + self.phase) + 
                        math.sin(y * 0.01 + self.phase) +
                        math.sin((x + y) * 0.01 + self.phase) +
                        math.sin(math.sqrt(x*x + y*y) * 0.01 + self.phase)) / 4
                self.plasma[y][x] = value

    def draw(self, surface):
        for y in range(0, SCREEN_HEIGHT, 2):
            for x in range(0, SCREEN_WIDTH, 2):
                value = self.plasma[y][x]
                hue = (value * 180 + 180 + self.phase * 50) % 360
                rgb = colorsys.hsv_to_rgb(hue/360, 0.8, 1.0)
                color = tuple(int(c * 255) for c in rgb)
                pygame.draw.circle(surface, color, (x, y), 1)

# ===== CREATE ALL SCREEN SAVERS =====

# Create all base screen savers
all_screen_savers = [
    # Basic screen savers
    CosmicDance(),
    RainbowWaves(),
    ParticleExplosion(),
    GeometricHypnosis(),
    NeuralNetwork(),
    ColorfulBubbles(),
    MatrixRain(),
    SpiralGalaxy(),
    FloatingIslands(),
    EnergyField(),
    
    # 3D screen savers
    CubeField(),
    ParticleSystem3D(),
    
    # Scientific screen savers
    DNAHelix(),
    FractalMandelbrot(),
    QuantumEntanglement(),
    
    # Creative screen savers
    SpaceWarp(),
    Fireworks(),
    ButterflyGarden(),
    
    # Interactive screen savers
    ConwayGameOfLife(),
    PlasmaEffect()
]

# Create unique variations for each screen saver
for i in range(5):  # 5 variations per screen saver
    for base_saver in all_screen_savers[:]:  # Use slice to avoid infinite loop
        # Create a unique variation with different parameters
        variation = type(f"{base_saver.__class__.__name__}Variation{i}", 
                        (base_saver.__class__,), {})()
        variation.name = f"{base_saver.name} Variation {i+1}"
        variation.duration = random.randint(3000, 10000)
        
        # Ensure colors are properly initialized
        variation.colors = variation.generate_colors()
        
        all_screen_savers.append(variation)

print(f"Total screen savers created: {len(all_screen_savers)}")