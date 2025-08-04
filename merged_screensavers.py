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
GRAY = (100, 100, 100)
LIGHT_GRAY = (150, 150, 150)
DARK_GRAY = (50, 50, 50)
BLUE = (100, 150, 255)
GREEN = (100, 255, 100)
RED = (255, 100, 100)
PURPLE = (255, 100, 255)

# Import additional libraries for advanced effects
try:
    import cv2
    CV2_AVAILABLE = True
except ImportError:
    CV2_AVAILABLE = False

class UIState:
    MAIN_MENU = "main_menu"
    SCREENSAVER = "screensaver"
    SETTINGS = "settings"

class Settings:
    def __init__(self):
        self.play_mode = "random"  # "random" or "sequential"
        self.duration = 5000  # milliseconds
        self.auto_advance = True
        self.show_preview = True

class PreviewRenderer:
    def __init__(self, width=180, height=120):
        self.width = width
        self.height = height
        self.surface = pygame.Surface((width, height))
        self.preview_cache = {}
        
    def generate_static_preview(self, screensaver_instance):
        """Generate a static preview for the screensaver"""
        preview_surface = pygame.Surface((self.width, self.height))
        preview_surface.fill(BLACK)
        
        try:
            # Create a copy of the instance for preview
            preview_saver = type(screensaver_instance)()
            preview_saver.start_time = time.time() - 1000  # Start 1 second ago
            
            # Run multiple updates to get a more interesting preview
            for _ in range(5):
                preview_saver.update()
            
            # Draw the preview
            preview_saver.draw(preview_surface)
            
            # Add a subtle border
            pygame.draw.rect(preview_surface, GRAY, (0, 0, self.width, self.height), 1)
            
        except Exception as e:
            # Create a colorful placeholder based on the screen saver name
            name = screensaver_instance.name.lower()
            if 'math' in name or 'function' in name or 'equation' in name:
                # Math-themed placeholder
                color = PURPLE
                for i in range(10):
                    x = random.randint(5, self.width-5)
                    y = random.randint(5, self.height-5)
                    pygame.draw.circle(preview_surface, color, (x, y), 2)
            elif 'particle' in name or 'explosion' in name:
                # Particle-themed placeholder
                color = RED
                for i in range(15):
                    x = random.randint(5, self.width-5)
                    y = random.randint(5, self.height-5)
                    pygame.draw.circle(preview_surface, color, (x, y), 1)
            elif 'space' in name or 'galaxy' in name or 'star' in name:
                # Space-themed placeholder
                color = BLUE
                for i in range(8):
                    x = random.randint(5, self.width-5)
                    y = random.randint(5, self.height-5)
                    pygame.draw.circle(preview_surface, color, (x, y), 1)
            elif 'color' in name or 'rainbow' in name:
                # Color-themed placeholder
                colors = [RED, GREEN, BLUE, PURPLE]
                for i in range(12):
                    x = random.randint(5, self.width-5)
                    y = random.randint(5, self.height-5)
                    pygame.draw.circle(preview_surface, random.choice(colors), (x, y), 2)
            else:
                # Generic placeholder
                color = GREEN
                for i in range(6):
                    x = random.randint(5, self.width-5)
                    y = random.randint(5, self.height-5)
                    pygame.draw.circle(preview_surface, color, (x, y), 3)
            
            # Add border
            pygame.draw.rect(preview_surface, GRAY, (0, 0, self.width, self.height), 1)
        
        return preview_surface
        
    def get_preview(self, screensaver_instance):
        """Get cached preview or generate new one"""
        saver_name = screensaver_instance.name
        if saver_name not in self.preview_cache:
            self.preview_cache[saver_name] = self.generate_static_preview(screensaver_instance)
        return self.preview_cache[saver_name]

class MainMenu:
    def __init__(self, screen_savers, settings):
        self.screen_savers = screen_savers
        self.settings = settings
        self.preview_renderer = PreviewRenderer()
        self.selected_index = 0
        self.grid_width = 6  # Reduced from 10
        self.grid_height = 4  # Increased from 2
        self.preview_width = 180  # Increased from 120
        self.preview_height = 120  # Increased from 80
        self.padding = 15  # Increased from 10
        self.start_x = 30
        self.start_y = 120
        
    def get_grid_position(self, index):
        """Convert index to grid position"""
        row = index // self.grid_width
        col = index % self.grid_width
        x = self.start_x + col * (self.preview_width + self.padding)
        y = self.start_y + row * (self.preview_height + self.padding)
        return x, y
        
    def get_index_from_pos(self, pos):
        """Convert mouse position to grid index"""
        x, y = pos
        for i in range(len(self.screen_savers)):
            grid_x, grid_y = self.get_grid_position(i)
            if (grid_x <= x <= grid_x + self.preview_width and 
                grid_y <= y <= grid_y + self.preview_height):
                return i
        return -1
        
    def handle_click(self, pos):
        """Handle mouse click on grid"""
        index = self.get_index_from_pos(pos)
        if index >= 0:
            return self.screen_savers[index]
        return None
        
    def draw(self, surface):
        surface.fill(BLACK)
        
        # Draw title
        font_large = pygame.font.Font(None, 48)
        title = font_large.render("Screen Saver Gallery", True, WHITE)
        surface.blit(title, (SCREEN_WIDTH//2 - title.get_width()//2, 30))
        
        # Draw subtitle
        font_small = pygame.font.Font(None, 24)
        subtitle = font_small.render(f"Click to preview • {len(self.screen_savers)} total", True, LIGHT_GRAY)
        surface.blit(subtitle, (SCREEN_WIDTH//2 - subtitle.get_width()//2, 80))
        
        # Draw grid of previews
        for i, saver_instance in enumerate(self.screen_savers):
            x, y = self.get_grid_position(i)
            
            # Get cached preview
            preview = self.preview_renderer.get_preview(saver_instance)
            surface.blit(preview, (x, y))
            
            # Draw selection highlight
            if i == self.selected_index:
                pygame.draw.rect(surface, BLUE, (x-2, y-2, self.preview_width+4, self.preview_height+4), 3)
            
            # Draw name
            font = pygame.font.Font(None, 16)
            name = saver_instance.name
            if len(name) > 15:
                name = name[:12] + "..."
            text = font.render(name, True, WHITE)
            text_rect = text.get_rect(center=(x + self.preview_width//2, y + self.preview_height + 15))
            surface.blit(text, text_rect)
        
        # Draw controls
        font = pygame.font.Font(None, 24)
        controls = [
            "Controls:",
            "• Click any preview to start that screen saver",
            "• ESC to return to menu",
            "• SPACE to skip to next",
            "• S for settings"
        ]
        
        for i, control in enumerate(controls):
            color = WHITE if i == 0 else LIGHT_GRAY
            text = font.render(control, True, color)
            surface.blit(text, (20, SCREEN_HEIGHT - 120 + i * 25))

class SettingsMenu:
    def __init__(self, settings):
        self.settings = settings
        self.selected_option = 0
        self.options = [
            ("Play Mode", ["Random", "Sequential"]),
            ("Duration (seconds)", ["3", "5", "8", "10", "15"]),
            ("Auto Advance", ["On", "Off"]),
            ("Show Preview", ["On", "Off"])
        ]
        
    def handle_key(self, key):
        """Handle key presses in settings"""
        if key == pygame.K_UP:
            self.selected_option = (self.selected_option - 1) % len(self.options)
        elif key == pygame.K_DOWN:
            self.selected_option = (self.selected_option + 1) % len(self.options)
        elif key == pygame.K_LEFT or key == pygame.K_RIGHT:
            self._change_setting()
        elif key == pygame.K_RETURN:
            self._change_setting()
            
    def _change_setting(self):
        """Change the current setting"""
        if self.selected_option == 0:  # Play Mode
            current = self.settings.play_mode
            options = ["random", "sequential"]
            current_index = options.index(current)
            self.settings.play_mode = options[(current_index + 1) % len(options)]
        elif self.selected_option == 1:  # Duration
            current = str(self.settings.duration // 1000)
            options = ["3", "5", "8", "10", "15"]
            current_index = options.index(current)
            new_duration = int(options[(current_index + 1) % len(options)])
            self.settings.duration = new_duration * 1000
        elif self.selected_option == 2:  # Auto Advance
            self.settings.auto_advance = not self.settings.auto_advance
        elif self.selected_option == 3:  # Show Preview
            self.settings.show_preview = not self.settings.show_preview
            
    def draw(self, surface):
        surface.fill(BLACK)
        
        # Draw title
        font_large = pygame.font.Font(None, 48)
        title = font_large.render("Settings", True, WHITE)
        surface.blit(title, (SCREEN_WIDTH//2 - title.get_width()//2, 50))
        
        # Draw options
        font = pygame.font.Font(None, 32)
        start_y = 150
        
        for i, (name, values) in enumerate(self.options):
            y = start_y + i * 60
            
            # Highlight selected option
            color = BLUE if i == self.selected_option else WHITE
            pygame.draw.rect(surface, color, (50, y-5, SCREEN_WIDTH-100, 50), 2 if i == self.selected_option else 0)
            
            # Draw option name
            name_text = font.render(name, True, WHITE)
            surface.blit(name_text, (70, y + 10))
            
            # Draw current value
            if name == "Play Mode":
                value = self.settings.play_mode.title()
            elif name == "Duration (seconds)":
                value = str(self.settings.duration // 1000)
            elif name == "Auto Advance":
                value = "On" if self.settings.auto_advance else "Off"
            elif name == "Show Preview":
                value = "On" if self.settings.show_preview else "Off"
            else:
                value = "Unknown"
                
            value_text = font.render(value, True, GREEN)
            surface.blit(value_text, (SCREEN_WIDTH - 200, y + 10))
            
            # Draw arrow indicators
            if i == self.selected_option:
                arrow_left = font.render("←", True, LIGHT_GRAY)
                arrow_right = font.render("→", True, LIGHT_GRAY)
                surface.blit(arrow_left, (SCREEN_WIDTH - 250, y + 10))
                surface.blit(arrow_right, (SCREEN_WIDTH - 150, y + 10))
        
        # Draw controls
        font_small = pygame.font.Font(None, 24)
        controls = [
            "Controls:",
            "• UP/DOWN to select option",
            "• LEFT/RIGHT or ENTER to change value",
            "• ESC to return to menu"
        ]
        
        for i, control in enumerate(controls):
            color = WHITE if i == 0 else LIGHT_GRAY
            text = font_small.render(control, True, color)
            surface.blit(text, (20, SCREEN_HEIGHT - 120 + i * 25))

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
        # For games, check if they're finished or if space was pressed
        if hasattr(self, 'game_over') and self.game_over:
            return True
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
        self.decay = random.uniform(2, 5)

    def update(self):
        self.x += self.velocity[0]
        self.y += self.velocity[1]
        self.life -= self.decay
        self.size = max(0, self.size - 0.1)

    def draw(self, surface):
        if self.life > 0:
            alpha = max(0, min(255, int(self.life)))
            color = (*self.color[:3], alpha)
            pygame.draw.circle(surface, color, (int(self.x), int(self.y)), int(self.size))

# ===== ALL SCREEN SAVERS =====

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

# ===== MATH-BASED SCREEN SAVERS =====

class AnimatedLinearFunction(ScreenSaver):
    def __init__(self):
        super().__init__("Animated Linear Function", 8000)
        self.m = random.uniform(-2, 2)
        self.b = random.uniform(-150, 150)
        self.m_change = random.uniform(-0.03, 0.03)
        self.b_change = random.uniform(-2, 2)
        self.points = []
        self.equation_text = "y = mx + b"
        self.change_timer = 0
        
    def update(self):
        self.m += self.m_change
        self.b += self.b_change
        self.change_timer += 1
        
        # Randomly change direction and speed
        if self.change_timer > 60:  # Every 60 frames
            self.m_change = random.uniform(-0.05, 0.05)
            self.b_change = random.uniform(-3, 3)
            self.change_timer = 0
        
        # Bounce off limits
        if abs(self.m) > 4:
            self.m_change *= -1
            self.m = 4 if self.m > 0 else -4
        if abs(self.b) > 300:
            self.b_change *= -1
            self.b = 300 if self.b > 0 else -300
            
        # Update equation text
        self.equation_text = f"y = {self.m:.2f}x + {self.b:.1f}"
        
    def draw(self, surface):
        # Draw coordinate grid
        center_x, center_y = SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2
        
        # Draw axes
        pygame.draw.line(surface, (100, 100, 100), (0, center_y), (SCREEN_WIDTH, center_y), 2)
        pygame.draw.line(surface, (100, 100, 100), (center_x, 0), (center_x, SCREEN_HEIGHT), 2)
        
        # Draw grid lines
        for i in range(-10, 11):
            x = center_x + i * 50
            pygame.draw.line(surface, (50, 50, 50), (x, 0), (x, SCREEN_HEIGHT), 1)
            y = center_y + i * 50
            pygame.draw.line(surface, (50, 50, 50), (0, y), (SCREEN_WIDTH, y), 1)
        
        # Draw function
        points = []
        for x in range(-center_x, center_x, 5):
            screen_x = center_x + x
            screen_y = center_y - (self.m * x + self.b)
            if 0 <= screen_y <= SCREEN_HEIGHT:
                points.append((screen_x, screen_y))
        
        if len(points) > 1:
            pygame.draw.lines(surface, (255, 100, 100), False, points, 3)
        
        # Draw equation
        font = pygame.font.Font(None, 48)
        text = font.render(self.equation_text, True, (255, 255, 255))
        surface.blit(text, (20, 20))

class OscillatingQuadratic(ScreenSaver):
    def __init__(self):
        super().__init__("Oscillating Quadratic", 8000)
        self.a = random.uniform(-0.8, 0.8)
        self.b = random.uniform(-3, 3)
        self.c = random.uniform(-150, 150)
        self.a_change = random.uniform(-0.02, 0.02)
        self.b_change = random.uniform(-0.1, 0.1)
        self.c_change = random.uniform(-3, 3)
        self.change_timer = 0
        
    def update(self):
        self.a += self.a_change
        self.b += self.b_change
        self.c += self.c_change
        self.change_timer += 1
        
        # Randomly change direction and speed
        if self.change_timer > 45:  # Every 45 frames
            self.a_change = random.uniform(-0.03, 0.03)
            self.b_change = random.uniform(-0.15, 0.15)
            self.c_change = random.uniform(-4, 4)
            self.change_timer = 0
        
        # Bounce off limits with more dynamic behavior
        if abs(self.a) > 1.2:
            self.a_change *= -1
            self.a = 1.2 if self.a > 0 else -1.2
        if abs(self.b) > 4:
            self.b_change *= -1
            self.b = 4 if self.b > 0 else -4
        if abs(self.c) > 250:
            self.c_change *= -1
            self.c = 250 if self.c > 0 else -250
            
    def draw(self, surface):
        center_x, center_y = SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2
        
        # Draw axes
        pygame.draw.line(surface, (100, 100, 100), (0, center_y), (SCREEN_WIDTH, center_y), 2)
        pygame.draw.line(surface, (100, 100, 100), (center_x, 0), (center_x, SCREEN_HEIGHT), 2)
        
        # Draw parabola
        points = []
        for x in range(-center_x, center_x, 5):
            screen_x = center_x + x
            y = self.a * x**2 + self.b * x + self.c
            screen_y = center_y - y
            if 0 <= screen_y <= SCREEN_HEIGHT:
                points.append((screen_x, screen_y))
        
        if len(points) > 1:
            pygame.draw.lines(surface, (100, 255, 100), False, points, 3)
        
        # Draw equation
        font = pygame.font.Font(None, 36)
        equation = f"y = {self.a:.2f}x² + {self.b:.2f}x + {self.c:.1f}"
        text = font.render(equation, True, (255, 255, 255))
        surface.blit(text, (20, 20))

class CubicFunctionMorph(ScreenSaver):
    def __init__(self):
        super().__init__("Cubic Function Morph", 8000)
        self.a = random.uniform(-0.15, 0.15)
        self.b = random.uniform(-0.8, 0.8)
        self.c = random.uniform(-3, 3)
        self.d = random.uniform(-150, 150)
        self.a_change = random.uniform(-0.008, 0.008)
        self.b_change = random.uniform(-0.015, 0.015)
        self.c_change = random.uniform(-0.08, 0.08)
        self.d_change = random.uniform(-2, 2)
        self.change_timer = 0
        
    def update(self):
        self.a += self.a_change
        self.b += self.b_change
        self.c += self.c_change
        self.d += self.d_change
        self.change_timer += 1
        
        # Randomly change direction and speed
        if self.change_timer > 40:  # Every 40 frames
            self.a_change = random.uniform(-0.012, 0.012)
            self.b_change = random.uniform(-0.02, 0.02)
            self.c_change = random.uniform(-0.1, 0.1)
            self.d_change = random.uniform(-3, 3)
            self.change_timer = 0
        
        # Bounce off limits with more dynamic behavior
        if abs(self.a) > 0.25:
            self.a_change *= -1
            self.a = 0.25 if self.a > 0 else -0.25
        if abs(self.b) > 1.2:
            self.b_change *= -1
            self.b = 1.2 if self.b > 0 else -1.2
        if abs(self.c) > 4:
            self.c_change *= -1
            self.c = 4 if self.c > 0 else -4
        if abs(self.d) > 250:
            self.d_change *= -1
            self.d = 250 if self.d > 0 else -250
            
    def draw(self, surface):
        center_x, center_y = SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2
        
        # Draw axes
        pygame.draw.line(surface, (100, 100, 100), (0, center_y), (SCREEN_WIDTH, center_y), 2)
        pygame.draw.line(surface, (100, 100, 100), (center_x, 0), (center_x, SCREEN_HEIGHT), 2)
        
        # Draw cubic function
        points = []
        for x in range(-center_x, center_x, 5):
            screen_x = center_x + x
            y = self.a * x**3 + self.b * x**2 + self.c * x + self.d
            screen_y = center_y - y
            if 0 <= screen_y <= SCREEN_HEIGHT:
                points.append((screen_x, screen_y))
        
        if len(points) > 1:
            pygame.draw.lines(surface, (255, 100, 255), False, points, 3)
        
        # Draw equation
        font = pygame.font.Font(None, 36)
        equation = f"y = {self.a:.3f}x³ + {self.b:.2f}x² + {self.c:.2f}x + {self.d:.1f}"
        text = font.render(equation, True, (255, 255, 255))
        surface.blit(text, (20, 20))

class TrigonometricFunctionWave(ScreenSaver):
    def __init__(self):
        super().__init__("Trigonometric Function Wave", 8000)
        self.amplitude = random.uniform(50, 200)
        self.frequency = random.uniform(0.01, 0.03)
        self.phase = random.uniform(0, 2 * math.pi)
        self.vertical_shift = random.uniform(-100, 100)
        self.amplitude_change = random.uniform(-2, 2)
        self.frequency_change = random.uniform(-0.001, 0.001)
        self.phase_change = random.uniform(-0.05, 0.05)
        self.shift_change = random.uniform(-1, 1)
        self.change_timer = 0
        
    def update(self):
        self.amplitude += self.amplitude_change
        self.frequency += self.frequency_change
        self.phase += self.phase_change
        self.vertical_shift += self.shift_change
        self.change_timer += 1
        
        # Randomly change direction and speed
        if self.change_timer > 50:
            self.amplitude_change = random.uniform(-3, 3)
            self.frequency_change = random.uniform(-0.002, 0.002)
            self.phase_change = random.uniform(-0.08, 0.08)
            self.shift_change = random.uniform(-2, 2)
            self.change_timer = 0
        
        # Bounce off limits
        if abs(self.amplitude) > 250:
            self.amplitude_change *= -1
            self.amplitude = 250 if self.amplitude > 0 else -250
        if abs(self.frequency) > 0.05:
            self.frequency_change *= -1
            self.frequency = 0.05 if self.frequency > 0 else -0.05
        if abs(self.vertical_shift) > 150:
            self.shift_change *= -1
            self.vertical_shift = 150 if self.vertical_shift > 0 else -150
            
    def draw(self, surface):
        center_x, center_y = SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2
        
        # Draw axes
        pygame.draw.line(surface, (100, 100, 100), (0, center_y), (SCREEN_WIDTH, center_y), 2)
        pygame.draw.line(surface, (100, 100, 100), (center_x, 0), (center_x, SCREEN_HEIGHT), 2)
        
        # Draw trigonometric function
        points = []
        for x in range(-center_x, center_x, 5):
            screen_x = center_x + x
            y = self.amplitude * math.sin(self.frequency * x + self.phase) + self.vertical_shift
            screen_y = center_y - y
            if 0 <= screen_y <= SCREEN_HEIGHT:
                points.append((screen_x, screen_y))
        
        if len(points) > 1:
            pygame.draw.lines(surface, (100, 255, 255), False, points, 3)
        
        # Draw equation
        font = pygame.font.Font(None, 36)
        equation = f"y = {self.amplitude:.0f}sin({self.frequency:.3f}x + {self.phase:.2f}) + {self.vertical_shift:.0f}"
        text = font.render(equation, True, (255, 255, 255))
        surface.blit(text, (20, 20))

class ExponentialGrowthDecay(ScreenSaver):
    def __init__(self):
        super().__init__("Exponential Growth/Decay", 8000)
        self.base = random.uniform(0.5, 2.0)
        self.coefficient = random.uniform(-100, 100)
        self.vertical_shift = random.uniform(-50, 50)
        self.base_change = random.uniform(-0.02, 0.02)
        self.coeff_change = random.uniform(-2, 2)
        self.shift_change = random.uniform(-1, 1)
        self.change_timer = 0
        
    def update(self):
        self.base += self.base_change
        self.coefficient += self.coeff_change
        self.vertical_shift += self.shift_change
        self.change_timer += 1
        
        # Randomly change direction and speed
        if self.change_timer > 55:
            self.base_change = random.uniform(-0.03, 0.03)
            self.coeff_change = random.uniform(-3, 3)
            self.shift_change = random.uniform(-2, 2)
            self.change_timer = 0
        
        # Bounce off limits
        if abs(self.base) > 3:
            self.base_change *= -1
            self.base = 3 if self.base > 0 else 0.1
        if abs(self.coefficient) > 150:
            self.coeff_change *= -1
            self.coefficient = 150 if self.coefficient > 0 else -150
        if abs(self.vertical_shift) > 100:
            self.shift_change *= -1
            self.vertical_shift = 100 if self.vertical_shift > 0 else -100
            
    def draw(self, surface):
        center_x, center_y = SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2
        
        # Draw axes
        pygame.draw.line(surface, (100, 100, 100), (0, center_y), (SCREEN_WIDTH, center_y), 2)
        pygame.draw.line(surface, (100, 100, 100), (center_x, 0), (center_x, SCREEN_HEIGHT), 2)
        
        # Draw exponential function
        points = []
        for x in range(-center_x//2, center_x//2, 5):
            screen_x = center_x + x
            y = self.coefficient * (self.base ** (x/50)) + self.vertical_shift
            screen_y = center_y - y
            if 0 <= screen_y <= SCREEN_HEIGHT:
                points.append((screen_x, screen_y))
        
        if len(points) > 1:
            pygame.draw.lines(surface, (255, 200, 100), False, points, 3)
        
        # Draw equation
        font = pygame.font.Font(None, 36)
        equation = f"y = {self.coefficient:.0f} * {self.base:.2f}^x + {self.vertical_shift:.0f}"
        text = font.render(equation, True, (255, 255, 255))
        surface.blit(text, (20, 20))

class LogarithmicFunction(ScreenSaver):
    def __init__(self):
        super().__init__("Logarithmic Function", 8000)
        self.coefficient = random.uniform(-100, 100)
        self.base = random.uniform(2, 10)
        self.vertical_shift = random.uniform(-100, 100)
        self.coeff_change = random.uniform(-2, 2)
        self.base_change = random.uniform(-0.1, 0.1)
        self.shift_change = random.uniform(-2, 2)
        self.change_timer = 0
        
    def update(self):
        self.coefficient += self.coeff_change
        self.base += self.base_change
        self.vertical_shift += self.shift_change
        self.change_timer += 1
        
        # Randomly change direction and speed
        if self.change_timer > 60:
            self.coeff_change = random.uniform(-3, 3)
            self.base_change = random.uniform(-0.15, 0.15)
            self.shift_change = random.uniform(-3, 3)
            self.change_timer = 0
        
        # Bounce off limits
        if abs(self.coefficient) > 150:
            self.coeff_change *= -1
            self.coefficient = 150 if self.coefficient > 0 else -150
        if abs(self.base) > 15 or self.base < 1.5:
            self.base_change *= -1
            self.base = max(1.5, min(15, self.base))
        if abs(self.vertical_shift) > 150:
            self.shift_change *= -1
            self.vertical_shift = 150 if self.vertical_shift > 0 else -150
            
    def draw(self, surface):
        center_x, center_y = SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2
        
        # Draw axes
        pygame.draw.line(surface, (100, 100, 100), (0, center_y), (SCREEN_WIDTH, center_y), 2)
        pygame.draw.line(surface, (100, 100, 100), (center_x, 0), (center_x, SCREEN_HEIGHT), 2)
        
        # Draw logarithmic function
        points = []
        for x in range(1, center_x, 5):
            screen_x = center_x + x
            try:
                y = self.coefficient * math.log(x/50, self.base) + self.vertical_shift
                screen_y = center_y - y
                if 0 <= screen_y <= SCREEN_HEIGHT:
                    points.append((screen_x, screen_y))
            except:
                pass
        
        if len(points) > 1:
            pygame.draw.lines(surface, (255, 100, 200), False, points, 3)
        
        # Draw equation
        font = pygame.font.Font(None, 36)
        equation = f"y = {self.coefficient:.0f} * log_{self.base:.1f}(x) + {self.vertical_shift:.0f}"
        text = font.render(equation, True, (255, 255, 255))
        surface.blit(text, (20, 20))

# Import all screen savers from all_screensavers.py
try:
    from all_screensavers import all_screen_savers
    ADDITIONAL_SAVERS_AVAILABLE = True
    print(f"Successfully imported {len(all_screen_savers)} screen savers from all_screensavers.py")
except ImportError as e:
    print(f"Could not import from all_screensavers.py: {e}")
    ADDITIONAL_SAVERS_AVAILABLE = False

# Create list of all screen savers (math-based ones first)
math_savers = [
    AnimatedLinearFunction(),
    OscillatingQuadratic(),
    CubicFunctionMorph(),
    TrigonometricFunctionWave(),
    ExponentialGrowthDecay(),
    LogarithmicFunction(),
]

# Create list of basic screen savers
basic_savers = [
    CosmicDance(),
    RainbowWaves(),
    ParticleExplosion(),
    GeometricHypnosis(),
    NeuralNetwork(),
    ColorfulBubbles(),
    MatrixRain(),
]

# Combine all screen savers
screen_savers = math_savers + basic_savers

# Add all screen savers from all_screensavers.py if available
if ADDITIONAL_SAVERS_AVAILABLE:
    # Remove duplicates by name
    existing_names = {saver.name for saver in screen_savers}
    unique_additional = [saver for saver in all_screen_savers if saver.name not in existing_names]
    screen_savers.extend(unique_additional)
    print(f"Added {len(unique_additional)} unique additional screen savers")
    print(f"Removed {len(all_screen_savers) - len(unique_additional)} duplicates")

if __name__ == "__main__":
    # Initialize UI system
    settings = Settings()
    main_menu = MainMenu(screen_savers, settings)
    settings_menu = SettingsMenu(settings)
    
    # Generate all previews upfront
    print("Generating previews...")
    for i, saver in enumerate(screen_savers):
        main_menu.preview_renderer.get_preview(saver)
        if i % 10 == 0:
            print(f"Generated {i}/{len(screen_savers)} previews...")
            # Show loading screen
            screen.fill(BLACK)
            font = pygame.font.Font(None, 48)
            title = font.render("Loading Screen Saver Gallery", True, WHITE)
            screen.blit(title, (SCREEN_WIDTH//2 - title.get_width()//2, SCREEN_HEIGHT//2 - 50))
            
            font_small = pygame.font.Font(None, 24)
            progress = font_small.render(f"Generating previews: {i}/{len(screen_savers)}", True, LIGHT_GRAY)
            screen.blit(progress, (SCREEN_WIDTH//2 - progress.get_width()//2, SCREEN_HEIGHT//2 + 20))
            
            pygame.display.flip()
    print("All previews generated!")
    
    # UI state management
    current_state = UIState.MAIN_MENU
    current_saver = None
    current_saver_index = 0
    
    print(f"Total screen savers created: {len(screen_savers)}")
    print("Available screen savers:")
    for i, saver in enumerate(screen_savers):
        print(f"  {i+1}. {saver.name}")
    
    print("\nStarting with UI Gallery...")
    clock = pygame.time.Clock()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if current_state == UIState.SCREENSAVER:
                        current_state = UIState.MAIN_MENU
                        current_saver = None
                    elif current_state == UIState.SETTINGS:
                        current_state = UIState.MAIN_MENU
                    else:
                        running = False
                elif event.key == pygame.K_SPACE and current_state == UIState.SCREENSAVER:
                    # Force switch to a new screen saver
                    if settings.play_mode == "random":
                        current_saver = type(random.choice(screen_savers))()
                    else:
                        current_saver_index = (current_saver_index + 1) % len(screen_savers)
                        current_saver = type(screen_savers[current_saver_index])()
                    current_saver.start_time = time.time()
                    current_saver.duration = settings.duration
                elif event.key == pygame.K_s and current_state == UIState.MAIN_MENU:
                    current_state = UIState.SETTINGS
                elif current_state == UIState.SETTINGS:
                    settings_menu.handle_key(event.key)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if current_state == UIState.MAIN_MENU:
                    # Handle click on preview grid
                    selected_saver = main_menu.handle_click(event.pos)
                    if selected_saver:
                        current_saver = type(selected_saver)()
                        current_saver.start_time = time.time()
                        current_saver.duration = settings.duration
                        current_state = UIState.SCREENSAVER
                        current_saver_index = screen_savers.index(selected_saver)
                elif current_state == UIState.SCREENSAVER:
                    # Pass click to current saver
                    if hasattr(current_saver, 'click_effect'):
                        current_saver.click_effect(event.pos)
            elif event.type == pygame.MOUSEMOTION:
                # Pass mouse position to current saver for interactivity
                if current_state == UIState.SCREENSAVER and current_saver:
                    if hasattr(current_saver, 'mouse_pos'):
                        current_saver.mouse_pos = event.pos
                    if hasattr(current_saver, 'interactive_update'):
                        current_saver.interactive_update(event.pos)

        # Update current state
        if current_state == UIState.SCREENSAVER and current_saver:
            # Check if current saver is finished
            if current_saver.is_finished() and settings.auto_advance:
                if settings.play_mode == "random":
                    current_saver = type(random.choice(screen_savers))()
                else:
                    current_saver_index = (current_saver_index + 1) % len(screen_savers)
                    current_saver = type(screen_savers[current_saver_index])()
                current_saver.start_time = time.time()
                current_saver.duration = settings.duration

        # Clear screen
        screen.fill(BLACK)

        # Draw current state
        if current_state == UIState.MAIN_MENU:
            main_menu.draw(screen)
        elif current_state == UIState.SETTINGS:
            settings_menu.draw(screen)
        elif current_state == UIState.SCREENSAVER and current_saver:
            # Update and draw current saver
            current_saver.update()
            current_saver.draw(screen)

            # Display current saver name and controls
            font = pygame.font.Font(None, 36)
            text = font.render(f"Current: {current_saver.name}", True, WHITE)
            screen.blit(text, (10, 10))
            
            # Show controls
            font_small = pygame.font.Font(None, 24)
            controls = [
                "ESC: Return to menu",
                "SPACE: Next screen saver",
                f"Mode: {settings.play_mode.title()}",
                f"Duration: {settings.duration//1000}s"
            ]
            for i, control in enumerate(controls):
                text = font_small.render(control, True, LIGHT_GRAY)
                screen.blit(text, (10, SCREEN_HEIGHT - 100 + i * 20))

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit() 