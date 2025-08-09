# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a 3D Labyrinth Game built using the Godot Engine. The project creates a procedurally generated maze that players can navigate in first-person 3D view to find the exit.

**Current Status**: Fully playable 3D maze game with first-person controls, procedural textures, and collectible chest system.

## Development Environment

### Engine Requirements
- **Godot Engine 4.x** (recommended: latest stable version)
- Cross-platform development (Windows, macOS, Linux)

### Project Structure
```
maze-3d/
├── scripts/                      # GDScript files (production)
│   ├── 01_maze_generator.gd     # Procedural maze generation
│   ├── 02_maze_renderer.gd      # 3D maze visualization
│   ├── 03_player_controller.gd  # First-person player controls
│   └── 04_game_ui.gd           # User interface system
├── archive/                      # Deprecated Python prototypes
│   ├── main.py                  # Original Python main
│   ├── maze_generator.py        # Python maze generation
│   ├── player.py                # Python player logic
│   ├── renderer_3d.py           # Python 3D rendering
│   └── requirements.txt         # Python dependencies
├── CLAUDE.md                    # This file
├── README.md                    # Project documentation
├── ROADMAP.md                   # Development roadmap
└── LICENSE                      # Project license
```

## Current Implementation

### Godot Scene Structure
```
Main (Node3D)
├── WorldEnvironment            # Environment settings with procedural sky
├── DirectionalLight3D          # Scene lighting with shadows
├── MazeGenerator (Node3D)      # With 01_maze_generator.gd script
├── MazeRenderer (Node3D)       # With 02_maze_renderer.gd script
├── Player (CharacterBody3D)    # With 03_player_controller.gd script
│   ├── Camera3D               # First-person camera
│   └── CollisionShape3D       # Player collision (CapsuleShape3D)
└── GameUI (Control)            # With 04_game_ui.gd script
```

### Completed Scripts

#### 01_maze_generator.gd
- **Purpose**: Generates procedural mazes using iterative backtracking
- **Features**:
  - Configurable maze grid (default: 21x21, supports up to 101x101+)
  - Iterative algorithm prevents stack overflow on large mazes
  - Ensures connected paths from center to edges
  - Creates starting area and random exit placement
  - Adds crossroads for more interesting navigation
- **Key Methods**: `generate_maze()`, `carve_path()`, `create_exit()`

#### 02_maze_renderer.gd  
- **Purpose**: Renders the maze data as 3D geometry with materials
- **Features**:
  - Creates walls, floor, exit markers, and collectible chests
  - Configurable parameters: wall height (5.0m), cell size (2.0m)
  - Procedural noise textures: stone walls, cellular floor patterns
  - Materials: textured walls, dark floor, glowing green exit, golden chests
  - Collision detection for all objects
  - Random chest placement (15 chests by default)
- **Key Methods**: `render_maze()`, `create_wall()`, `create_floor()`, `create_chest()`

#### 03_player_controller.gd
- **Purpose**: First-person player movement and interaction
- **Features**:
  - WASD movement with mouse look controls
  - Physics-based movement with gravity and jumping
  - Collision detection with walls
  - Distance-based chest collection system
  - Points tracking and scoring
  - Mouse capture/release with Escape key
- **Key Methods**: `_physics_process()`, `check_chest_collection()`, `add_point()`

#### 04_game_ui.gd
- **Purpose**: User interface and HUD display
- **Features**:
  - Real-time points display in top-left corner
  - Clean UI styling with shadows and proper fonts
  - Signal-based communication with player controller
- **Key Methods**: `create_ui()`, `_on_points_changed()`

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

The current implementation supports large mazes (tested up to 101x101) but performance depends on maze size:
- Each wall cell creates a StaticBody3D with MeshInstance3D and CollisionShape3D
- Default 21x21 maze (~200 walls) runs smoothly on most hardware
- 101x101 maze (~5,000 walls) may impact performance on lower-end devices
- Iterative maze generation prevents stack overflow on any maze size
- Procedural textures are generated once and cached for performance

## Migration Notes

This project was initially prototyped in Python using pygame but has been migrated to Godot Engine for better 3D capabilities and performance. The original Python prototype files have been moved to the `archive/` folder for reference but are no longer maintained or used in the current implementation.