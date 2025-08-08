#!/usr/bin/env python3

import pygame
import sys
import time
from maze_generator import MazeGenerator
from renderer_3d import Renderer3D
from player import Player

class LabyrinthGame:
    def __init__(self):
        pygame.init()
        
        # Game settings
        self.width = 1024
        self.height = 768
        self.fps = 60
        
        # Initialize components
        self.renderer = Renderer3D(self.width, self.height)
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 24)
        
        # Generate maze
        self.maze_width = 51  # Odd numbers work best for maze generation
        self.maze_height = 51
        self.maze_generator = MazeGenerator(self.maze_width, self.maze_height)
        self.maze = self.maze_generator.generate()
        
        # Create player at center
        center_x, center_y = self.maze_generator.get_center_position()
        self.player = Player(float(center_x), float(center_y))
        
        
        # Game state
        self.running = True
        self.won = False
        
        # Hide mouse cursor and capture mouse
        pygame.mouse.set_visible(False)
        pygame.event.set_grab(True)
        
        print("Labyrinth generated!")
        print("Controls:")
        print("  WASD - Move")
        print("  Mouse - Look around") 
        print("  ESC - Quit")
        print("Find the exit (green on minimap)!")
    
    def handle_events(self):
        """Handle pygame events"""
        mouse_rel = pygame.mouse.get_rel()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                elif event.key == pygame.K_r and self.won:
                    # Restart game
                    self.restart_game()
        
        return mouse_rel
    
    def update(self, dt: float, mouse_rel: tuple):
        """Update game state"""
        if not self.won:
            # Get current key states
            keys_pressed = pygame.key.get_pressed()
            
            # Update player
            self.player.update(dt, keys_pressed, mouse_rel, self.maze)
            
            # Check win condition
            if self.player.is_at_exit(self.maze):
                self.won = True
                print("Congratulations! You escaped the labyrinth!")
                print("Press 'R' to play again or ESC to quit")
    
    def render(self):
        """Render the game"""
        self.renderer.clear_screen()
        
        if not self.won:
            # Render 3D view
            player_x, player_y = self.player.get_position()
            player_angle = self.player.get_angle()
            player_pitch = self.player.get_pitch()
            
            self.renderer.render_scene(self.maze, player_x, player_y, player_angle, player_pitch)
            self.renderer.render_minimap(self.maze, player_x, player_y, player_angle)
            
            # Render UI
            fps = int(self.clock.get_fps())
            self.renderer.render_ui(self.font, fps, player_x, player_y, player_angle, self.maze)
        else:
            # Render win screen
            self.render_win_screen()
        
        self.renderer.display()
    
    def render_win_screen(self):
        """Render the victory screen"""
        # Win message
        win_text = pygame.font.Font(None, 72).render("YOU ESCAPED!", True, (0, 255, 0))
        win_rect = win_text.get_rect(center=(self.width//2, self.height//2 - 50))
        self.renderer.screen.blit(win_text, win_rect)
        
        # Instructions
        restart_text = self.font.render("Press 'R' to play again", True, (255, 255, 255))
        restart_rect = restart_text.get_rect(center=(self.width//2, self.height//2 + 20))
        self.renderer.screen.blit(restart_text, restart_rect)
        
        quit_text = self.font.render("Press ESC to quit", True, (255, 255, 255))
        quit_rect = quit_text.get_rect(center=(self.width//2, self.height//2 + 50))
        self.renderer.screen.blit(quit_text, quit_rect)
    
    def restart_game(self):
        """Restart the game with a new maze"""
        # Generate new maze
        self.maze = self.maze_generator.generate()
        
        # Reset player position
        center_x, center_y = self.maze_generator.get_center_position()
        self.player = Player(float(center_x), float(center_y))
        
        # Reset game state
        self.won = False
        
        print("New labyrinth generated!")
    
    def run(self):
        """Main game loop"""
        last_time = time.time()
        
        while self.running:
            current_time = time.time()
            dt = current_time - last_time
            last_time = current_time
            
            # Handle events
            mouse_rel = self.handle_events()
            
            # Update game
            self.update(dt, mouse_rel)
            
            # Render
            self.render()
            
            # Control frame rate
            self.clock.tick(self.fps)
        
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = LabyrinthGame()
    game.run()