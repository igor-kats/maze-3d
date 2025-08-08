# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a 3D Labyrinth Game built using the Godot Engine. The project creates a procedurally generated maze that players can navigate in first-person 3D view to find the exit.

**Current Status**: Maze generation and rendering scripts completed, needs scene setup and additional game systems.

## Development Environment

### Engine Requirements
- **Godot Engine 4.x** (recommended: latest stable version)
- Cross-platform development (Windows, macOS, Linux)

### Project Structure
```
Labyrinth_game/
├── scripts/                    # GDScript files
│   ├── 01_maze_generator.gd   # Procedural maze generation
│   └── 02_maze_renderer.gd    # 3D maze visualization
├── main.py                    # Python prototype (deprecated)
├── maze_generator.py          # Python prototype (deprecated)
├── player.py                  # Python prototype (deprecated)
├── renderer_3d.py             # Python prototype (deprecated)
├── requirements.txt           # Python dependencies (deprecated)
├── CLAUDE.md                  # This file
├── README.md                  # Project documentation
└── ROADMAP.md                 # Development roadmap
```

## Current Implementation

### Godot Scene Structure
```
Main (Node3D)
├── WorldEnvironment          # Environment settings
├── DirectionalLight3D        # Scene lighting
├── MeshInstance3D           # Additional mesh objects
├── maze_generator (Node3D)   # With 01_maze_generator.gd script
├── MazeRenderer (Node3D)     # With 02_maze_renderer.gd script
└── Camera3D                 # First-person camera (to be added)
```

### Completed Scripts

#### 01_maze_generator.gd
- **Purpose**: Generates procedural mazes using recursive backtracking
- **Features**:
  - 51x51 maze grid with configurable dimensions
  - Ensures connected paths from center to edges
  - Creates starting area and random exit placement
  - Adds crossroads for more interesting navigation
- **Key Methods**: `generate_maze()`, `carve_path()`, `create_exit()`

#### 02_maze_renderer.gd  
- **Purpose**: Renders the maze data as 3D geometry
- **Features**:
  - Creates walls, floor, and exit markers
  - Configurable wall height (3.0m), cell size (2.0m)
  - Materials: gray walls, dark floor, glowing green exit
  - Collision detection for walls
- **Key Methods**: `render_maze()`, `create_wall()`, `create_floor()`

### Development Commands

#### Setting Up Godot Project
1. Open Godot Engine
2. Import or create new project in this directory
3. Set up the scene structure as described above
4. Attach scripts to respective nodes
5. Run the scene to generate and view the maze

#### Script Development
- Scripts follow naming convention: `##_<scriptname>.gd`
- Use tabs for indentation (Godot standard)
- Export variables for easy tweaking in editor

## Performance Considerations

The current implementation generates a 51x51 maze (2,601 cells) which may be intensive for lower-end hardware:
- Each wall cell creates a StaticBody3D with MeshInstance3D and CollisionShape3D
- Consider reducing maze size for performance testing
- Future optimization: use MeshLibrary or procedural mesh generation

## Migration Notes

This project was initially prototyped in Python using pygame but has been migrated to Godot Engine for better 3D capabilities and performance. The Python files remain for reference but are deprecated.