import pygame
import random
import math
import time
import sys
import os
from typing import List, Tuple, Dict, Any
import colorsys
import numpy as np

# Initialize Pygame
pygame.init()

# Screen setup - Use windowed mode instead of fullscreen
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 800
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("ADHD Brain Rot Screen Savers")

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Import base classes
from base_screensaver import ScreenSaver, Particle

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

# Create all screen savers
screen_savers = [
    CosmicDance(),
    RainbowWaves(),
    ParticleExplosion(),
    GeometricHypnosis(),
    NeuralNetwork(),
    ColorfulBubbles(),
    MatrixRain(),
    SpiralGalaxy(),
    FloatingIslands(),
    EnergyField()
]

# Import all screen savers from combined file
try:
    from all_screensavers import all_screen_savers
    screen_savers.extend(all_screen_savers)
    print(f"Loaded {len(all_screen_savers)} screen savers from combined file")
except ImportError as e:
    print(f"Note: Combined screen savers not loaded: {e}")

# Add more variations
for i in range(50):  # Create 50 more variations
    base_saver = random.choice(screen_savers)
    new_saver = type(f"Variation{i}", (base_saver.__class__,), {})()
    new_saver.name = f"{base_saver.name} Variation {i+1}"
    new_saver.duration = random.randint(3000, 10000)
    screen_savers.append(new_saver)

print(f"Total screen savers loaded: {len(screen_savers)}")

# Main loop
current_saver = random.choice(screen_savers)
clock = pygame.time.Clock()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            elif event.key == pygame.K_SPACE:
                current_saver = random.choice(screen_savers)
                current_saver.start_time = time.time()
        elif event.type == pygame.MOUSEMOTION:
            # Pass mouse position to current saver for interactivity
            if hasattr(current_saver, 'mouse_pos'):
                current_saver.mouse_pos = event.pos
            # Make all screen savers interactive with mouse
            if hasattr(current_saver, 'interactive_update'):
                current_saver.interactive_update(event.pos)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # Click to trigger special effects
            if hasattr(current_saver, 'click_effect'):
                current_saver.click_effect(event.pos)

    # Check if current saver is finished
    if current_saver.is_finished():
        current_saver = random.choice(screen_savers)
        current_saver.start_time = time.time()

    # Clear screen
    screen.fill(BLACK)

    # Update and draw current saver
    current_saver.update()
    current_saver.draw(screen)

    # Display current saver name
    font = pygame.font.Font(None, 36)
    text = font.render(f"Current: {current_saver.name}", True, WHITE)
    screen.blit(text, (10, 10))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit() 