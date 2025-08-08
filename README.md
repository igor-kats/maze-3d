# 3D Labyrinth Game

A procedurally generated 3D maze escape game built with Godot Engine 4.x.

## Overview

Navigate through a randomly generated 3D labyrinth in first-person view to find the exit. Each maze is unique, featuring procedural generation with recursive backtracking algorithms.

## Features

- **Procedural Maze Generation**: Every playthrough offers a unique 51x51 maze
- **3D First-Person Experience**: Immersive 3D navigation with realistic collision detection  
- **Visual Indicators**: Glowing green exit markers for clear objectives
- **Optimized Rendering**: Efficient 3D mesh generation with materials and lighting

## Current Status

🟡 **In Development** - Core maze generation and rendering systems complete

### ✅ Completed
- Maze generation algorithm (recursive backtracking)
- 3D maze renderer with walls, floors, and exit markers
- Basic scene structure and lighting setup
- Material system (wall, floor, exit materials)

### 🔄 In Progress  
- Scene configuration and node setup
- Performance optimization for lower-end hardware

### ⏳ Planned
- First-person player controller with mouse look
- Player movement and collision detection
- Win condition and level progression
- UI system (minimap, HUD, menus)
- Sound effects and ambient audio
- Multiple maze sizes and difficulty levels

## Requirements

- **Godot Engine 4.x** (4.1+ recommended)
- **System Requirements**: 
  - OpenGL 3.3 compatible graphics card
  - 4GB RAM minimum (8GB recommended for larger mazes)
  - Multi-core CPU recommended for maze generation

## Quick Start

### Setup
1. Install [Godot Engine 4.x](https://godotengine.org/download)
2. Clone this repository:
   ```bash
   git clone <repository-url>
   cd Labyrinth_game
   ```
3. Open Godot and import the project
4. Open the main scene and run the project

### Scene Structure Setup
Create the following scene structure:
```
Main (Node3D)
├── WorldEnvironment
├── DirectionalLight3D  
├── MeshInstance3D
├── maze_generator (Node3D) → Attach scripts/01_maze_generator.gd
├── MazeRenderer (Node3D) → Attach scripts/02_maze_renderer.gd  
└── Camera3D (to be added)
```

## Performance Notes

The default 51x51 maze creates ~2,600 wall objects, which may impact performance on older hardware. For testing on lower-end devices:

1. Reduce maze size in `01_maze_generator.gd`:
   ```gdscript
   var width = 25  # Reduced from 51
   var height = 25 # Reduced from 51
   ```

2. Adjust rendering quality in project settings

## Development

### Adding New Features
- Scripts use numbered naming: `##_<name>.gd`
- Follow Godot's GDScript conventions (tabs for indentation)
- Export variables for editor configuration
- Document new functions and classes

### Contributing
1. Fork the repository
2. Create a feature branch
3. Follow the existing code style
4. Update documentation for new features
5. Submit a pull request

## Architecture

### Core Scripts

**`01_maze_generator.gd`**
- Implements recursive backtracking maze generation
- Creates starting areas and exit placement
- Configurable maze dimensions and complexity

**`02_maze_renderer.gd`** 
- Converts maze data to 3D geometry
- Handles materials and collision shapes
- Optimized mesh creation and management

### Technical Details
- **Maze Algorithm**: Recursive backtracking ensures single-solution paths
- **Rendering**: Individual StaticBody3D nodes per wall for precise collision
- **Materials**: StandardMaterial3D with configurable colors and emission
- **Coordinates**: 2D maze grid mapped to 3D world space (X,Z plane)

## License

[Add your license here]

## Credits

Developed using Godot Engine 4.x. Maze generation inspired by classic recursive backtracking algorithms.