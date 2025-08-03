import pygame
import random
import math
import time
import colorsys
import numpy as np
from typing import List, Tuple, Dict, Any
from base_screensaver import ScreenSaver, Particle, SCREEN_WIDTH, SCREEN_HEIGHT

# Advanced library-based screen savers
class OpenCVWebcam(ScreenSaver):
    def __init__(self):
        super().__init__("Webcam Effects", 5000)
        self.cap = None
        if CV2_AVAILABLE:
            try:
                self.cap = cv2.VideoCapture(0)
            except:
                pass

    def update(self):
        self.phase += 0.02

    def draw(self, surface):
        if self.cap and self.cap.isOpened():
            ret, frame = self.cap.read()
            if ret:
                # Convert BGR to RGB
                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                
                # Apply effects
                if self.phase % 2 < 1:
                    # Edge detection
                    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                    edges = cv2.Canny(gray, 100, 200)
                    frame_rgb = cv2.cvtColor(edges, cv2.COLOR_GRAY2RGB)
                else:
                    # Color shift
                    frame_rgb = cv2.applyColorMap(frame_rgb, cv2.COLORMAP_RAINBOW)
                
                # Resize to screen
                frame_resized = cv2.resize(frame_rgb, (SCREEN_WIDTH, SCREEN_HEIGHT))
                
                # Convert to pygame surface
                frame_surface = pygame.surfarray.make_surface(frame_resized)
                surface.blit(frame_surface, (0, 0))
        else:
            # Fallback if no webcam
            self.draw_fallback(surface)

    def draw_fallback(self, surface):
        # Draw colorful patterns when no webcam
        for i in range(50):
            x = random.randint(0, SCREEN_WIDTH)
            y = random.randint(0, SCREEN_HEIGHT)
            color = random.choice(self.colors)
            pygame.draw.circle(surface, color, (x, y), random.randint(5, 20))

class MatplotlibPlot(ScreenSaver):
    def __init__(self):
        super().__init__("Matplotlib Plot", 8000)
        self.points = []
        self.generate_points()

    def generate_points(self):
        for _ in range(100):
            point = {
                'x': random.uniform(-10, 10),
                'y': random.uniform(-10, 10),
                'color': random.choice(self.colors)
            }
            self.points.append(point)

    def update(self):
        self.phase += 0.02

    def draw(self, surface):
        center_x, center_y = SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2
        scale = 30
        
        # Draw coordinate grid
        for i in range(-10, 11):
            x = center_x + i * scale
            pygame.draw.line(surface, (50, 50, 50), (x, 0), (x, SCREEN_HEIGHT))
            y = center_y + i * scale
            pygame.draw.line(surface, (50, 50, 50), (0, y), (SCREEN_WIDTH, y))
        
        # Draw points
        for point in self.points:
            x = center_x + point['x'] * scale
            y = center_y + point['y'] * scale
            pygame.draw.circle(surface, point['color'], (int(x), int(y)), 3)

class FourierTransform(ScreenSaver):
    def __init__(self):
        super().__init__("Fourier Transform", 7000)
        self.points = []
        self.generate_points()

    def generate_points(self):
        for i in range(100):
            angle = i * 0.1
            radius = 50 + 30 * math.sin(i * 0.2)
            x = radius * math.cos(angle)
            y = radius * math.sin(angle)
            self.points.append({'x': x, 'y': y, 'angle': angle})

    def update(self):
        self.phase += 0.02

    def draw(self, surface):
        center_x, center_y = SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2
        
        # Draw Fourier series approximation
        points = []
        for t in range(0, 628, 5):  # 0 to 2π
            x, y = 0, 0
            for i, point in enumerate(self.points):
                freq = i + 1
                x += point['x'] * math.cos(freq * t * 0.01 + self.phase) / freq
                y += point['y'] * math.sin(freq * t * 0.01 + self.phase) / freq
            
            screen_x = center_x + x
            screen_y = center_y + y
            points.append((screen_x, screen_y))
        
        if len(points) > 1:
            hue = (self.phase * 50) % 360
            rgb = colorsys.hsv_to_rgb(hue/360, 0.8, 1.0)
            color = tuple(int(c * 255) for c in rgb)
            pygame.draw.lines(surface, color, False, points, 2)

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

class RayTracing(ScreenSaver):
    def __init__(self):
        super().__init__("Ray Tracing", 8000)
        self.spheres = []
        self.generate_spheres()

    def generate_spheres(self):
        for _ in range(5):
            sphere = {
                'x': random.uniform(-5, 5),
                'y': random.uniform(-5, 5),
                'z': random.uniform(2, 10),
                'radius': random.uniform(0.5, 2),
                'color': random.choice(self.colors)
            }
            self.spheres.append(sphere)

    def update(self):
        self.phase += 0.02

    def draw(self, surface):
        # Simple ray tracing
        for x in range(0, SCREEN_WIDTH, 4):
            for y in range(0, SCREEN_HEIGHT, 4):
                # Ray direction
                ray_x = (x - SCREEN_WIDTH/2) / (SCREEN_WIDTH/2)
                ray_y = (y - SCREEN_HEIGHT/2) / (SCREEN_HEIGHT/2)
                ray_z = 1
                
                # Find closest sphere
                min_dist = float('inf')
                closest_color = (0, 0, 0)
                
                for sphere in self.spheres:
                    # Simple sphere intersection
                    dx = ray_x - sphere['x']
                    dy = ray_y - sphere['y']
                    dz = ray_z - sphere['z']
                    dist = math.sqrt(dx*dx + dy*dy + dz*dz)
                    
                    if dist < sphere['radius'] and dist < min_dist:
                        min_dist = dist
                        closest_color = sphere['color']
                
                if min_dist < float('inf'):
                    pygame.draw.circle(surface, closest_color, (x, y), 2)

class WaveInterference(ScreenSaver):
    def __init__(self):
        super().__init__("Wave Interference", 7000)
        self.sources = []
        self.generate_sources()

    def generate_sources(self):
        for _ in range(3):
            source = {
                'x': random.randint(100, SCREEN_WIDTH - 100),
                'y': random.randint(100, SCREEN_HEIGHT - 100),
                'frequency': random.uniform(0.02, 0.05),
                'amplitude': random.uniform(50, 100),
                'phase': random.uniform(0, 2 * math.pi)
            }
            self.sources.append(source)

    def update(self):
        self.phase += 0.03

    def draw(self, surface):
        for x in range(0, SCREEN_WIDTH, 4):
            for y in range(0, SCREEN_HEIGHT, 4):
                # Calculate wave interference
                total_amplitude = 0
                for source in self.sources:
                    distance = math.sqrt((x - source['x'])**2 + (y - source['y'])**2)
                    wave = source['amplitude'] * math.sin(
                        source['frequency'] * distance + source['phase'] + self.phase
                    )
                    total_amplitude += wave
                
                # Color based on interference
                normalized = (total_amplitude + 300) / 600  # Normalize to 0-1
                hue = (normalized * 360 + self.phase * 50) % 360
                rgb = colorsys.hsv_to_rgb(hue/360, 0.8, 1.0)
                color = tuple(int(c * 255) for c in rgb)
                
                pygame.draw.circle(surface, color, (x, y), 2)

class ParticleSwarm(ScreenSaver):
    def __init__(self):
        super().__init__("Particle Swarm", 6000)
        self.particles = []
        self.generate_particles()

    def generate_particles(self):
        for _ in range(50):
            particle = {
                'x': random.uniform(0, SCREEN_WIDTH),
                'y': random.uniform(0, SCREEN_HEIGHT),
                'vx': random.uniform(-2, 2),
                'vy': random.uniform(-2, 2),
                'color': random.choice(self.colors),
                'size': random.uniform(3, 8)
            }
            self.particles.append(particle)

    def update(self):
        self.phase += 0.02
        
        # Update particle positions
        for particle in self.particles:
            particle['x'] += particle['vx']
            particle['y'] += particle['vy']
            
            # Bounce off walls
            if particle['x'] < 0 or particle['x'] > SCREEN_WIDTH:
                particle['vx'] *= -1
            if particle['y'] < 0 or particle['y'] > SCREEN_HEIGHT:
                particle['vy'] *= -1
            
            # Swarm behavior - move towards center
            center_x, center_y = SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2
            dx = center_x - particle['x']
            dy = center_y - particle['y']
            distance = math.sqrt(dx*dx + dy*dy)
            
            if distance > 0:
                particle['vx'] += dx / distance * 0.1
                particle['vy'] += dy / distance * 0.1

    def draw(self, surface):
        for particle in self.particles:
            pygame.draw.circle(surface, particle['color'], 
                             (int(particle['x']), int(particle['y'])), int(particle['size']))

class FractalTree3D(ScreenSaver):
    def __init__(self):
        super().__init__("3D Fractal Tree", 9000)
        self.max_depth = 8

    def draw_branch_3d(self, surface, x, y, z, length, angle_x, angle_y, depth, color):
        if depth > self.max_depth:
            return
            
        # 3D rotation
        end_x = x + length * math.cos(angle_y) * math.cos(angle_x)
        end_y = y + length * math.sin(angle_y) * math.cos(angle_x)
        end_z = z + length * math.sin(angle_x)
        
        # Simple 3D to 2D projection
        scale = 200 / (200 + end_z)
        screen_x = SCREEN_WIDTH // 2 + end_x * scale
        screen_y = SCREEN_HEIGHT // 2 + end_y * scale
        
        # Draw branch
        if depth > 0:
            start_scale = 200 / (200 + z)
            start_x = SCREEN_WIDTH // 2 + x * start_scale
            start_y = SCREEN_HEIGHT // 2 + y * start_scale
            pygame.draw.line(surface, color, (start_x, start_y), (screen_x, screen_y), max(1, 5 - depth))
        
        # Draw leaves at the end
        if depth == self.max_depth:
            pygame.draw.circle(surface, color, (int(screen_x), int(screen_y)), 3)
        
        # Recursive branches
        if depth < self.max_depth:
            new_length = length * 0.7
            new_angle_x1 = angle_x + 0.3 + math.sin(self.phase + depth) * 0.2
            new_angle_x2 = angle_x - 0.3 + math.sin(self.phase + depth) * 0.2
            new_angle_y1 = angle_y + 0.5 + math.sin(self.phase + depth) * 0.3
            new_angle_y2 = angle_y - 0.5 + math.sin(self.phase + depth) * 0.3
            
            hue = (depth * 30 + self.phase * 50) % 360
            rgb = colorsys.hsv_to_rgb(hue/360, 0.8, 1.0)
            new_color = tuple(int(c * 255) for c in rgb)
            
            self.draw_branch_3d(surface, end_x, end_y, end_z, new_length, new_angle_x1, new_angle_y1, depth + 1, new_color)
            self.draw_branch_3d(surface, end_x, end_y, end_z, new_length, new_angle_x2, new_angle_y2, depth + 1, new_color)

    def update(self):
        self.phase += 0.01

    def draw(self, surface):
        start_x, start_y, start_z = 0, 0, 0
        initial_length = 100
        initial_angle_x = -math.pi / 2
        initial_angle_y = 0
        
        hue = (self.phase * 50) % 360
        rgb = colorsys.hsv_to_rgb(hue/360, 0.8, 1.0)
        color = tuple(int(c * 255) for c in rgb)
        
        self.draw_branch_3d(surface, start_x, start_y, start_z, initial_length, 
                           initial_angle_x, initial_angle_y, 0, color)

# Create all library-based screen savers
library_savers = [
    OpenCVWebcam(),
    MatplotlibPlot(),
    FourierTransform(),
    ConwayGameOfLife(),
    PlasmaEffect(),
    RayTracing(),
    WaveInterference(),
    ParticleSwarm(),
    FractalTree3D()
]

# Create variations for each library saver
for i in range(10):  # 10 variations per library saver = 90 more
    for base_saver in library_savers:
        new_saver = type(f"{base_saver.__class__.__name__}Variation{i}", 
                        (base_saver.__class__,), {})()
        new_saver.name = f"{base_saver.name} Variation {i+1}"
        new_saver.duration = random.randint(3000, 10000)
        library_savers.append(new_saver) 