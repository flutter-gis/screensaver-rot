import pygame
import random
import math
import time
import colorsys
import numpy as np
from typing import List, Tuple, Dict, Any
from base_screensaver import ScreenSaver, Particle, SCREEN_WIDTH, SCREEN_HEIGHT

# Final batch of unique screen savers
class VortexTunnel(ScreenSaver):
    def __init__(self):
        super().__init__("Vortex Tunnel", 8000)
        self.rings = []
        self.generate_rings()

    def generate_rings(self):
        for i in range(20):
            ring = {
                'radius': 50 + i * 30,
                'color': random.choice(self.colors),
                'speed': random.uniform(0.02, 0.08)
            }
            self.rings.append(ring)

    def update(self):
        self.phase += 0.03

    def draw(self, surface):
        center_x, center_y = SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2
        
        for ring in self.rings:
            # Create tunnel effect
            radius = ring['radius'] + self.phase * 50
            if radius > 0:
                pygame.draw.circle(surface, ring['color'], (center_x, center_y), int(radius), 3)

class LightningStorm(ScreenSaver):
    def __init__(self):
        super().__init__("Lightning Storm", 6000)
        self.lightning_bolts = []
        self.generate_lightning()

    def generate_lightning(self):
        for _ in range(5):
            bolt = {
                'start_x': random.randint(0, SCREEN_WIDTH),
                'start_y': 0,
                'end_x': random.randint(0, SCREEN_WIDTH),
                'end_y': SCREEN_HEIGHT,
                'color': (255, 255, 255),
                'intensity': random.uniform(0, 2 * math.pi)
            }
            self.lightning_bolts.append(bolt)

    def update(self):
        self.phase += 0.05
        for bolt in self.lightning_bolts:
            bolt['intensity'] += 0.1

    def draw_lightning(self, surface, start_x, start_y, end_x, end_y, intensity):
        if math.sin(intensity) > 0.5:
            points = [(start_x, start_y)]
            current_x, current_y = start_x, start_y
            
            while current_y < end_y:
                current_x += random.randint(-50, 50)
                current_y += random.randint(20, 40)
                points.append((current_x, current_y))
            
            points.append((end_x, end_y))
            
            if len(points) > 1:
                pygame.draw.lines(surface, (255, 255, 255), False, points, 3)

    def draw(self, surface):
        surface.fill((0, 0, 50))  # Dark blue background
        
        for bolt in self.lightning_bolts:
            self.draw_lightning(surface, bolt['start_x'], bolt['start_y'],
                              bolt['end_x'], bolt['end_y'], bolt['intensity'])

class GalaxyCollision(ScreenSaver):
    def __init__(self):
        super().__init__("Galaxy Collision", 10000)
        self.galaxy1 = []
        self.galaxy2 = []
        self.generate_galaxies()

    def generate_galaxies(self):
        # First galaxy
        center1_x, center1_y = SCREEN_WIDTH // 3, SCREEN_HEIGHT // 2
        for _ in range(100):
            angle = random.uniform(0, 2 * math.pi)
            radius = random.uniform(20, 150)
            self.galaxy1.append({
                'x': center1_x + radius * math.cos(angle),
                'y': center1_y + radius * math.sin(angle),
                'vx': -radius * math.sin(angle) * 0.5,
                'vy': radius * math.cos(angle) * 0.5,
                'color': (255, 100, 100)
            })
        
        # Second galaxy
        center2_x, center2_y = 2 * SCREEN_WIDTH // 3, SCREEN_HEIGHT // 2
        for _ in range(100):
            angle = random.uniform(0, 2 * math.pi)
            radius = random.uniform(20, 150)
            self.galaxy2.append({
                'x': center2_x + radius * math.cos(angle),
                'y': center2_y + radius * math.sin(angle),
                'vx': -radius * math.sin(angle) * 0.5,
                'vy': radius * math.cos(angle) * 0.5,
                'color': (100, 100, 255)
            })

    def update(self):
        self.phase += 0.01
        
        # Update galaxy 1
        for star in self.galaxy1:
            star['x'] += star['vx']
            star['y'] += star['vy']
        
        # Update galaxy 2
        for star in self.galaxy2:
            star['x'] += star['vx']
            star['y'] += star['vy']

    def draw(self, surface):
        # Draw all stars
        for star in self.galaxy1 + self.galaxy2:
            if 0 <= star['x'] < SCREEN_WIDTH and 0 <= star['y'] < SCREEN_HEIGHT:
                pygame.draw.circle(surface, star['color'], 
                                 (int(star['x']), int(star['y'])), 2)

class DNAReplication(ScreenSaver):
    def __init__(self):
        super().__init__("DNA Replication", 8000)
        self.strands = []
        self.generate_strands()

    def generate_strands(self):
        for i in range(4):  # 4 strands
            strand = {
                'points': [],
                'color': random.choice(self.colors),
                'offset': i * math.pi / 2,
                'replicating': False
            }
            for j in range(50):
                strand['points'].append({
                    'angle': j * 0.2,
                    'radius': 30 + 10 * math.sin(j * 0.3)
                })
            self.strands.append(strand)

    def update(self):
        self.phase += 0.02
        if self.phase > 4:  # Start replication
            for strand in self.strands:
                strand['replicating'] = True

    def draw(self, surface):
        center_x, center_y = SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2
        
        for strand in self.strands:
            points = []
            for point in strand['points']:
                x = center_x + point['radius'] * math.cos(point['angle'] + strand['offset'] + self.phase)
                y = center_y + (point['angle'] - 5) * 8
                points.append((x, y))
            
            if len(points) > 1:
                pygame.draw.lines(surface, strand['color'], False, points, 3)
                
                # Draw replicating strand
                if strand['replicating']:
                    offset_points = [(x + 20, y) for x, y in points]
                    pygame.draw.lines(surface, strand['color'], False, offset_points, 2)

class QuantumTunneling(ScreenSaver):
    def __init__(self):
        super().__init__("Quantum Tunneling", 7000)
        self.particles = []
        self.barriers = []
        self.generate_quantum_system()

    def generate_quantum_system(self):
        # Create barriers
        for i in range(3):
            barrier = {
                'x': (i + 1) * SCREEN_WIDTH // 4,
                'width': 20,
                'height': SCREEN_HEIGHT,
                'transparency': random.uniform(0.3, 0.7)
            }
            self.barriers.append(barrier)
        
        # Create quantum particles
        for _ in range(20):
            particle = {
                'x': random.randint(0, SCREEN_WIDTH),
                'y': random.randint(0, SCREEN_HEIGHT),
                'vx': random.uniform(1, 3),
                'color': random.choice(self.colors),
                'size': random.uniform(3, 8),
                'tunneling': False
            }
            self.particles.append(particle)

    def update(self):
        self.phase += 0.02
        
        for particle in self.particles:
            particle['x'] += particle['vx']
            
            # Check for tunneling through barriers
            for barrier in self.barriers:
                if (barrier['x'] - barrier['width']/2 < particle['x'] < 
                    barrier['x'] + barrier['width']/2):
                    if random.random() < barrier['transparency']:
                        particle['tunneling'] = True
                    else:
                        particle['vx'] *= -1  # Bounce back
            
            # Reset position if off screen
            if particle['x'] > SCREEN_WIDTH:
                particle['x'] = 0
                particle['tunneling'] = False

    def draw(self, surface):
        # Draw barriers
        for barrier in self.barriers:
            alpha = int(255 * barrier['transparency'])
            barrier_color = (100, 100, 100, alpha)
            rect = pygame.Rect(barrier['x'] - barrier['width']/2, 0, 
                             barrier['width'], barrier['height'])
            pygame.draw.rect(surface, barrier_color, rect)
        
        # Draw particles
        for particle in self.particles:
            color = particle['color']
            if particle['tunneling']:
                color = (255, 255, 0)  # Yellow when tunneling
            pygame.draw.circle(surface, color, 
                             (int(particle['x']), int(particle['y'])), int(particle['size']))

class NeuralEvolution(ScreenSaver):
    def __init__(self):
        super().__init__("Neural Evolution", 9000)
        self.networks = []
        self.generate_networks()

    def generate_networks(self):
        for _ in range(5):
            network = {
                'nodes': [],
                'connections': [],
                'fitness': random.uniform(0, 1),
                'color': random.choice(self.colors)
            }
            
            # Create nodes
            for i in range(10):
                node = {
                    'x': random.randint(50, SCREEN_WIDTH - 50),
                    'y': random.randint(50, SCREEN_HEIGHT - 50),
                    'activation': random.uniform(0, 2 * math.pi)
                }
                network['nodes'].append(node)
            
            # Create connections
            for i in range(len(network['nodes'])):
                for j in range(i + 1, len(network['nodes'])):
                    if random.random() < 0.3:
                        network['connections'].append((i, j))
            
            self.networks.append(network)

    def update(self):
        self.phase += 0.02
        
        # Evolve networks
        for network in self.networks:
            network['fitness'] += random.uniform(-0.01, 0.01)
            network['fitness'] = max(0, min(1, network['fitness']))
            
            for node in network['nodes']:
                node['activation'] += 0.1

    def draw(self, surface):
        for network in self.networks:
            # Draw connections
            for i, j in network['connections']:
                node1 = network['nodes'][i]
                node2 = network['nodes'][j]
                strength = math.sin(node1['activation'] + node2['activation'])
                if strength > 0:
                    pygame.draw.line(surface, network['color'], 
                                   (node1['x'], node1['y']), 
                                   (node2['x'], node2['y']), 2)
            
            # Draw nodes
            for node in network['nodes']:
                size = 3 + 5 * network['fitness']
                pygame.draw.circle(surface, network['color'], 
                                 (int(node['x']), int(node['y'])), int(size))

class CrystalCave3D(ScreenSaver):
    def __init__(self):
        super().__init__("3D Crystal Cave", 10000)
        self.crystals_3d = []
        self.generate_3d_crystals()

    def generate_3d_crystals(self):
        for _ in range(15):
            crystal = {
                'x': random.uniform(-100, 100),
                'y': random.uniform(-100, 100),
                'z': random.uniform(50, 200),
                'size': random.uniform(10, 40),
                'color': random.choice(self.colors),
                'rotation': random.uniform(0, 2 * math.pi)
            }
            self.crystals_3d.append(crystal)

    def update(self):
        self.phase += 0.01
        for crystal in self.crystals_3d:
            crystal['rotation'] += 0.02

    def draw_crystal_3d(self, surface, x, y, z, size, rotation, color):
        # 3D to 2D projection
        scale = 200 / (200 + z)
        screen_x = SCREEN_WIDTH // 2 + x * scale
        screen_y = SCREEN_HEIGHT // 2 + y * scale
        screen_size = size * scale
        
        # Draw 3D crystal
        points = []
        for i in range(6):
            angle = rotation + i * math.pi / 3
            px = screen_x + screen_size * math.cos(angle)
            py = screen_y + screen_size * math.sin(angle)
            points.append((px, py))
        
        if len(points) >= 3:
            pygame.draw.polygon(surface, color, points)
            pygame.draw.polygon(surface, (255, 255, 255), points, 2)

    def draw(self, surface):
        # Sort crystals by Z for proper depth
        sorted_crystals = sorted(self.crystals_3d, key=lambda c: c['z'], reverse=True)
        
        for crystal in sorted_crystals:
            self.draw_crystal_3d(surface, crystal['x'], crystal['y'], crystal['z'],
                                crystal['size'], crystal['rotation'], crystal['color'])

class ParticleAccelerator(ScreenSaver):
    def __init__(self):
        super().__init__("Particle Accelerator", 8000)
        self.particles = []
        self.rings = []
        self.generate_accelerator()

    def generate_accelerator(self):
        # Create accelerator rings
        for i in range(5):
            ring = {
                'radius': 100 + i * 80,
                'color': random.choice(self.colors),
                'speed': random.uniform(0.02, 0.08)
            }
            self.rings.append(ring)
        
        # Create particles
        for _ in range(30):
            particle = {
                'angle': random.uniform(0, 2 * math.pi),
                'radius': random.uniform(50, 300),
                'speed': random.uniform(0.01, 0.05),
                'color': random.choice(self.colors),
                'size': random.uniform(2, 6)
            }
            self.particles.append(particle)

    def update(self):
        self.phase += 0.02
        
        for ring in self.rings:
            ring['speed'] += 0.001  # Accelerate
        
        for particle in self.particles:
            particle['angle'] += particle['speed']
            particle['speed'] += 0.001  # Accelerate particles

    def draw(self, surface):
        center_x, center_y = SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2
        
        # Draw accelerator rings
        for ring in self.rings:
            pygame.draw.circle(surface, ring['color'], (center_x, center_y), 
                             int(ring['radius']), 2)
        
        # Draw particles
        for particle in self.particles:
            x = center_x + particle['radius'] * math.cos(particle['angle'])
            y = center_y + particle['radius'] * math.sin(particle['angle'])
            pygame.draw.circle(surface, particle['color'], (int(x), int(y)), int(particle['size']))

# Create all final screen savers
final_savers = [
    VortexTunnel(),
    LightningStorm(),
    GalaxyCollision(),
    DNAReplication(),
    QuantumTunneling(),
    NeuralEvolution(),
    CrystalCave3D(),
    ParticleAccelerator()
]

# Create variations for each final saver
for i in range(10):  # 10 variations per final saver = 80 more
    for base_saver in final_savers:
        new_saver = type(f"{base_saver.__class__.__name__}Variation{i}", 
                        (base_saver.__class__,), {})()
        new_saver.name = f"{base_saver.name} Variation {i+1}"
        new_saver.duration = random.randint(3000, 10000)
        final_savers.append(new_saver) 