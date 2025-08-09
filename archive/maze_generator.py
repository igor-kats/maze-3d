import random
from typing import List, Tuple, Set

class MazeGenerator:
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        self.maze = [[1 for _ in range(width)] for _ in range(height)]  # 1 = wall, 0 = path
        
    def generate(self) -> List[List[int]]:
        """Generate a maze using recursive backtracking algorithm"""
        # Start from center
        start_x, start_y = self.width // 2, self.height // 2
        if start_x % 2 == 0:
            start_x += 1
        if start_y % 2 == 0:
            start_y += 1
            
        self._carve_path(start_x, start_y)
        self._ensure_starting_area(start_x, start_y)
        self._add_crossroads()
        self._create_exit()
        return self.maze
    
    def _carve_path(self, x: int, y: int):
        """Carve a path using recursive backtracking"""
        self.maze[y][x] = 0  # Mark as path
        
        # Get random directions
        directions = [(0, 2), (2, 0), (0, -2), (-2, 0)]
        random.shuffle(directions)
        
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            
            # Check if the new position is valid and unvisited
            if (0 < nx < self.width - 1 and 
                0 < ny < self.height - 1 and 
                self.maze[ny][nx] == 1):
                
                # Carve the wall between current and next cell
                self.maze[y + dy // 2][x + dx // 2] = 0
                self._carve_path(nx, ny)
    
    def _ensure_starting_area(self, start_x: int, start_y: int):
        """Ensure there's a clear starting area around the center"""
        # Clear a small area around the starting position
        for dy in range(-1, 2):
            for dx in range(-1, 2):
                new_x, new_y = start_x + dx, start_y + dy
                if (0 <= new_x < self.width and 0 <= new_y < self.height):
                    self.maze[new_y][new_x] = 0
    
    def _add_crossroads(self):
        """Add additional passages to create more crossroads and choices"""
        # Calculate number of additional passages to add
        total_cells = self.width * self.height
        num_passages = total_cells // 50  # Add roughly 2% more passages
        
        for _ in range(num_passages):
            # Pick a random wall that could become a passage
            for attempt in range(50):  # Try up to 50 times
                x = random.randrange(1, self.width - 1)
                y = random.randrange(1, self.height - 1)
                
                # Only consider walls that are surrounded by at least 2 paths
                if self.maze[y][x] == 1:
                    # Count adjacent paths
                    adjacent_paths = 0
                    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
                    
                    for dx, dy in directions:
                        nx, ny = x + dx, y + dy
                        if (0 <= nx < self.width and 0 <= ny < self.height and 
                            self.maze[ny][nx] == 0):
                            adjacent_paths += 1
                    
                    # If this wall has 2 or more adjacent paths, consider making it a passage
                    if adjacent_paths >= 2:
                        # 30% chance to create the passage (creates more variety)
                        if random.random() < 0.3:
                            self.maze[y][x] = 0
                            break
    
    def _create_exit(self):
        """Create an exit at the edge of the maze"""
        # Find edge positions and create exit
        edges = []
        
        # Top and bottom edges
        for x in range(1, self.width - 1, 2):
            if self.maze[1][x] == 0:
                edges.append((x, 0))
            if self.maze[self.height - 2][x] == 0:
                edges.append((x, self.height - 1))
        
        # Left and right edges  
        for y in range(1, self.height - 1, 2):
            if self.maze[y][1] == 0:
                edges.append((0, y))
            if self.maze[y][self.width - 2] == 0:
                edges.append((self.width - 1, y))
        
        if edges:
            exit_x, exit_y = random.choice(edges)
            self.maze[exit_y][exit_x] = 2  # 2 = exit
    
    def get_center_position(self) -> Tuple[int, int]:
        """Get the center starting position"""
        return (self.width // 2, self.height // 2)
    
    def get_exit_position(self) -> Tuple[int, int]:
        """Get the exit position"""
        for y in range(self.height):
            for x in range(self.width):
                if self.maze[y][x] == 2:
                    return (x, y)
        return (0, 0)  # Fallback
    
    def is_wall(self, x: int, y: int) -> bool:
        """Check if position is a wall"""
        if x < 0 or x >= self.width or y < 0 or y >= self.height:
            return True
        return self.maze[y][x] == 1
    
    def print_maze(self):
        """Print maze for debugging"""
        for row in self.maze:
            print(''.join(['█' if cell == 1 else ('E' if cell == 2 else ' ') for cell in row]))