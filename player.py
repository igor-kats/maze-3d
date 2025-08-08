import pygame
import math
from typing import List

class Player:
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y
        self.angle = 0.0  # Player's facing direction (yaw)
        self.pitch = 0.0  # Player's vertical look angle (pitch)
        self.speed = 3.0  # Movement speed
        self.rotation_speed = 2.0  # Rotation speed
        
        # Mouse sensitivity
        self.mouse_sensitivity = 0.003
        self.max_pitch = math.pi / 3  # Limit pitch to 60 degrees up/down
        
    def update(self, dt: float, keys_pressed, mouse_rel: tuple, maze: List[List[int]]):
        """Update player position and rotation"""
        # Mouse look
        mouse_x, mouse_y = mouse_rel
        self.angle += mouse_x * self.mouse_sensitivity
        self.pitch -= mouse_y * self.mouse_sensitivity  # Negative for natural mouse look
        
        # Clamp pitch to prevent over-rotation
        self.pitch = max(-self.max_pitch, min(self.max_pitch, self.pitch))
        
        # Keep angle in range [0, 2π]
        while self.angle < 0:
            self.angle += 2 * math.pi
        while self.angle >= 2 * math.pi:
            self.angle -= 2 * math.pi
        
        # Calculate movement vectors
        # Note: In maze coordinates, Y increases downward
        # Adjust angle so 0° = North, 90° = East, 180° = South, 270° = West
        adjusted_angle = self.angle - math.pi/2
        forward_x = math.cos(adjusted_angle)
        forward_y = math.sin(adjusted_angle)
        right_x = math.cos(adjusted_angle + math.pi/2)
        right_y = math.sin(adjusted_angle + math.pi/2)
        
        # Handle movement with collision detection
        new_x = self.x
        new_y = self.y
        
        move_speed = self.speed * dt
        
        # Forward/backward movement
        if keys_pressed[pygame.K_w]:
            new_x += forward_x * move_speed
            new_y += forward_y * move_speed
        if keys_pressed[pygame.K_s]:
            new_x -= forward_x * move_speed
            new_y -= forward_y * move_speed
        
        # Strafe left/right
        if keys_pressed[pygame.K_a]:
            new_x -= right_x * move_speed
            new_y -= right_y * move_speed
        if keys_pressed[pygame.K_d]:
            new_x += right_x * move_speed
            new_y += right_y * move_speed
        
        # Apply movement with collision detection
        if not self._check_collision(new_x, self.y, maze):
            self.x = new_x
        if not self._check_collision(self.x, new_y, maze):
            self.y = new_y
    
    def _check_collision(self, x: float, y: float, maze: List[List[int]]) -> bool:
        """Check if position collides with walls"""
        # Player radius for collision
        radius = 0.3
        
        # Check corners and center points of player's bounding box
        check_points = [
            (x, y),                          # Center
            (x - radius, y - radius),        # Top-left
            (x + radius, y - radius),        # Top-right
            (x - radius, y + radius),        # Bottom-left
            (x + radius, y + radius),        # Bottom-right
            (x, y - radius),                 # Top-center
            (x, y + radius),                 # Bottom-center
            (x - radius, y),                 # Left-center
            (x + radius, y)                  # Right-center
        ]
        
        for point_x, point_y in check_points:
            maze_x, maze_y = int(point_x), int(point_y)
            
            # Check bounds
            if (maze_x < 0 or maze_x >= len(maze[0]) or 
                maze_y < 0 or maze_y >= len(maze)):
                return True
            
            # Check if position is a wall
            if maze[maze_y][maze_x] == 1:
                return True
        
        return False
    
    def get_position(self) -> tuple:
        """Get current position"""
        return (self.x, self.y)
    
    def get_angle(self) -> float:
        """Get current facing angle"""
        return self.angle
    
    def get_pitch(self) -> float:
        """Get current pitch angle"""
        return self.pitch
    
    def is_at_exit(self, maze: List[List[int]]) -> bool:
        """Check if player is at the exit"""
        maze_x, maze_y = int(self.x), int(self.y)
        
        if (0 <= maze_x < len(maze[0]) and 
            0 <= maze_y < len(maze)):
            return maze[maze_y][maze_x] == 2
        
        return False