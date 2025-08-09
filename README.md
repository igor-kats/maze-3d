# 3D Labyrinth Game

A procedurally generated 3D maze escape game built with Godot Engine 4.x.

## Overview

Navigate through a randomly generated 3D labyrinth in first-person view to find the exit. Each maze is unique, featuring procedural generation with recursive backtracking algorithms.

## Features

- **Procedural Maze Generation**: Every playthrough offers a unique maze (default 21x21, scalable to 101x101+)
- **3D First-Person Experience**: Immersive navigation with WASD movement and mouse look controls
- **Procedural Textures**: Stone-like walls and cellular floor patterns using Godot's noise system
- **Collectible System**: Golden chests scattered throughout the maze award points when collected
- **Interactive Gameplay**: Physics-based movement with jumping, collision detection, and scoring
- **Real-time UI**: Points display and responsive user interface
- **Visual Polish**: Glowing exit markers, textured materials, and dynamic lighting

## Current Status

🟢 **Fully Playable** - Complete 3D maze game with all core features

### ✅ Completed
- Iterative maze generation algorithm (supports large mazes without stack overflow)
- 3D maze renderer with procedural textures and materials
- First-person player controller with WASD movement and mouse look
- Physics system with collision detection, gravity, and jumping
- Collectible chest system with points tracking
- Real-time UI displaying current score
- Complete scene structure with proper lighting and environment
- Material system with stone textures, glowing exit, and golden chests

### 🔄 Future Enhancements
- Win condition and level progression system
- Sound effects and ambient audio
- Minimap or navigation aids  
- Multiple difficulty levels and maze variations
- Performance optimizations for very large mazes
- Menu system and game state management

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
   git clone https://github.com/igor-kats/maze-3d.git
   cd maze-3d
   ```
3. Open Godot and import the project
4. Open the main scene and run the project

**Note**: The `archive/` folder contains the original Python prototypes and can be ignored for the Godot implementation.

### Scene Structure Setup
Create the following scene structure:
```
Main (Node3D)
├── WorldEnvironment             → Configure with procedural sky
├── DirectionalLight3D           → Enable shadows
├── MazeGenerator (Node3D)       → Attach scripts/01_maze_generator.gd
├── MazeRenderer (Node3D)        → Attach scripts/02_maze_renderer.gd
├── Player (CharacterBody3D)     → Attach scripts/03_player_controller.gd
│   ├── Camera3D                → Position at (0, 1.8, 0)
│   └── CollisionShape3D        → CapsuleShape3D (height: 1.8, radius: 0.4)
└── GameUI (Control)             → Attach scripts/04_game_ui.gd
```

### Controls
- **WASD** or **Arrow Keys**: Move around
- **Mouse**: Look around (first-person camera)
- **Spacebar**: Jump
- **Escape**: Toggle mouse capture/release

## Performance Notes

The default 21x21 maze creates ~200 wall objects and runs smoothly on most hardware. For different performance needs:

**For better performance:**
1. Reduce maze size in `01_maze_generator.gd`:
   ```gdscript
   var width = 11  # Smaller maze
   var height = 11
   ```

**For larger mazes:**
1. Increase maze size (tested up to 101x101):
   ```gdscript
   var width = 51  # Larger maze
   var height = 51
   ```

**Additional settings:**
- Adjust chest count in MazeRenderer: `@export var chest_count: int = 15`
- Modify wall height: `@export var wall_height: float = 5.0`

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
- Implements iterative backtracking maze generation
- Prevents stack overflow on large mazes (supports 101x101+)
- Creates starting areas and exit placement
- Configurable maze dimensions and complexity

**`02_maze_renderer.gd`** 
- Converts maze data to 3D geometry with procedural textures
- Handles materials, collision shapes, and collectible placement
- Creates stone-textured walls, cellular floor patterns, and golden chests
- Optimized mesh creation and management

**`03_player_controller.gd`**
- First-person movement with WASD controls and mouse look
- Physics-based movement with gravity, jumping, and collision
- Distance-based chest collection system with points tracking

**`04_game_ui.gd`**
- Real-time UI displaying current score
- Signal-based communication with game systems

### Technical Details
- **Maze Algorithm**: Iterative backtracking ensures single-solution paths without stack overflow
- **Rendering**: Individual StaticBody3D nodes per wall for precise collision
- **Materials**: StandardMaterial3D with procedural noise textures, roughness, and metallic properties
- **Collectibles**: Area3D-based chests with distance detection for collection
- **Physics**: CharacterBody3D player with capsule collision and gravity
- **Coordinates**: 2D maze grid mapped to 3D world space (X,Z plane)

## License

[Add your license here]

## Credits

Developed using Godot Engine 4.x. Maze generation inspired by classic recursive backtracking algorithms.