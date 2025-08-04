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
        # Draw title
        font = pygame.font.Font(None, 48)
        title = font.render("Screen Saver Gallery", True, WHITE)
        surface.blit(title, (SCREEN_WIDTH//2 - title.get_width()//2, 20))
        
        # Draw subtitle
        font_small = pygame.font.Font(None, 24)
        subtitle = font_small.render(f"Click to preview • {len(self.screen_savers)} total", True, LIGHT_GRAY)
        surface.blit(subtitle, (SCREEN_WIDTH//2 - subtitle.get_width()//2, 70))
        
        # Draw grid of screen saver names
        for i, saver_instance in enumerate(self.screen_savers):
            if i >= 24:  # Limit to 6x4 grid
                break
                
            grid_x, grid_y = self.get_grid_position(i)
            
            # Draw background rectangle
            pygame.draw.rect(surface, DARK_GRAY, (grid_x, grid_y, 180, 120))
            pygame.draw.rect(surface, LIGHT_GRAY, (grid_x, grid_y, 180, 120), 2)
            
            # Draw screen saver name
            font_name = pygame.font.Font(None, 20)
            name_lines = self._wrap_text(saver_instance.name, font_name, 160)
            
            for j, line in enumerate(name_lines):
                text = font_name.render(line, True, WHITE)
                text_x = grid_x + (180 - text.get_width()) // 2
                text_y = grid_y + 10 + j * 20
                surface.blit(text, (text_x, text_y))
            
            # Draw equation for math-based screen savers
            if any(math_keyword in saver_instance.name.lower() for math_keyword in 
                   ['function', 'linear', 'quadratic', 'cubic', 'trigonometric', 'exponential', 'logarithmic']):
                equation = self._get_equation(saver_instance)
                if equation:
                    font_eq = pygame.font.Font(None, 16)
                    eq_text = font_eq.render(equation, True, LIGHT_GRAY)
                    eq_x = grid_x + (180 - eq_text.get_width()) // 2
                    eq_y = grid_y + 80
                    surface.blit(eq_text, (eq_x, eq_y))
    
    def _wrap_text(self, text, font, max_width):
        """Wrap text to fit within max_width"""
        words = text.split()
        lines = []
        current_line = ""
        
        for word in words:
            test_line = current_line + " " + word if current_line else word
            if font.render(test_line, True, WHITE).get_width() <= max_width:
                current_line = test_line
            else:
                if current_line:
                    lines.append(current_line)
                current_line = word
        
        if current_line:
            lines.append(current_line)
        
        return lines[:2]  # Limit to 2 lines
    
    def _get_equation(self, saver_instance):
        """Get the current equation for math-based screen savers"""
        if hasattr(saver_instance, 'get_equation'):
            return saver_instance.get_equation()
        
        # Default equations based on screen saver name
        name = saver_instance.name.lower()
        if 'linear' in name:
            return "f(x) = mx + b"
        elif 'quadratic' in name:
            return "f(x) = ax² + bx + c"
        elif 'cubic' in name:
            return "f(x) = ax³ + bx² + cx + d"
        elif 'trigonometric' in name:
            return "f(x) = A sin(Bx + C) + D"
        elif 'exponential' in name:
            return "f(x) = a * b^x + c"
        elif 'logarithmic' in name:
            return "f(x) = a * log_b(x) + c"
        
        return None

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
        self.b = random.uniform(-100, 100)
        self.m_change = random.uniform(-0.01, 0.01)
        self.b_change = random.uniform(-1, 1)
        self.change_counter = 0
        self.colors = self.generate_colors()

    def update(self):
        self.change_counter += 1
        if self.change_counter >= 120:  # Reduced from 60 to 120 for less sporadic changes
            self.m_change = random.uniform(-0.01, 0.01)
            self.b_change = random.uniform(-1, 1)
            self.change_counter = 0
        
        self.m += self.m_change
        self.b += self.b_change
        
        # Bounce off limits
        if self.m < -3 or self.m > 3:
            self.m_change *= -1
        if self.b < -150 or self.b > 150:
            self.b_change *= -1

    def get_equation(self):
        return f"f(x) = {self.m:.2f}x + {self.b:.1f}"

    def draw(self, surface):
        # Draw coordinate grid
        for x in range(0, SCREEN_WIDTH, 50):
            pygame.draw.line(surface, DARK_GRAY, (x, 0), (x, SCREEN_HEIGHT), 1)
        for y in range(0, SCREEN_HEIGHT, 50):
            pygame.draw.line(surface, DARK_GRAY, (0, y), (SCREEN_WIDTH, y), 1)
        
        # Draw linear function
        points = []
        for x in range(0, SCREEN_WIDTH):
            y = SCREEN_HEIGHT // 2 - int(self.m * x + self.b)
            if 0 <= y < SCREEN_HEIGHT:
                points.append((x, y))
        
        if len(points) > 1:
            pygame.draw.lines(surface, self.colors[0], False, points, 3)
        
        # Draw equation
        font = pygame.font.Font(None, 36)
        equation = f"f(x) = {self.m:.2f}x + {self.b:.1f}"
        text = font.render(equation, True, WHITE)
        surface.blit(text, (10, 10))

class OscillatingQuadratic(ScreenSaver):
    def __init__(self):
        super().__init__("Oscillating Quadratic", 8000)
        self.a = random.uniform(-0.01, 0.01)
        self.b = random.uniform(-2, 2)
        self.c = random.uniform(-50, 50)
        self.a_change = random.uniform(-0.001, 0.001)
        self.b_change = random.uniform(-0.01, 0.01)
        self.c_change = random.uniform(-0.5, 0.5)
        self.change_counter = 0
        self.colors = self.generate_colors()

    def update(self):
        self.change_counter += 1
        if self.change_counter >= 90:  # Reduced from 45 to 90 for less sporadic changes
            self.a_change = random.uniform(-0.001, 0.001)
            self.b_change = random.uniform(-0.01, 0.01)
            self.c_change = random.uniform(-0.5, 0.5)
            self.change_counter = 0
        
        self.a += self.a_change
        self.b += self.b_change
        self.c += self.c_change
        
        # Bounce off limits
        if self.a < -0.02 or self.a > 0.02:
            self.a_change *= -1
        if self.b < -3 or self.b > 3:
            self.b_change *= -1
        if self.c < -100 or self.c > 100:
            self.c_change *= -1

    def get_equation(self):
        return f"f(x) = {self.a:.3f}x² + {self.b:.2f}x + {self.c:.1f}"

    def draw(self, surface):
        # Draw coordinate grid
        for x in range(0, SCREEN_WIDTH, 50):
            pygame.draw.line(surface, DARK_GRAY, (x, 0), (x, SCREEN_HEIGHT), 1)
        for y in range(0, SCREEN_HEIGHT, 50):
            pygame.draw.line(surface, DARK_GRAY, (0, y), (SCREEN_WIDTH, y), 1)
        
        # Draw quadratic function
        points = []
        for x in range(0, SCREEN_WIDTH):
            y = SCREEN_HEIGHT // 2 - int(self.a * x * x + self.b * x + self.c)
            if 0 <= y < SCREEN_HEIGHT:
                points.append((x, y))
        
        if len(points) > 1:
            pygame.draw.lines(surface, self.colors[0], False, points, 3)
        
        # Draw equation
        font = pygame.font.Font(None, 36)
        equation = f"f(x) = {self.a:.3f}x² + {self.b:.2f}x + {self.c:.1f}"
        text = font.render(equation, True, WHITE)
        surface.blit(text, (10, 10))

class CubicFunctionMorph(ScreenSaver):
    def __init__(self):
        super().__init__("Cubic Function Morph", 8000)
        self.a = random.uniform(-0.0001, 0.0001)
        self.b = random.uniform(-0.01, 0.01)
        self.c = random.uniform(-0.5, 0.5)
        self.d = random.uniform(-25, 25)
        self.a_change = random.uniform(-0.00001, 0.00001)
        self.b_change = random.uniform(-0.001, 0.001)
        self.c_change = random.uniform(-0.01, 0.01)
        self.d_change = random.uniform(-0.2, 0.2)
        self.change_counter = 0
        self.colors = self.generate_colors()

    def update(self):
        self.change_counter += 1
        if self.change_counter >= 80:  # Reduced from 40 to 80 for less sporadic changes
            self.a_change = random.uniform(-0.00001, 0.00001)
            self.b_change = random.uniform(-0.001, 0.001)
            self.c_change = random.uniform(-0.01, 0.01)
            self.d_change = random.uniform(-0.2, 0.2)
            self.change_counter = 0
        
        self.a += self.a_change
        self.b += self.b_change
        self.c += self.c_change
        self.d += self.d_change
        
        # Bounce off limits
        if self.a < -0.0002 or self.a > 0.0002:
            self.a_change *= -1
        if self.b < -0.02 or self.b > 0.02:
            self.b_change *= -1
        if self.c < -1 or self.c > 1:
            self.c_change *= -1
        if self.d < -50 or self.d > 50:
            self.d_change *= -1

    def get_equation(self):
        return f"f(x) = {self.a:.5f}x³ + {self.b:.3f}x² + {self.c:.2f}x + {self.d:.1f}"

    def draw(self, surface):
        # Draw coordinate grid
        for x in range(0, SCREEN_WIDTH, 50):
            pygame.draw.line(surface, DARK_GRAY, (x, 0), (x, SCREEN_HEIGHT), 1)
        for y in range(0, SCREEN_HEIGHT, 50):
            pygame.draw.line(surface, DARK_GRAY, (0, y), (SCREEN_WIDTH, y), 1)
        
        # Draw cubic function
        points = []
        for x in range(0, SCREEN_WIDTH):
            y = SCREEN_HEIGHT // 2 - int(self.a * x * x * x + self.b * x * x + self.c * x + self.d)
            if 0 <= y < SCREEN_HEIGHT:
                points.append((x, y))
        
        if len(points) > 1:
            pygame.draw.lines(surface, self.colors[0], False, points, 3)
        
        # Draw equation
        font = pygame.font.Font(None, 36)
        equation = f"f(x) = {self.a:.5f}x³ + {self.b:.3f}x² + {self.c:.2f}x + {self.d:.1f}"
        text = font.render(equation, True, WHITE)
        surface.blit(text, (10, 10))

class TrigonometricFunctionWave(ScreenSaver):
    def __init__(self):
        super().__init__("Trigonometric Function Wave", 8000)
        self.amplitude = random.uniform(20, 80)
        self.frequency = random.uniform(0.01, 0.05)
        self.phase = random.uniform(0, 2 * math.pi)
        self.vertical_shift = random.uniform(-50, 50)
        self.amplitude_change = random.uniform(-0.5, 0.5)
        self.frequency_change = random.uniform(-0.001, 0.001)
        self.phase_change = random.uniform(-0.02, 0.02)
        self.vertical_shift_change = random.uniform(-0.5, 0.5)
        self.change_counter = 0
        self.colors = self.generate_colors()

    def update(self):
        self.change_counter += 1
        if self.change_counter >= 100:  # Reduced from 50 to 100 for less sporadic changes
            self.amplitude_change = random.uniform(-0.5, 0.5)
            self.frequency_change = random.uniform(-0.001, 0.001)
            self.phase_change = random.uniform(-0.02, 0.02)
            self.vertical_shift_change = random.uniform(-0.5, 0.5)
            self.change_counter = 0
        
        self.amplitude += self.amplitude_change
        self.frequency += self.frequency_change
        self.phase += self.phase_change
        self.vertical_shift += self.vertical_shift_change
        
        # Bounce off limits
        if self.amplitude < 10 or self.amplitude > 100:
            self.amplitude_change *= -1
        if self.frequency < 0.005 or self.frequency > 0.1:
            self.frequency_change *= -1
        if self.vertical_shift < -100 or self.vertical_shift > 100:
            self.vertical_shift_change *= -1

    def get_equation(self):
        return f"f(x) = {self.amplitude:.1f}sin({self.frequency:.3f}x + {self.phase:.2f}) + {self.vertical_shift:.1f}"

    def draw(self, surface):
        # Draw coordinate grid
        for x in range(0, SCREEN_WIDTH, 50):
            pygame.draw.line(surface, DARK_GRAY, (x, 0), (x, SCREEN_HEIGHT), 1)
        for y in range(0, SCREEN_HEIGHT, 50):
            pygame.draw.line(surface, DARK_GRAY, (0, y), (SCREEN_WIDTH, y), 1)
        
        # Draw trigonometric function
        points = []
        for x in range(0, SCREEN_WIDTH):
            y = SCREEN_HEIGHT // 2 - int(self.amplitude * math.sin(self.frequency * x + self.phase) + self.vertical_shift)
            if 0 <= y < SCREEN_HEIGHT:
                points.append((x, y))
        
        if len(points) > 1:
            pygame.draw.lines(surface, self.colors[0], False, points, 3)
        
        # Draw equation
        font = pygame.font.Font(None, 36)
        equation = f"f(x) = {self.amplitude:.1f}sin({self.frequency:.3f}x + {self.phase:.2f}) + {self.vertical_shift:.1f}"
        text = font.render(equation, True, WHITE)
        surface.blit(text, (10, 10))

class ExponentialGrowthDecay(ScreenSaver):
    def __init__(self):
        super().__init__("Exponential Growth/Decay", 8000)
        self.base = random.uniform(1.1, 2.0)
        self.coefficient = random.uniform(0.5, 2.0)
        self.vertical_shift = random.uniform(-50, 50)
        self.base_change = random.uniform(-0.01, 0.01)
        self.coefficient_change = random.uniform(-0.02, 0.02)
        self.vertical_shift_change = random.uniform(-0.5, 0.5)
        self.change_counter = 0
        self.colors = self.generate_colors()

    def update(self):
        self.change_counter += 1
        if self.change_counter >= 110:  # Reduced from 55 to 110 for less sporadic changes
            self.base_change = random.uniform(-0.01, 0.01)
            self.coefficient_change = random.uniform(-0.02, 0.02)
            self.vertical_shift_change = random.uniform(-0.5, 0.5)
            self.change_counter = 0
        
        self.base += self.base_change
        self.coefficient += self.coefficient_change
        self.vertical_shift += self.vertical_shift_change
        
        # Bounce off limits
        if self.base < 1.05 or self.base > 3.0:
            self.base_change *= -1
        if self.coefficient < 0.1 or self.coefficient > 5.0:
            self.coefficient_change *= -1
        if self.vertical_shift < -100 or self.vertical_shift > 100:
            self.vertical_shift_change *= -1

    def get_equation(self):
        return f"f(x) = {self.coefficient:.2f} * {self.base:.2f}^x + {self.vertical_shift:.1f}"

    def draw(self, surface):
        # Draw coordinate grid
        for x in range(0, SCREEN_WIDTH, 50):
            pygame.draw.line(surface, DARK_GRAY, (x, 0), (x, SCREEN_WIDTH), 1)
        for y in range(0, SCREEN_HEIGHT, 50):
            pygame.draw.line(surface, DARK_GRAY, (0, y), (SCREEN_WIDTH, y), 1)
        
        # Draw exponential function
        points = []
        for x in range(0, SCREEN_WIDTH):
            try:
                y = SCREEN_HEIGHT // 2 - int(self.coefficient * (self.base ** (x / 100)) + self.vertical_shift)
                if 0 <= y < SCREEN_HEIGHT:
                    points.append((x, y))
            except (OverflowError, ValueError):
                continue
        
        if len(points) > 1:
            pygame.draw.lines(surface, self.colors[0], False, points, 3)
        
        # Draw equation
        font = pygame.font.Font(None, 36)
        equation = f"f(x) = {self.coefficient:.2f} * {self.base:.2f}^x + {self.vertical_shift:.1f}"
        text = font.render(equation, True, WHITE)
        surface.blit(text, (10, 10))

class LogarithmicFunction(ScreenSaver):
    def __init__(self):
        super().__init__("Logarithmic Function", 8000)
        self.coefficient = random.uniform(0.5, 2.0)
        self.base = random.uniform(1.5, 3.0)
        self.vertical_shift = random.uniform(-50, 50)
        self.coefficient_change = random.uniform(-0.02, 0.02)
        self.base_change = random.uniform(-0.01, 0.01)
        self.vertical_shift_change = random.uniform(-1, 1)
        self.change_counter = 0
        self.colors = self.generate_colors()

    def update(self):
        self.change_counter += 1
        if self.change_counter >= 120:  # Reduced from 60 to 120 for less sporadic changes
            self.coefficient_change = random.uniform(-0.02, 0.02)
            self.base_change = random.uniform(-0.01, 0.01)
            self.vertical_shift_change = random.uniform(-1, 1)
            self.change_counter = 0
        
        self.coefficient += self.coefficient_change
        self.base += self.base_change
        self.vertical_shift += self.vertical_shift_change
        
        # Bounce off limits
        if self.coefficient < 0.1 or self.coefficient > 5.0:
            self.coefficient_change *= -1
        if self.base < 1.1 or self.base > 5.0:
            self.base_change *= -1
        if self.vertical_shift < -100 or self.vertical_shift > 100:
            self.vertical_shift_change *= -1

    def get_equation(self):
        return f"f(x) = {self.coefficient:.2f} * log_{self.base:.2f}(x) + {self.vertical_shift:.1f}"

    def draw(self, surface):
        # Draw coordinate grid
        for x in range(0, SCREEN_WIDTH, 50):
            pygame.draw.line(surface, DARK_GRAY, (x, 0), (x, SCREEN_HEIGHT), 1)
        for y in range(0, SCREEN_HEIGHT, 50):
            pygame.draw.line(surface, DARK_GRAY, (0, y), (SCREEN_WIDTH, y), 1)
        
        # Draw logarithmic function
        points = []
        for x in range(0, SCREEN_WIDTH):
            if x > 0:  # Avoid log(0)
                try:
                    y = SCREEN_HEIGHT // 2 - int(self.coefficient * math.log(x / 100, self.base) + self.vertical_shift)
                    if 0 <= y < SCREEN_HEIGHT:
                        points.append((x, y))
                except (ValueError, ZeroDivisionError):
                    continue
        
        if len(points) > 1:
            pygame.draw.lines(surface, self.colors[0], False, points, 3)
        
        # Draw equation
        font = pygame.font.Font(None, 36)
        equation = f"f(x) = {self.coefficient:.2f} * log_{self.base:.2f}(x) + {self.vertical_shift:.1f}"
        text = font.render(equation, True, WHITE)
        surface.blit(text, (10, 10))

# Additional Screen Savers
class ColorFlowGrid(ScreenSaver):
    def __init__(self):
        super().__init__("Color Flow Grid", 6000)
        self.grid_size = 20
        self.cells = []
        self.time = 0
        self.generate_grid()
        
    def generate_grid(self):
        self.cells = []
        for x in range(0, SCREEN_WIDTH, self.grid_size):
            for y in range(0, SCREEN_HEIGHT, self.grid_size):
                self.cells.append({
                    'x': x, 'y': y,
                    'color': (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)),
                    'phase': random.uniform(0, 2 * math.pi)
                })
    
    def update(self):
        self.time += 0.05
        for cell in self.cells:
            # Create flowing color effect
            r = int(128 + 127 * math.sin(self.time + cell['phase']))
            g = int(128 + 127 * math.sin(self.time + cell['phase'] + 2 * math.pi / 3))
            b = int(128 + 127 * math.sin(self.time + cell['phase'] + 4 * math.pi / 3))
            cell['color'] = (r, g, b)
    
    def draw(self, surface):
        for cell in self.cells:
            pygame.draw.rect(surface, cell['color'], 
                           (cell['x'], cell['y'], self.grid_size, self.grid_size))

class FloatingBubbles(ScreenSaver):
    def __init__(self):
        super().__init__("Floating Bubbles", 7000)
        self.bubbles = []
        self.generate_bubbles()
        
    def generate_bubbles(self):
        self.bubbles = []
        for _ in range(15):
            self.bubbles.append({
                'x': random.randint(0, SCREEN_WIDTH),
                'y': random.randint(0, SCREEN_HEIGHT),
                'size': random.randint(20, 60),
                'speed': random.uniform(0.5, 2.0),
                'color': (random.randint(100, 255), random.randint(100, 255), random.randint(100, 255)),
                'alpha': random.randint(100, 200)
            })
    
    def update(self):
        for bubble in self.bubbles:
            bubble['y'] -= bubble['speed']
            if bubble['y'] + bubble['size'] < 0:
                bubble['y'] = SCREEN_HEIGHT + bubble['size']
                bubble['x'] = random.randint(0, SCREEN_WIDTH)
    
    def draw(self, surface):
        for bubble in self.bubbles:
            # Create a surface with alpha for transparency
            bubble_surface = pygame.Surface((bubble['size'] * 2, bubble['size'] * 2), pygame.SRCALPHA)
            pygame.draw.circle(bubble_surface, (*bubble['color'], bubble['alpha']), 
                             (bubble['size'], bubble['size']), bubble['size'])
            surface.blit(bubble_surface, (bubble['x'] - bubble['size'], bubble['y'] - bubble['size']))

class KaleidoscopeTunnel(ScreenSaver):
    def __init__(self):
        super().__init__("Kaleidoscope Tunnel", 8000)
        self.angle = 0
        self.zoom = 0
        self.colors = self.generate_colors()
        
    def update(self):
        self.angle += 2
        self.zoom += 0.5
        
    def draw(self, surface):
        center_x, center_y = SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2
        
        for i in range(8):  # 8-fold symmetry
            angle = self.angle + i * 45
            for j in range(20):
                radius = 50 + j * 20 + self.zoom
                x = center_x + int(radius * math.cos(math.radians(angle)))
                y = center_y + int(radius * math.sin(math.radians(angle)))
                size = max(1, 20 - j)
                color = self.colors[j % len(self.colors)]
                pygame.draw.circle(surface, color, (x, y), size)

class BezierBlossom(ScreenSaver):
    def __init__(self):
        super().__init__("Bezier Blossom", 6000)
        self.points = []
        self.time = 0
        self.generate_points()
        
    def generate_points(self):
        self.points = []
        center_x, center_y = SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2
        for i in range(8):
            angle = i * 45
            radius = random.randint(100, 200)
            x = center_x + int(radius * math.cos(math.radians(angle)))
            y = center_y + int(radius * math.sin(math.radians(angle)))
            self.points.append((x, y))
    
    def bezier_curve(self, points, t):
        if len(points) == 1:
            return points[0]
        new_points = []
        for i in range(len(points) - 1):
            x = points[i][0] + t * (points[i + 1][0] - points[i][0])
            y = points[i][1] + t * (points[i + 1][1] - points[i][1])
            new_points.append((x, y))
        return self.bezier_curve(new_points, t)
    
    def update(self):
        self.time += 0.02
        if self.time >= 1:
            self.time = 0
            self.generate_points()
    
    def draw(self, surface):
        # Draw Bezier curve
        curve_points = []
        for t in range(0, 100, 2):
            t_val = t / 100.0
            point = self.bezier_curve(self.points, t_val)
            curve_points.append(point)
        
        if len(curve_points) > 1:
            pygame.draw.lines(surface, self.colors[0], False, curve_points, 3)
        
        # Draw control points
        for point in self.points:
            pygame.draw.circle(surface, WHITE, point, 5)

class StarfieldWarpDrive(ScreenSaver):
    def __init__(self):
        super().__init__("Starfield Warp Drive", 7000)
        self.stars = []
        self.generate_stars()
        
    def generate_stars(self):
        self.stars = []
        for _ in range(100):
            self.stars.append({
                'x': random.randint(0, SCREEN_WIDTH),
                'y': random.randint(0, SCREEN_HEIGHT),
                'z': random.randint(1, 100),
                'speed': random.uniform(1, 5)
            })
    
    def update(self):
        for star in self.stars:
            star['z'] -= star['speed']
            if star['z'] <= 0:
                star['z'] = 100
                star['x'] = random.randint(0, SCREEN_WIDTH)
                star['y'] = random.randint(0, SCREEN_HEIGHT)
    
    def draw(self, surface):
        center_x, center_y = SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2
        
        for star in self.stars:
            # Project 3D to 2D
            if star['z'] > 0:
                x = center_x + (star['x'] - center_x) / star['z']
                y = center_y + (star['y'] - center_y) / star['z']
                
                if 0 <= x < SCREEN_WIDTH and 0 <= y < SCREEN_HEIGHT:
                    size = max(1, int(10 / star['z']))
                    brightness = min(255, int(255 / star['z']))
                    color = (brightness, brightness, brightness)
                    pygame.draw.circle(surface, color, (int(x), int(y)), size)

class LissajousOrbitDance(ScreenSaver):
    def __init__(self):
        super().__init__("Lissajous Orbit Dance", 6000)
        self.time = 0
        self.colors = self.generate_colors()
        
    def update(self):
        self.time += 0.05
        
    def draw(self, surface):
        center_x, center_y = SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2
        
        # Draw multiple Lissajous curves
        for i in range(3):
            a = 100 + i * 50
            b = 100 + i * 30
            freq_x = 2 + i
            freq_y = 3 + i
            phase = self.time + i * math.pi / 3
            
            points = []
            for t in range(0, 628, 5):  # 0 to 2π
                t_val = t / 100.0
                x = center_x + int(a * math.sin(freq_x * t_val + phase))
                y = center_y + int(b * math.sin(freq_y * t_val))
                points.append((x, y))
            
            if len(points) > 1:
                pygame.draw.lines(surface, self.colors[i % len(self.colors)], False, points, 2)

class ParticleFireworks(ScreenSaver):
    def __init__(self):
        super().__init__("Particle Fireworks", 5000)
        self.particles = []
        self.explosions = []
        self.time = 0
        
    def create_explosion(self, x, y):
        explosion = {
            'x': x, 'y': y,
            'particles': [],
            'age': 0
        }
        for _ in range(30):
            angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(2, 8)
            explosion['particles'].append({
                'dx': math.cos(angle) * speed,
                'dy': math.sin(angle) * speed,
                'x': x, 'y': y,
                'color': self.colors[random.randint(0, len(self.colors) - 1)]
            })
        self.explosions.append(explosion)
    
    def update(self):
        self.time += 1
        
        # Create new explosions
        if self.time % 60 == 0:
            self.create_explosion(random.randint(100, SCREEN_WIDTH - 100),
                                random.randint(100, SCREEN_HEIGHT - 100))
        
        # Update explosions
        for explosion in self.explosions[:]:
            explosion['age'] += 1
            for particle in explosion['particles']:
                particle['x'] += particle['dx']
                particle['y'] += particle['dy']
                particle['dy'] += 0.1  # Gravity
            
            # Remove old explosions
            if explosion['age'] > 120:
                self.explosions.remove(explosion)
    
    def draw(self, surface):
        # Draw all particles
        for explosion in self.explosions:
            for particle in explosion['particles']:
                pygame.draw.circle(surface, particle['color'], 
                                 (int(particle['x']), int(particle['y'])), 2)

class MagneticDots(ScreenSaver):
    def __init__(self):
        super().__init__("Magnetic Dots", 7000)
        self.dots = []
        self.generate_dots()
        
    def generate_dots(self):
        self.dots = []
        for _ in range(20):
            self.dots.append({
                'x': random.randint(0, SCREEN_WIDTH),
                'y': random.randint(0, SCREEN_HEIGHT),
                'dx': random.uniform(-2, 2),
                'dy': random.uniform(-2, 2),
                'charge': random.choice([-1, 1]),
                'color': self.colors[random.randint(0, len(self.colors) - 1)]
            })
    
    def update(self):
        for dot in self.dots:
            # Update position
            dot['x'] += dot['dx']
            dot['y'] += dot['dy']
            
            # Bounce off walls
            if dot['x'] <= 0 or dot['x'] >= SCREEN_WIDTH:
                dot['dx'] *= -1
            if dot['y'] <= 0 or dot['y'] >= SCREEN_HEIGHT:
                dot['dy'] *= -1
            
            # Magnetic attraction/repulsion
            for other_dot in self.dots:
                if dot != other_dot:
                    dx = other_dot['x'] - dot['x']
                    dy = other_dot['y'] - dot['y']
                    distance = math.sqrt(dx*dx + dy*dy)
                    if distance > 0 and distance < 100:
                        force = (dot['charge'] * other_dot['charge']) / (distance * distance)
                        dot['dx'] += (dx / distance) * force * 0.1
                        dot['dy'] += (dy / distance) * force * 0.1
    
    def draw(self, surface):
        for dot in self.dots:
            pygame.draw.circle(surface, dot['color'], 
                             (int(dot['x']), int(dot['y'])), 5)

class FractalVines(ScreenSaver):
    def __init__(self):
        super().__init__("Fractal Vines", 8000)
        self.vines = []
        self.time = 0
        self.generate_vines()
        
    def generate_vines(self):
        self.vines = []
        for _ in range(5):
            vine = {
                'x': random.randint(0, SCREEN_WIDTH),
                'y': SCREEN_HEIGHT,
                'segments': [],
                'color': self.colors[random.randint(0, len(self.colors) - 1)]
            }
            self.vines.append(vine)
    
    def grow_vine(self, vine):
        if len(vine['segments']) < 20:
            if len(vine['segments']) == 0:
                x, y = vine['x'], vine['y']
            else:
                x, y = vine['segments'][-1]
            
            angle = random.uniform(-math.pi/4, math.pi/4)
            length = random.randint(10, 30)
            new_x = x + length * math.cos(angle)
            new_y = y - length * math.sin(angle)
            
            if 0 <= new_x < SCREEN_WIDTH and 0 <= new_y < SCREEN_HEIGHT:
                vine['segments'].append((new_x, new_y))
    
    def update(self):
        self.time += 1
        if self.time % 10 == 0:
            for vine in self.vines:
                self.grow_vine(vine)
    
    def draw(self, surface):
        for vine in self.vines:
            if len(vine['segments']) > 1:
                pygame.draw.lines(surface, vine['color'], False, vine['segments'], 3)

class PaintDripCanvas(ScreenSaver):
    def __init__(self):
        super().__init__("Paint Drip Canvas", 6000)
        self.drips = []
        self.time = 0
        
    def create_drip(self):
        drip = {
            'x': random.randint(0, SCREEN_WIDTH),
            'y': 0,
            'speed': random.uniform(1, 3),
            'color': self.colors[random.randint(0, len(self.colors) - 1)],
            'size': random.randint(2, 8)
        }
        self.drips.append(drip)
    
    def update(self):
        self.time += 1
        if self.time % 30 == 0:
            self.create_drip()
        
        for drip in self.drips[:]:
            drip['y'] += drip['speed']
            if drip['y'] > SCREEN_HEIGHT:
                self.drips.remove(drip)
    
    def draw(self, surface):
        for drip in self.drips:
            pygame.draw.circle(surface, drip['color'], 
                             (int(drip['x']), int(drip['y'])), drip['size'])

class SoapFilmInterference(ScreenSaver):
    def __init__(self):
        super().__init__("Soap Film Interference", 7000)
        self.time = 0
        
    def update(self):
        self.time += 0.05
        
    def draw(self, surface):
        for x in range(0, SCREEN_WIDTH, 4):
            for y in range(0, SCREEN_HEIGHT, 4):
                # Create interference pattern
                wave1 = math.sin(x * 0.02 + self.time)
                wave2 = math.sin(y * 0.02 + self.time * 1.5)
                interference = wave1 + wave2
                
                # Convert to color
                intensity = int(128 + 127 * interference)
                color = (intensity, intensity, intensity)
                pygame.draw.rect(surface, color, (x, y, 4, 4))

class MirrorEchoes(ScreenSaver):
    def __init__(self):
        super().__init__("Mirror Echoes", 6000)
        self.particles = []
        self.time = 0
        self.generate_particles()
        
    def generate_particles(self):
        self.particles = []
        for _ in range(10):
            self.particles.append({
                'x': random.randint(0, SCREEN_WIDTH),
                'y': random.randint(0, SCREEN_HEIGHT),
                'dx': random.uniform(-3, 3),
                'dy': random.uniform(-3, 3),
                'color': self.colors[random.randint(0, len(self.colors) - 1)]
            })
    
    def update(self):
        self.time += 1
        for particle in self.particles:
            particle['x'] += particle['dx']
            particle['y'] += particle['dy']
            
            # Bounce off walls
            if particle['x'] <= 0 or particle['x'] >= SCREEN_WIDTH:
                particle['dx'] *= -1
            if particle['y'] <= 0 or particle['y'] >= SCREEN_HEIGHT:
                particle['dy'] *= -1
    
    def draw(self, surface):
        for particle in self.particles:
            # Draw main particle
            pygame.draw.circle(surface, particle['color'], 
                             (int(particle['x']), int(particle['y'])), 5)
            
            # Draw mirror reflections
            for i in range(1, 4):
                alpha = 255 // i
                color = (*particle['color'], alpha)
                pygame.draw.circle(surface, color, 
                                 (int(particle['x'] + i * 20), int(particle['y'])), 3)

class SwarmingParticles(ScreenSaver):
    def __init__(self):
        super().__init__("Swarming Particles", 7000)
        self.particles = []
        self.generate_particles()
        
    def generate_particles(self):
        self.particles = []
        for _ in range(50):
            self.particles.append({
                'x': random.randint(0, SCREEN_WIDTH),
                'y': random.randint(0, SCREEN_HEIGHT),
                'dx': random.uniform(-1, 1),
                'dy': random.uniform(-1, 1),
                'color': self.colors[random.randint(0, len(self.colors) - 1)]
            })
    
    def update(self):
        for particle in self.particles:
            # Update position
            particle['x'] += particle['dx']
            particle['y'] += particle['dy']
            
            # Bounce off walls
            if particle['x'] <= 0 or particle['x'] >= SCREEN_WIDTH:
                particle['dx'] *= -1
            if particle['y'] <= 0 or particle['y'] >= SCREEN_HEIGHT:
                particle['dy'] *= -1
            
            # Swarming behavior - move towards nearby particles
            for other in self.particles:
                if particle != other:
                    dx = other['x'] - particle['x']
                    dy = other['y'] - particle['y']
                    distance = math.sqrt(dx*dx + dy*dy)
                    if distance < 50 and distance > 0:
                        particle['dx'] += (dx / distance) * 0.1
                        particle['dy'] += (dy / distance) * 0.1
    
    def draw(self, surface):
        for particle in self.particles:
            pygame.draw.circle(surface, particle['color'], 
                             (int(particle['x']), int(particle['y'])), 2)

class RandomWalkersWithTrails(ScreenSaver):
    def __init__(self):
        super().__init__("Random Walkers with Trails", 6000)
        self.walkers = []
        self.generate_walkers()
        
    def generate_walkers(self):
        self.walkers = []
        for _ in range(8):
            self.walkers.append({
                'x': random.randint(0, SCREEN_WIDTH),
                'y': random.randint(0, SCREEN_HEIGHT),
                'trail': [],
                'color': self.colors[random.randint(0, len(self.colors) - 1)]
            })
    
    def update(self):
        for walker in self.walkers:
            # Random walk
            walker['x'] += random.randint(-3, 3)
            walker['y'] += random.randint(-3, 3)
            
            # Keep in bounds
            walker['x'] = max(0, min(SCREEN_WIDTH, walker['x']))
            walker['y'] = max(0, min(SCREEN_HEIGHT, walker['y']))
            
            # Add to trail
            walker['trail'].append((walker['x'], walker['y']))
            if len(walker['trail']) > 20:
                walker['trail'].pop(0)
    
    def draw(self, surface):
        for walker in self.walkers:
            # Draw trail
            if len(walker['trail']) > 1:
                pygame.draw.lines(surface, walker['color'], False, walker['trail'], 2)
            
            # Draw current position
            pygame.draw.circle(surface, walker['color'], 
                             (int(walker['x']), int(walker['y'])), 4)

class CollidingBallsWithElasticBounce(ScreenSaver):
    def __init__(self):
        super().__init__("Colliding Balls with Elastic Bounce", 7000)
        self.balls = []
        self.generate_balls()
        
    def generate_balls(self):
        self.balls = []
        for _ in range(15):
            self.balls.append({
                'x': random.randint(50, SCREEN_WIDTH - 50),
                'y': random.randint(50, SCREEN_HEIGHT - 50),
                'dx': random.uniform(-5, 5),
                'dy': random.uniform(-5, 5),
                'radius': random.randint(10, 25),
                'color': self.colors[random.randint(0, len(self.colors) - 1)]
            })
    
    def update(self):
        for ball in self.balls:
            # Update position
            ball['x'] += ball['dx']
            ball['y'] += ball['dy']
            
            # Bounce off walls
            if ball['x'] - ball['radius'] <= 0 or ball['x'] + ball['radius'] >= SCREEN_WIDTH:
                ball['dx'] *= -1
            if ball['y'] - ball['radius'] <= 0 or ball['y'] + ball['radius'] >= SCREEN_HEIGHT:
                ball['dy'] *= -1
            
            # Collision detection with other balls
            for other in self.balls:
                if ball != other:
                    dx = other['x'] - ball['x']
                    dy = other['y'] - ball['y']
                    distance = math.sqrt(dx*dx + dy*dy)
                    min_distance = ball['radius'] + other['radius']
                    
                    if distance < min_distance and distance > 0:
                        # Elastic collision
                        angle = math.atan2(dy, dx)
                        ball['dx'] = -ball['dx']
                        ball['dy'] = -ball['dy']
                        other['dx'] = -other['dx']
                        other['dy'] = -other['dy']
    
    def draw(self, surface):
        for ball in self.balls:
            pygame.draw.circle(surface, ball['color'], 
                             (int(ball['x']), int(ball['y'])), ball['radius'])

class GravityWellAttractors(ScreenSaver):
    def __init__(self):
        super().__init__("Gravity Well Attractors", 7000)
        self.particles = []
        self.wells = []
        self.generate_objects()
        
    def generate_objects(self):
        self.particles = []
        self.wells = []
        
        # Create gravity wells
        for _ in range(3):
            self.wells.append({
                'x': random.randint(100, SCREEN_WIDTH - 100),
                'y': random.randint(100, SCREEN_HEIGHT - 100),
                'strength': random.uniform(0.5, 2.0),
                'color': self.colors[random.randint(0, len(self.colors) - 1)]
            })
        
        # Create particles
        for _ in range(30):
            self.particles.append({
                'x': random.randint(0, SCREEN_WIDTH),
                'y': random.randint(0, SCREEN_HEIGHT),
                'dx': random.uniform(-2, 2),
                'dy': random.uniform(-2, 2),
                'color': self.colors[random.randint(0, len(self.colors) - 1)]
            })
    
    def update(self):
        for particle in self.particles:
            # Apply gravity from wells
            for well in self.wells:
                dx = well['x'] - particle['x']
                dy = well['y'] - particle['y']
                distance = math.sqrt(dx*dx + dy*dy)
                if distance > 0:
                    force = well['strength'] / (distance * distance)
                    particle['dx'] += (dx / distance) * force
                    particle['dy'] += (dy / distance) * force
            
            # Update position
            particle['x'] += particle['dx']
            particle['y'] += particle['dy']
            
            # Bounce off walls
            if particle['x'] <= 0 or particle['x'] >= SCREEN_WIDTH:
                particle['dx'] *= -1
            if particle['y'] <= 0 or particle['y'] >= SCREEN_HEIGHT:
                particle['dy'] *= -1
    
    def draw(self, surface):
        # Draw gravity wells
        for well in self.wells:
            pygame.draw.circle(surface, well['color'], 
                             (int(well['x']), int(well['y'])), 15)
        
        # Draw particles
        for particle in self.particles:
            pygame.draw.circle(surface, particle['color'], 
                             (int(particle['x']), int(particle['y'])), 3)

class FireflyMotion(ScreenSaver):
    def __init__(self):
        super().__init__("Firefly Motion (Random Blinking)", 6000)
        self.fireflies = []
        self.generate_fireflies()
        
    def generate_fireflies(self):
        self.fireflies = []
        for _ in range(25):
            self.fireflies.append({
                'x': random.randint(0, SCREEN_WIDTH),
                'y': random.randint(0, SCREEN_HEIGHT),
                'dx': random.uniform(-1, 1),
                'dy': random.uniform(-1, 1),
                'blink_timer': random.randint(0, 60),
                'blink_duration': random.randint(10, 30),
                'color': self.colors[random.randint(0, len(self.colors) - 1)]
            })
    
    def update(self):
        for firefly in self.fireflies:
            # Update position
            firefly['x'] += firefly['dx']
            firefly['y'] += firefly['dy']
            
            # Bounce off walls
            if firefly['x'] <= 0 or firefly['x'] >= SCREEN_WIDTH:
                firefly['dx'] *= -1
            if firefly['y'] <= 0 or firefly['y'] >= SCREEN_HEIGHT:
                firefly['dy'] *= -1
            
            # Update blinking
            firefly['blink_timer'] += 1
            if firefly['blink_timer'] >= firefly['blink_duration']:
                firefly['blink_timer'] = 0
                firefly['blink_duration'] = random.randint(10, 30)
    
    def draw(self, surface):
        for firefly in self.fireflies:
            # Only draw if blinking
            if firefly['blink_timer'] < firefly['blink_duration'] // 2:
                pygame.draw.circle(surface, firefly['color'], 
                                 (int(firefly['x']), int(firefly['y'])), 3)

class SpiralParticleFountain(ScreenSaver):
    def __init__(self):
        super().__init__("Spiral Particle Fountain", 7000)
        self.particles = []
        self.time = 0
        
    def create_particle(self):
        angle = self.time * 0.1
        radius = 50
        x = SCREEN_WIDTH // 2 + int(radius * math.cos(angle))
        y = SCREEN_HEIGHT // 2 + int(radius * math.sin(angle))
        
        particle = {
            'x': x, 'y': y,
            'dx': random.uniform(-2, 2),
            'dy': random.uniform(-5, -1),
            'life': 100,
            'color': self.colors[random.randint(0, len(self.colors) - 1)]
        }
        self.particles.append(particle)
    
    def update(self):
        self.time += 1
        if self.time % 5 == 0:
            self.create_particle()
        
        for particle in self.particles[:]:
            particle['x'] += particle['dx']
            particle['y'] += particle['dy']
            particle['dy'] += 0.1  # Gravity
            particle['life'] -= 1
            
            if particle['life'] <= 0 or particle['y'] > SCREEN_HEIGHT:
                self.particles.remove(particle)
    
    def draw(self, surface):
        for particle in self.particles:
            alpha = int(255 * (particle['life'] / 100))
            color = (*particle['color'], alpha)
            pygame.draw.circle(surface, color, 
                             (int(particle['x']), int(particle['y'])), 3)

class DustCloudDrift(ScreenSaver):
    def __init__(self):
        super().__init__("Dust Cloud Drift", 6000)
        self.dust = []
        self.generate_dust()
        
    def generate_dust(self):
        self.dust = []
        for _ in range(100):
            self.dust.append({
                'x': random.randint(0, SCREEN_WIDTH),
                'y': random.randint(0, SCREEN_HEIGHT),
                'dx': random.uniform(-0.5, 0.5),
                'dy': random.uniform(-0.5, 0.5),
                'size': random.randint(1, 3),
                'color': (random.randint(150, 255), random.randint(150, 255), random.randint(150, 255))
            })
    
    def update(self):
        for particle in self.dust:
            particle['x'] += particle['dx']
            particle['y'] += particle['dy']
            
            # Wrap around screen
            if particle['x'] < 0:
                particle['x'] = SCREEN_WIDTH
            elif particle['x'] > SCREEN_WIDTH:
                particle['x'] = 0
            if particle['y'] < 0:
                particle['y'] = SCREEN_HEIGHT
            elif particle['y'] > SCREEN_HEIGHT:
                particle['y'] = 0
    
    def draw(self, surface):
        for particle in self.dust:
            pygame.draw.circle(surface, particle['color'], 
                             (int(particle['x']), int(particle['y'])), particle['size'])

class BoidsFlockingSimulation(ScreenSaver):
    def __init__(self):
        super().__init__("Boids (Flocking Simulation)", 7000)
        self.boids = []
        self.generate_boids()
        
    def generate_boids(self):
        self.boids = []
        for _ in range(30):
            self.boids.append({
                'x': random.randint(0, SCREEN_WIDTH),
                'y': random.randint(0, SCREEN_HEIGHT),
                'dx': random.uniform(-2, 2),
                'dy': random.uniform(-2, 2),
                'color': self.colors[random.randint(0, len(self.colors) - 1)]
            })
    
    def update(self):
        for boid in self.boids:
            # Flocking behavior
            separation = [0, 0]
            alignment = [0, 0]
            cohesion = [0, 0]
            neighbors = 0
            
            for other in self.boids:
                if boid != other:
                    dx = other['x'] - boid['x']
                    dy = other['y'] - boid['y']
                    distance = math.sqrt(dx*dx + dy*dy)
                    
                    if distance < 50 and distance > 0:
                        neighbors += 1
                        # Separation
                        separation[0] -= dx / distance
                        separation[1] -= dy / distance
                        # Alignment
                        alignment[0] += other['dx']
                        alignment[1] += other['dy']
                        # Cohesion
                        cohesion[0] += other['x']
                        cohesion[1] += other['y']
            
            if neighbors > 0:
                # Apply flocking rules
                boid['dx'] += separation[0] * 0.05
                boid['dy'] += separation[1] * 0.05
                boid['dx'] += alignment[0] / neighbors * 0.05
                boid['dy'] += alignment[1] / neighbors * 0.05
                boid['dx'] += (cohesion[0] / neighbors - boid['x']) * 0.05
                boid['dy'] += (cohesion[1] / neighbors - boid['y']) * 0.05
            
            # Update position
            boid['x'] += boid['dx']
            boid['y'] += boid['dy']
            
            # Wrap around screen
            if boid['x'] < 0:
                boid['x'] = SCREEN_WIDTH
            elif boid['x'] > SCREEN_WIDTH:
                boid['x'] = 0
            if boid['y'] < 0:
                boid['y'] = SCREEN_HEIGHT
            elif boid['y'] > SCREEN_HEIGHT:
                boid['y'] = 0
    
    def draw(self, surface):
        for boid in self.boids:
            # Draw boid as a triangle pointing in direction of movement
            angle = math.atan2(boid['dy'], boid['dx'])
            points = [
                (boid['x'] + 10 * math.cos(angle), boid['y'] + 10 * math.sin(angle)),
                (boid['x'] + 5 * math.cos(angle + 2.6), boid['y'] + 5 * math.sin(angle + 2.6)),
                (boid['x'] + 5 * math.cos(angle - 2.6), boid['y'] + 5 * math.sin(angle - 2.6))
            ]
            pygame.draw.polygon(surface, boid['color'], points)

class BrownianMotionDots(ScreenSaver):
    def __init__(self):
        super().__init__("Brownian Motion Dots", 6000)
        self.dots = []
        self.generate_dots()
        
    def generate_dots(self):
        self.dots = []
        for _ in range(50):
            self.dots.append({
                'x': random.randint(0, SCREEN_WIDTH),
                'y': random.randint(0, SCREEN_HEIGHT),
                'color': self.colors[random.randint(0, len(self.colors) - 1)]
            })
    
    def update(self):
        for dot in self.dots:
            # Random walk (Brownian motion)
            dot['x'] += random.randint(-2, 2)
            dot['y'] += random.randint(-2, 2)
            
            # Keep in bounds
            dot['x'] = max(0, min(SCREEN_WIDTH, dot['x']))
            dot['y'] = max(0, min(SCREEN_HEIGHT, dot['y']))
    
    def draw(self, surface):
        for dot in self.dots:
            pygame.draw.circle(surface, dot['color'], 
                             (int(dot['x']), int(dot['y'])), 3)

class OrbitingMoons(ScreenSaver):
    def __init__(self):
        super().__init__("Orbiting Moons", 7000)
        self.moons = []
        self.time = 0
        self.generate_moons()
        
    def generate_moons(self):
        self.moons = []
        center_x, center_y = SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2
        
        for i in range(5):
            self.moons.append({
                'angle': i * 2 * math.pi / 5,
                'radius': 100 + i * 30,
                'speed': 0.02 + i * 0.005,
                'size': 10 + i * 2,
                'color': self.colors[i % len(self.colors)]
            })
    
    def update(self):
        self.time += 1
        for moon in self.moons:
            moon['angle'] += moon['speed']
    
    def draw(self, surface):
        center_x, center_y = SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2
        
        # Draw central planet
        pygame.draw.circle(surface, WHITE, (center_x, center_y), 20)
        
        # Draw moons
        for moon in self.moons:
            x = center_x + int(moon['radius'] * math.cos(moon['angle']))
            y = center_y + int(moon['radius'] * math.sin(moon['angle']))
            pygame.draw.circle(surface, moon['color'], (x, y), moon['size'])

class TornadoFunnel(ScreenSaver):
    def __init__(self):
        super().__init__("Tornado Funnel", 6000)
        self.particles = []
        self.time = 0
        
    def create_particle(self):
        angle = random.uniform(0, 2 * math.pi)
        radius = random.randint(50, 200)
        x = SCREEN_WIDTH // 2 + int(radius * math.cos(angle))
        y = SCREEN_HEIGHT // 2 + int(radius * math.sin(angle))
        
        particle = {
            'x': x, 'y': y,
            'angle': angle,
            'radius': radius,
            'speed': random.uniform(0.05, 0.15),
            'color': self.colors[random.randint(0, len(self.colors) - 1)]
        }
        self.particles.append(particle)
    
    def update(self):
        self.time += 1
        if self.time % 10 == 0:
            self.create_particle()
        
        for particle in self.particles[:]:
            particle['angle'] += particle['speed']
            particle['radius'] -= 1
            
            particle['x'] = SCREEN_WIDTH // 2 + int(particle['radius'] * math.cos(particle['angle']))
            particle['y'] = SCREEN_HEIGHT // 2 + int(particle['radius'] * math.sin(particle['angle']))
            
            if particle['radius'] <= 0:
                self.particles.remove(particle)
    
    def draw(self, surface):
        for particle in self.particles:
            pygame.draw.circle(surface, particle['color'], 
                             (int(particle['x']), int(particle['y'])), 3)

class DrippingInk(ScreenSaver):
    def __init__(self):
        super().__init__("Dripping Ink", 6000)
        self.drops = []
        self.time = 0
        
    def create_drop(self):
        drop = {
            'x': random.randint(0, SCREEN_WIDTH),
            'y': 0,
            'size': random.randint(5, 15),
            'speed': random.uniform(2, 5),
            'color': self.colors[random.randint(0, len(self.colors) - 1)]
        }
        self.drops.append(drop)
    
    def update(self):
        self.time += 1
        if self.time % 30 == 0:
            self.create_drop()
        
        for drop in self.drops[:]:
            drop['y'] += drop['speed']
            if drop['y'] > SCREEN_HEIGHT:
                self.drops.remove(drop)
    
    def draw(self, surface):
        for drop in self.drops:
            pygame.draw.circle(surface, drop['color'], 
                             (int(drop['x']), int(drop['y'])), drop['size'])

class ParticleTrailsThatFormShapes(ScreenSaver):
    def __init__(self):
        super().__init__("Particle Trails that Form Shapes", 7000)
        self.particles = []
        self.time = 0
        self.generate_particles()
        
    def generate_particles(self):
        self.particles = []
        for _ in range(20):
            self.particles.append({
                'x': random.randint(0, SCREEN_WIDTH),
                'y': random.randint(0, SCREEN_HEIGHT),
                'dx': random.uniform(-2, 2),
                'dy': random.uniform(-2, 2),
                'trail': [],
                'color': self.colors[random.randint(0, len(self.colors) - 1)]
            })
    
    def update(self):
        self.time += 1
        for particle in self.particles:
            # Update position
            particle['x'] += particle['dx']
            particle['y'] += particle['dy']
            
            # Bounce off walls
            if particle['x'] <= 0 or particle['x'] >= SCREEN_WIDTH:
                particle['dx'] *= -1
            if particle['y'] <= 0 or particle['y'] >= SCREEN_HEIGHT:
                particle['dy'] *= -1
            
            # Add to trail
            particle['trail'].append((particle['x'], particle['y']))
            if len(particle['trail']) > 50:
                particle['trail'].pop(0)
    
    def draw(self, surface):
        for particle in self.particles:
            # Draw trail
            if len(particle['trail']) > 1:
                pygame.draw.lines(surface, particle['color'], False, particle['trail'], 2)
            
            # Draw current position
            pygame.draw.circle(surface, particle['color'], 
                             (int(particle['x']), int(particle['y'])), 4)

class PixelRain(ScreenSaver):
    def __init__(self):
        super().__init__("Pixel Rain (Color Matrix)", 6000)
        self.pixels = []
        self.generate_pixels()
        
    def generate_pixels(self):
        self.pixels = []
        for x in range(0, SCREEN_WIDTH, 20):
            for y in range(0, SCREEN_HEIGHT, 20):
                self.pixels.append({
                    'x': x, 'y': y,
                    'speed': random.uniform(1, 3),
                    'color': self.colors[random.randint(0, len(self.colors) - 1)]
                })
    
    def update(self):
        for pixel in self.pixels:
            pixel['y'] += pixel['speed']
            if pixel['y'] > SCREEN_HEIGHT:
                pixel['y'] = -20
    
    def draw(self, surface):
        for pixel in self.pixels:
            pygame.draw.rect(surface, pixel['color'], 
                           (int(pixel['x']), int(pixel['y']), 18, 18))

class FloatingOrbsWithGlow(ScreenSaver):
    def __init__(self):
        super().__init__("Floating Orbs with Glow", 7000)
        self.orbs = []
        self.generate_orbs()
        
    def generate_orbs(self):
        self.orbs = []
        for _ in range(15):
            self.orbs.append({
                'x': random.randint(0, SCREEN_WIDTH),
                'y': random.randint(0, SCREEN_HEIGHT),
                'dx': random.uniform(-1, 1),
                'dy': random.uniform(-1, 1),
                'size': random.randint(20, 40),
                'glow_size': random.randint(40, 80),
                'color': self.colors[random.randint(0, len(self.colors) - 1)]
            })
    
    def update(self):
        for orb in self.orbs:
            orb['x'] += orb['dx']
            orb['y'] += orb['dy']
            
            # Bounce off walls
            if orb['x'] - orb['size'] <= 0 or orb['x'] + orb['size'] >= SCREEN_WIDTH:
                orb['dx'] *= -1
            if orb['y'] - orb['size'] <= 0 or orb['y'] + orb['size'] >= SCREEN_HEIGHT:
                orb['dy'] *= -1
    
    def draw(self, surface):
        for orb in self.orbs:
            # Draw glow
            for i in range(3):
                glow_size = orb['glow_size'] - i * 10
                alpha = 100 - i * 30
                glow_color = (*orb['color'], alpha)
                pygame.draw.circle(surface, glow_color, 
                                 (int(orb['x']), int(orb['y'])), glow_size)
            
            # Draw core
            pygame.draw.circle(surface, orb['color'], 
                             (int(orb['x']), int(orb['y'])), orb['size'])

class FuzzyTailsOnMovingDots(ScreenSaver):
    def __init__(self):
        super().__init__("Fuzzy Tails on Moving Dots", 6000)
        self.dots = []
        self.generate_dots()
        
    def generate_dots(self):
        self.dots = []
        for _ in range(20):
            self.dots.append({
                'x': random.randint(0, SCREEN_WIDTH),
                'y': random.randint(0, SCREEN_HEIGHT),
                'dx': random.uniform(-2, 2),
                'dy': random.uniform(-2, 2),
                'trail': [],
                'color': self.colors[random.randint(0, len(self.colors) - 1)]
            })
    
    def update(self):
        for dot in self.dots:
            # Update position
            dot['x'] += dot['dx']
            dot['y'] += dot['dy']
            
            # Bounce off walls
            if dot['x'] <= 0 or dot['x'] >= SCREEN_WIDTH:
                dot['dx'] *= -1
            if dot['y'] <= 0 or dot['y'] >= SCREEN_HEIGHT:
                dot['dy'] *= -1
            
            # Add to trail with some randomness
            dot['trail'].append((dot['x'] + random.randint(-2, 2), 
                               dot['y'] + random.randint(-2, 2)))
            if len(dot['trail']) > 30:
                dot['trail'].pop(0)
    
    def draw(self, surface):
        for dot in self.dots:
            # Draw fuzzy trail
            if len(dot['trail']) > 1:
                for i, point in enumerate(dot['trail']):
                    alpha = int(255 * (i / len(dot['trail'])))
                    color = (*dot['color'], alpha)
                    pygame.draw.circle(surface, color, 
                                     (int(point[0]), int(point[1])), 2)
            
            # Draw current position
            pygame.draw.circle(surface, dot['color'], 
                             (int(dot['x']), int(dot['y'])), 4)

class MetaballBlobsMerging(ScreenSaver):
    def __init__(self):
        super().__init__("Metaball Blobs Merging/Splitting", 7000)
        self.blobs = []
        self.generate_blobs()
        
    def generate_blobs(self):
        self.blobs = []
        for _ in range(8):
            self.blobs.append({
                'x': random.randint(0, SCREEN_WIDTH),
                'y': random.randint(0, SCREEN_HEIGHT),
                'dx': random.uniform(-1, 1),
                'dy': random.uniform(-1, 1),
                'radius': random.randint(20, 40),
                'color': self.colors[random.randint(0, len(self.colors) - 1)]
            })
    
    def update(self):
        for blob in self.blobs:
            blob['x'] += blob['dx']
            blob['y'] += blob['dy']
            
            # Bounce off walls
            if blob['x'] - blob['radius'] <= 0 or blob['x'] + blob['radius'] >= SCREEN_WIDTH:
                blob['dx'] *= -1
            if blob['y'] - blob['radius'] <= 0 or blob['y'] + blob['radius'] >= SCREEN_HEIGHT:
                blob['dy'] *= -1
    
    def draw(self, surface):
        # Simple metaball effect - draw overlapping circles
        for blob in self.blobs:
            pygame.draw.circle(surface, blob['color'], 
                             (int(blob['x']), int(blob['y'])), blob['radius'])

class FirefliesSyncingGlow(ScreenSaver):
    def __init__(self):
        super().__init__("Fireflies Syncing Glow", 6000)
        self.fireflies = []
        self.sync_timer = 0
        self.generate_fireflies()
        
    def generate_fireflies(self):
        self.fireflies = []
        for _ in range(30):
            self.fireflies.append({
                'x': random.randint(0, SCREEN_WIDTH),
                'y': random.randint(0, SCREEN_HEIGHT),
                'dx': random.uniform(-1, 1),
                'dy': random.uniform(-1, 1),
                'phase': random.uniform(0, 2 * math.pi),
                'color': self.colors[random.randint(0, len(self.colors) - 1)]
            })
    
    def update(self):
        self.sync_timer += 1
        for firefly in self.fireflies:
            firefly['x'] += firefly['dx']
            firefly['y'] += firefly['dy']
            
            # Bounce off walls
            if firefly['x'] <= 0 or firefly['x'] >= SCREEN_WIDTH:
                firefly['dx'] *= -1
            if firefly['y'] <= 0 or firefly['y'] >= SCREEN_HEIGHT:
                firefly['dy'] *= -1
    
    def draw(self, surface):
        sync_value = math.sin(self.sync_timer * 0.1)
        for firefly in self.fireflies:
            # Synchronized blinking
            brightness = int(128 + 127 * sync_value)
            color = (brightness, brightness, brightness)
            pygame.draw.circle(surface, color, 
                             (int(firefly['x']), int(firefly['y'])), 3)

class CurlNoiseFieldMovement(ScreenSaver):
    def __init__(self):
        super().__init__("Curl Noise Field Movement", 7000)
        self.particles = []
        self.time = 0
        self.generate_particles()
        
    def generate_particles(self):
        self.particles = []
        for _ in range(50):
            self.particles.append({
                'x': random.randint(0, SCREEN_WIDTH),
                'y': random.randint(0, SCREEN_HEIGHT),
                'color': self.colors[random.randint(0, len(self.colors) - 1)]
            })
    
    def curl_noise(self, x, y, t):
        # Simplified curl noise
        angle = math.sin(x * 0.01 + t) * math.cos(y * 0.01 + t)
        return math.cos(angle), math.sin(angle)
    
    def update(self):
        self.time += 0.05
        for particle in self.particles:
            dx, dy = self.curl_noise(particle['x'], particle['y'], self.time)
            particle['x'] += dx * 2
            particle['y'] += dy * 2
            
            # Wrap around screen
            if particle['x'] < 0:
                particle['x'] = SCREEN_WIDTH
            elif particle['x'] > SCREEN_WIDTH:
                particle['x'] = 0
            if particle['y'] < 0:
                particle['y'] = SCREEN_HEIGHT
            elif particle['y'] > SCREEN_HEIGHT:
                particle['y'] = 0
    
    def draw(self, surface):
        for particle in self.particles:
            pygame.draw.circle(surface, particle['color'], 
                             (int(particle['x']), int(particle['y'])), 2)

class CircularWaveRipples(ScreenSaver):
    def __init__(self):
        super().__init__("Circular Wave Ripples", 6000)
        self.ripples = []
        self.time = 0
        
    def create_ripple(self):
        ripple = {
            'x': random.randint(100, SCREEN_WIDTH - 100),
            'y': random.randint(100, SCREEN_HEIGHT - 100),
            'radius': 0,
            'max_radius': random.randint(100, 200),
            'speed': random.uniform(1, 3),
            'color': self.colors[random.randint(0, len(self.colors) - 1)]
        }
        self.ripples.append(ripple)
    
    def update(self):
        self.time += 1
        if self.time % 60 == 0:
            self.create_ripple()
        
        for ripple in self.ripples[:]:
            ripple['radius'] += ripple['speed']
            if ripple['radius'] > ripple['max_radius']:
                self.ripples.remove(ripple)
    
    def draw(self, surface):
        for ripple in self.ripples:
            alpha = int(255 * (1 - ripple['radius'] / ripple['max_radius']))
            color = (*ripple['color'], alpha)
            pygame.draw.circle(surface, color, 
                             (int(ripple['x']), int(ripple['y'])), int(ripple['radius']), 2)

class LissajousCurves(ScreenSaver):
    def __init__(self):
        super().__init__("Lissajous Curves", 7000)
        self.time = 0
        self.colors = self.generate_colors()
        
    def update(self):
        self.time += 0.02
        
    def draw(self, surface):
        center_x, center_y = SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2
        
        # Draw multiple Lissajous curves
        for i in range(3):
            a = 150 + i * 50
            b = 100 + i * 30
            freq_x = 3 + i
            freq_y = 2 + i
            phase = self.time + i * math.pi / 3
            
            points = []
            for t in range(0, 628, 2):  # 0 to 2π
                t_val = t / 100.0
                x = center_x + int(a * math.sin(freq_x * t_val + phase))
                y = center_y + int(b * math.sin(freq_y * t_val))
                points.append((x, y))
            
            if len(points) > 1:
                pygame.draw.lines(surface, self.colors[i % len(self.colors)], False, points, 2)

class SpirographFlowers(ScreenSaver):
    def __init__(self):
        super().__init__("Spirograph Flowers", 6000)
        self.time = 0
        self.colors = self.generate_colors()
        
    def update(self):
        self.time += 0.03
        
    def draw(self, surface):
        center_x, center_y = SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2
        
        # Draw spirograph patterns
        for i in range(4):
            R = 100 + i * 20
            r = 30 + i * 10
            d = 50 + i * 15
            
            points = []
            for t in range(0, 1000, 2):
                t_val = t / 100.0
                x = center_x + int((R - r) * math.cos(t_val) + d * math.cos((R - r) * t_val / r))
                y = center_y + int((R - r) * math.sin(t_val) - d * math.sin((R - r) * t_val / r))
                points.append((x, y))
            
            if len(points) > 1:
                pygame.draw.lines(surface, self.colors[i % len(self.colors)], False, points, 2)

class RotatingPolygons(ScreenSaver):
    def __init__(self):
        super().__init__("Rotating Polygons", 6000)
        self.polygons = []
        self.generate_polygons()
        
    def generate_polygons(self):
        self.polygons = []
        for i in range(8):
            sides = 3 + i  # Triangle to decagon
            self.polygons.append({
                'sides': sides,
                'angle': i * math.pi / 4,
                'radius': 50 + i * 20,
                'speed': 0.02 + i * 0.005,
                'color': self.colors[i % len(self.colors)]
            })
    
    def update(self):
        for polygon in self.polygons:
            polygon['angle'] += polygon['speed']
    
    def draw(self, surface):
        center_x, center_y = SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2
        
        for polygon in self.polygons:
            points = []
            for i in range(polygon['sides']):
                angle = polygon['angle'] + i * 2 * math.pi / polygon['sides']
                x = center_x + int(polygon['radius'] * math.cos(angle))
                y = center_y + int(polygon['radius'] * math.sin(angle))
                points.append((x, y))
            
            pygame.draw.polygon(surface, polygon['color'], points)

class DynamicVoronoiDiagram(ScreenSaver):
    def __init__(self):
        super().__init__("Dynamic Voronoi Diagram", 7000)
        self.points = []
        self.generate_points()
        
    def generate_points(self):
        self.points = []
        for _ in range(15):
            self.points.append({
                'x': random.randint(50, SCREEN_WIDTH - 50),
                'y': random.randint(50, SCREEN_HEIGHT - 50),
                'dx': random.uniform(-1, 1),
                'dy': random.uniform(-1, 1),
                'color': self.colors[random.randint(0, len(self.colors) - 1)]
            })
    
    def update(self):
        for point in self.points:
            point['x'] += point['dx']
            point['y'] += point['dy']
            
            # Bounce off walls
            if point['x'] <= 0 or point['x'] >= SCREEN_WIDTH:
                point['dx'] *= -1
            if point['y'] <= 0 or point['y'] >= SCREEN_HEIGHT:
                point['dy'] *= -1
    
    def draw(self, surface):
        # Simple Voronoi-like effect - draw lines between points
        for i, point1 in enumerate(self.points):
            for j, point2 in enumerate(self.points):
                if i < j:
                    pygame.draw.line(surface, LIGHT_GRAY, 
                                   (int(point1['x']), int(point1['y'])),
                                   (int(point2['x']), int(point2['y'])), 1)
        
        # Draw points
        for point in self.points:
            pygame.draw.circle(surface, point['color'], 
                             (int(point['x']), int(point['y'])), 5)

class DelaunayTriangulation(ScreenSaver):
    def __init__(self):
        super().__init__("Delaunay Triangulation", 6000)
        self.points = []
        self.generate_points()
        
    def generate_points(self):
        self.points = []
        for _ in range(20):
            self.points.append({
                'x': random.randint(50, SCREEN_WIDTH - 50),
                'y': random.randint(50, SCREEN_HEIGHT - 50),
                'color': self.colors[random.randint(0, len(self.colors) - 1)]
            })
    
    def update(self):
        # Move points slowly
        for point in self.points:
            point['x'] += random.uniform(-0.5, 0.5)
            point['y'] += random.uniform(-0.5, 0.5)
            
            # Keep in bounds
            point['x'] = max(50, min(SCREEN_WIDTH - 50, point['x']))
            point['y'] = max(50, min(SCREEN_HEIGHT - 50, point['y']))
    
    def draw(self, surface):
        # Simple triangulation - connect all points
        for i, point1 in enumerate(self.points):
            for j, point2 in enumerate(self.points):
                if i < j:
                    pygame.draw.line(surface, LIGHT_GRAY, 
                                   (int(point1['x']), int(point1['y'])),
                                   (int(point2['x']), int(point2['y'])), 1)
        
        # Draw points
        for point in self.points:
            pygame.draw.circle(surface, point['color'], 
                             (int(point['x']), int(point['y'])), 3)

class CirclePackingAnimation(ScreenSaver):
    def __init__(self):
        super().__init__("Circle Packing Animation", 7000)
        self.circles = []
        self.time = 0
        self.generate_circles()
        
    def generate_circles(self):
        self.circles = []
        for _ in range(30):
            self.circles.append({
                'x': random.randint(50, SCREEN_WIDTH - 50),
                'y': random.randint(50, SCREEN_HEIGHT - 50),
                'radius': random.randint(5, 20),
                'growing': True,
                'color': self.colors[random.randint(0, len(self.colors) - 1)]
            })
    
    def update(self):
        self.time += 1
        for circle in self.circles:
            if circle['growing']:
                circle['radius'] += 0.5
                if circle['radius'] >= 30:
                    circle['growing'] = False
            else:
                circle['radius'] -= 0.5
                if circle['radius'] <= 5:
                    circle['growing'] = True
    
    def draw(self, surface):
        for circle in self.circles:
            pygame.draw.circle(surface, circle['color'], 
                             (int(circle['x']), int(circle['y'])), int(circle['radius']))

class ParametricFunctionPlots(ScreenSaver):
    def __init__(self):
        super().__init__("Parametric Function Plots", 6000)
        self.time = 0
        self.colors = self.generate_colors()
        
    def update(self):
        self.time += 0.02
        
    def draw(self, surface):
        center_x, center_y = SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2
        
        # Draw parametric curves
        for i in range(3):
            points = []
            for t in range(0, 628, 2):  # 0 to 2π
                t_val = t / 100.0
                # Different parametric functions
                if i == 0:
                    x = center_x + int(100 * math.cos(t_val + self.time))
                    y = center_y + int(100 * math.sin(t_val + self.time))
                elif i == 1:
                    x = center_x + int(80 * math.cos(2 * t_val + self.time))
                    y = center_y + int(80 * math.sin(3 * t_val + self.time))
                else:
                    x = center_x + int(60 * math.cos(3 * t_val + self.time))
                    y = center_y + int(60 * math.sin(2 * t_val + self.time))
                points.append((x, y))
            
            if len(points) > 1:
                pygame.draw.lines(surface, self.colors[i % len(self.colors)], False, points, 2)

class JuliaSetExplorer(ScreenSaver):
    def __init__(self):
        super().__init__("Julia Set Explorer", 8000)
        self.time = 0
        self.colors = self.generate_colors()
        
    def update(self):
        self.time += 0.01
        
    def draw(self, surface):
        # Simplified Julia set
        center_x, center_y = SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2
        scale = 100
        
        for x in range(0, SCREEN_WIDTH, 4):
            for y in range(0, SCREEN_HEIGHT, 4):
                # Map pixel to complex plane
                zx = (x - center_x) / scale
                zy = (y - center_y) / scale
                
                # Julia set iteration
                c = 0.7 * math.cos(self.time) + 0.7j * math.sin(self.time)
                z = zx + zy * 1j
                
                for i in range(20):
                    z = z * z + c
                    if abs(z) > 2:
                        break
                
                if i < 20:
                    color = self.colors[i % len(self.colors)]
                    pygame.draw.rect(surface, color, (x, y, 4, 4))

class MandelbrotZoomDrift(ScreenSaver):
    def __init__(self):
        super().__init__("Mandelbrot Zoom Drift", 8000)
        self.time = 0
        self.colors = self.generate_colors()
        
    def update(self):
        self.time += 0.005
        
    def draw(self, surface):
        # Simplified Mandelbrot set with zoom
        center_x, center_y = SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2
        scale = 100 + 50 * math.sin(self.time)
        
        for x in range(0, SCREEN_WIDTH, 4):
            for y in range(0, SCREEN_HEIGHT, 4):
                # Map pixel to complex plane
                cx = (x - center_x) / scale
                cy = (y - center_y) / scale
                
                # Mandelbrot iteration
                zx, zy = 0, 0
                for i in range(20):
                    zx2 = zx * zx - zy * zy + cx
                    zy2 = 2 * zx * zy + cy
                    zx, zy = zx2, zy2
                    
                    if zx * zx + zy * zy > 4:
                        break
                
                if i < 20:
                    color = self.colors[i % len(self.colors)]
                    pygame.draw.rect(surface, color, (x, y, 4, 4))

class PenroseTilingAnimation(ScreenSaver):
    def __init__(self):
        super().__init__("Penrose Tiling Animation", 7000)
        self.time = 0
        self.colors = self.generate_colors()
        
    def update(self):
        self.time += 0.02
        
    def draw(self, surface):
        center_x, center_y = SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2
        
        # Simplified Penrose-like pattern
        for i in range(8):
            angle = self.time + i * math.pi / 4
            radius = 50 + i * 20
            
            # Draw rhombus-like shapes
            points = []
            for j in range(4):
                point_angle = angle + j * math.pi / 2
                x = center_x + int(radius * math.cos(point_angle))
                y = center_y + int(radius * math.sin(point_angle))
                points.append((x, y))
            
            pygame.draw.polygon(surface, self.colors[i % len(self.colors)], points)

class RotatingTesseract(ScreenSaver):
    def __init__(self):
        super().__init__("Rotating Tesseract (4D Cube)", 7000)
        self.time = 0
        self.colors = self.generate_colors()
        
    def update(self):
        self.time += 0.02
        
    def draw(self, surface):
        center_x, center_y = SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2
        
        # Simplified 4D cube projection
        for i in range(16):
            angle = self.time + i * math.pi / 8
            radius = 80 + i * 10
            
            x = center_x + int(radius * math.cos(angle))
            y = center_y + int(radius * math.sin(angle))
            
            size = 10 + i * 2
            pygame.draw.circle(surface, self.colors[i % len(self.colors)], 
                             (x, y), size)

class OscillatingSineWaveRibbons(ScreenSaver):
    def __init__(self):
        super().__init__("Oscillating Sine Wave Ribbons", 6000)
        self.time = 0
        self.colors = self.generate_colors()
        
    def update(self):
        self.time += 0.05
        
    def draw(self, surface):
        # Draw multiple sine wave ribbons
        for i in range(5):
            points = []
            for x in range(0, SCREEN_WIDTH, 5):
                y = SCREEN_HEIGHT // 2 + int(50 * math.sin(x * 0.02 + self.time + i) + 
                                            30 * math.sin(x * 0.01 + self.time * 2 + i))
                points.append((x, y))
            
            if len(points) > 1:
                pygame.draw.lines(surface, self.colors[i % len(self.colors)], False, points, 3)

class ConvexHullDancers(ScreenSaver):
    def __init__(self):
        super().__init__("Convex Hull Dancers", 6000)
        self.points = []
        self.generate_points()
        
    def generate_points(self):
        self.points = []
        for _ in range(15):
            self.points.append({
                'x': random.randint(50, SCREEN_WIDTH - 50),
                'y': random.randint(50, SCREEN_HEIGHT - 50),
                'dx': random.uniform(-2, 2),
                'dy': random.uniform(-2, 2),
                'color': self.colors[random.randint(0, len(self.colors) - 1)]
            })
    
    def update(self):
        for point in self.points:
            point['x'] += point['dx']
            point['y'] += point['dy']
            
            # Bounce off walls
            if point['x'] <= 0 or point['x'] >= SCREEN_WIDTH:
                point['dx'] *= -1
            if point['y'] <= 0 or point['y'] >= SCREEN_HEIGHT:
                point['dy'] *= -1
    
    def draw(self, surface):
        # Draw convex hull (simplified)
        if len(self.points) >= 3:
            hull_points = [(p['x'], p['y']) for p in self.points]
            # Simple convex hull approximation
            pygame.draw.polygon(surface, LIGHT_GRAY, hull_points, 2)
        
        # Draw points
        for point in self.points:
            pygame.draw.circle(surface, point['color'], 
                             (int(point['x']), int(point['y'])), 5)

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
    ColorFlowGrid(),
    FloatingBubbles(),
    KaleidoscopeTunnel(),
    BezierBlossom(),
    StarfieldWarpDrive(),
    LissajousOrbitDance(),
    ParticleFireworks(),
    MagneticDots(),
    FractalVines(),
    PaintDripCanvas(),
    SoapFilmInterference(),
    MirrorEchoes(),
    SwarmingParticles(),
    RandomWalkersWithTrails(),
    CollidingBallsWithElasticBounce(),
    GravityWellAttractors(),
    FireflyMotion(),
    SpiralParticleFountain(),
    DustCloudDrift(),
    BoidsFlockingSimulation(),
    BrownianMotionDots(),
    OrbitingMoons(),
    TornadoFunnel(),
    DrippingInk(),
    ParticleTrailsThatFormShapes(),
    PixelRain(),
    FloatingOrbsWithGlow(),
    FuzzyTailsOnMovingDots(),
    MetaballBlobsMerging(),
    FirefliesSyncingGlow(),
    CurlNoiseFieldMovement(),
    CircularWaveRipples(),
    LissajousCurves(),
    SpirographFlowers(),
    RotatingPolygons(),
    DynamicVoronoiDiagram(),
    DelaunayTriangulation(),
    CirclePackingAnimation(),
    ParametricFunctionPlots(),
    JuliaSetExplorer(),
    MandelbrotZoomDrift(),
    PenroseTilingAnimation(),
    RotatingTesseract(),
    OscillatingSineWaveRibbons(),
    ConvexHullDancers(),
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