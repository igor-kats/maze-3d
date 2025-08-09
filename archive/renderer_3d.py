import pygame
import math
import numpy as np
from typing import List, Tuple

class Renderer3D:
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("3D Labyrinth Escape")
        
        # Colors
        self.BLACK = (0, 0, 0)
        self.WHITE = (255, 255, 255)
        self.LIGHT_GRAY = (220, 220, 220)
        self.RED = (255, 0, 0)
        self.GREEN = (0, 255, 0)
        self.BLUE = (0, 0, 255)
        self.GRAY = (128, 128, 128)
        self.DARK_GRAY = (64, 64, 64)
        
        # Natural colors
        self.SKY_BLUE = (135, 206, 235)
        self.CLOUD_WHITE = (248, 248, 255)
        self.HEDGE_GREEN = (34, 139, 34)
        self.EARTH_BROWN = (139, 69, 19)
        
        # Brick colors
        self.BRICK_RED = (180, 60, 40)
        self.BRICK_DARK = (120, 40, 30)
        self.MORTAR_GRAY = (200, 200, 200)
        self.BRICK_LIGHT = (220, 80, 60)
        
        # Bush/hedge colors
        self.BUSH_GREEN = (34, 139, 34)
        self.BUSH_DARK = (20, 80, 20)
        self.BUSH_LIGHT = (50, 180, 50)
        self.BUSH_SHADOW = (15, 60, 15)
        
        # Floor tile colors
        self.FLOOR_LIGHT = (180, 120, 60)  # Light brown tile
        self.FLOOR_DARK = (120, 80, 40)   # Dark brown tile
        
        # 3D projection parameters
        self.fov = math.pi / 3  # 60 degrees
        self.view_distance = 10
        
    def clear_screen(self):
        """Clear the screen and draw sky with clouds"""
        # Fill with sky blue
        self.screen.fill(self.SKY_BLUE)
        
        # Draw some simple cloud shapes
        self.draw_clouds()
    
    def draw_clouds(self):
        """Draw simple cloud shapes on the sky"""
        import random
        random.seed(42)  # Fixed seed for consistent clouds
        
        # Draw several cloud patches
        for i in range(8):
            x = (i * 150 + 50) % (self.width + 200)
            y = random.randint(10, self.height // 3)
            
            # Draw cloud as overlapping circles
            for j in range(4):
                cloud_x = x + random.randint(-30, 30)
                cloud_y = y + random.randint(-15, 15)
                radius = random.randint(25, 45)
                
                # Draw cloud shadow first (slightly darker)
                shadow_color = (220, 220, 230)
                pygame.draw.circle(self.screen, shadow_color, 
                                 (cloud_x + 2, cloud_y + 2), radius)
                
                # Draw main cloud
                pygame.draw.circle(self.screen, self.CLOUD_WHITE, 
                                 (cloud_x, cloud_y), radius)
    
    def render_scene(self, maze: List[List[int]], player_x: float, player_y: float, player_angle: float, player_pitch: float):
        """Render 3D scene with proper floor, ceiling, and walls"""
        num_rays = self.width
        horizon_line = self.height // 2 + int(player_pitch * 200)  # Pitch affects horizon
        player_height = 0.5  # Player eye level above ground plane (y=0)
        
        for ray_id in range(num_rays):
            # Calculate ray angle
            ray_angle = player_angle - self.fov/2 + (ray_id / num_rays) * self.fov
            
            # Cast ray and find distance to wall
            wall_distance, hit_wall = self._cast_ray(maze, player_x, player_y, ray_angle)
            wall_distance *= math.cos(ray_angle - player_angle)  # Correct fisheye
            
            # Render floor using floor casting
            self._render_floor_column(ray_id, ray_angle, player_x, player_y, player_height, player_pitch, horizon_line)
            
            # Render walls if hit
            if hit_wall and wall_distance > 0:
                # Calculate wall height on screen
                wall_height = int(self.height / (wall_distance + 0.0001))
                wall_top = horizon_line - wall_height // 2
                wall_bottom = horizon_line + wall_height // 2
                
                # Draw textured wall
                self._render_textured_wall(ray_id, wall_top, wall_bottom, wall_distance, ray_angle, 
                                         player_x, player_y, maze)
    
    def _render_floor_column(self, ray_id: int, ray_angle: float, player_x: float, player_y: float, 
                           player_height: float, player_pitch: float, horizon_line: int):
        """Super simple fast floor - just gradient"""
        if horizon_line >= self.height:
            return
        
        # Simple tile-like effect based on column position and player position
        tile_variation = int((ray_id * 0.1 + player_x + player_y)) % 4
        
        if tile_variation < 2:
            floor_color = self.FLOOR_LIGHT
        else:
            floor_color = self.FLOOR_DARK
            
        # Single line draw - maximum performance!
        pygame.draw.line(self.screen, floor_color,
                       (ray_id, horizon_line), (ray_id, self.height))
    
    def _render_textured_wall(self, ray_id: int, wall_top: int, wall_bottom: int, wall_distance: float,
                            ray_angle: float, player_x: float, player_y: float, maze: List[List[int]]):
        """Render a wall column with ONLY line drawing for maximum performance"""
        # Calculate wall hit position
        adjusted_angle = ray_angle - math.pi/2
        hit_x = player_x + math.cos(adjusted_angle) * wall_distance
        hit_y = player_y + math.sin(adjusted_angle) * wall_distance
        
        # Determine wall type based on position
        wall_type = self._get_wall_type(hit_x, hit_y)
        
        # Distance-based brightness
        brightness = max(0.4, min(1.0, 1.0 - wall_distance / self.view_distance))
        
        # Get base color
        base_color, accent_color = self._get_fast_wall_colors(wall_type, hit_x, hit_y)
        
        # Apply brightness
        wall_color = (int(base_color[0] * brightness),
                     int(base_color[1] * brightness), 
                     int(base_color[2] * brightness))
        
        # ONLY use line drawing - no pixel operations!
        pygame.draw.line(self.screen, wall_color, 
                       (ray_id, max(0, wall_top)), 
                       (ray_id, min(self.height, wall_bottom)))
    
    def _get_wall_type(self, x: float, y: float):
        """Determine wall type based on position - creates varied maze sections"""
        # Create zones - different areas have different wall types
        zone_x = int(x / 10)  # Every 10 units
        zone_y = int(y / 10)
        
        # Use zone coordinates to determine type
        zone_sum = zone_x + zone_y
        
        # Mix of brick and bush areas
        if zone_sum % 3 == 0:
            return "brick"
        else:
            return "bush"
    
    def _get_fast_wall_colors(self, wall_type: str, x: float, y: float):
        """Get base and accent colors for fast wall rendering"""
        if wall_type == "brick":
            # Simple brick color variation
            variation = int((x + y) * 2) % 3
            if variation == 0:
                return self.BRICK_RED, self.MORTAR_GRAY
            elif variation == 1:
                return self.BRICK_DARK, self.MORTAR_GRAY  
            else:
                return self.BRICK_LIGHT, self.MORTAR_GRAY
        else:
            # Bush colors
            variation = int((x + y) * 1.5) % 4
            if variation == 0:
                return self.BUSH_GREEN, self.BUSH_LIGHT
            elif variation == 1:
                return self.BUSH_GREEN, self.BUSH_DARK
            elif variation == 2:
                return self.BUSH_DARK, self.BUSH_LIGHT
            else:
                return self.BUSH_GREEN, self.BUSH_SHADOW
    
    def _cast_ray(self, maze: List[List[int]], start_x: float, start_y: float, angle: float) -> Tuple[float, bool]:
        """Cast a ray and return distance to wall"""
        # Adjust angle so 0° = North, 90° = East, 180° = South, 270° = West
        adjusted_angle = angle - math.pi/2
        dx = math.cos(adjusted_angle)
        dy = math.sin(adjusted_angle)
        
        # Ray casting with small steps
        step_size = 0.05
        distance = 0
        x, y = start_x, start_y
        
        while distance < self.view_distance:
            x += dx * step_size
            y += dy * step_size
            distance += step_size
            
            # Check maze boundaries
            maze_x, maze_y = int(x), int(y)
            if (maze_y < 0 or maze_y >= len(maze) or 
                maze_x < 0 or maze_x >= len(maze[0]) or
                maze[maze_y][maze_x] == 1):
                return distance, True
        
        return self.view_distance, False
    
    def render_minimap(self, maze: List[List[int]], player_x: float, player_y: float, player_angle: float):
        """Render a 2D minimap in the corner"""
        minimap_size = 150
        minimap_scale = 3
        minimap_x = self.width - minimap_size - 10
        minimap_y = 10
        
        # Draw minimap background
        pygame.draw.rect(self.screen, (240, 240, 240), 
                        (minimap_x, minimap_y, minimap_size, minimap_size))
        
        # Draw maze walls on minimap
        cell_size = minimap_scale
        for y in range(len(maze)):
            for x in range(len(maze[0])):
                screen_x = minimap_x + x * cell_size
                screen_y = minimap_y + y * cell_size
                
                if maze[y][x] == 1:  # Wall
                    pygame.draw.rect(self.screen, (60, 120, 60), 
                                   (screen_x, screen_y, cell_size, cell_size))
                elif maze[y][x] == 2:  # Exit
                    pygame.draw.rect(self.screen, (255, 215, 0), 
                                   (screen_x, screen_y, cell_size, cell_size))
        
        # Draw player on minimap
        player_screen_x = minimap_x + int(player_x * cell_size)
        player_screen_y = minimap_y + int(player_y * cell_size)
        pygame.draw.circle(self.screen, self.RED, 
                          (player_screen_x, player_screen_y), 3)
        
        # Draw player direction (facing direction)
        # Adjust angle so 0° = North, 90° = East, 180° = South, 270° = West
        adjusted_angle = player_angle - math.pi/2
        direction_length = 15
        end_x = player_screen_x + int(math.cos(adjusted_angle) * direction_length)
        end_y = player_screen_y + int(math.sin(adjusted_angle) * direction_length)
        pygame.draw.line(self.screen, self.RED, 
                        (player_screen_x, player_screen_y), (end_x, end_y), 3)
        
        # Draw a small triangle to show direction more clearly
        pygame.draw.circle(self.screen, self.RED, (end_x, end_y), 3)
    
    def render_ui(self, font, fps: int, player_x=None, player_y=None, player_angle=None, maze=None):
        """Render UI elements"""
        # FPS counter
        fps_text = font.render(f"FPS: {fps}", True, self.BLACK)
        self.screen.blit(fps_text, (10, 10))
        
        # Instructions
        instructions = [
            "WASD: Move",
            "Mouse: Look around",
            "ESC: Quit"
        ]
        
        for i, instruction in enumerate(instructions):
            text = font.render(instruction, True, self.BLACK)
            self.screen.blit(text, (10, 40 + i * 20))
    
    def display(self):
        """Update the display"""
        pygame.display.flip()