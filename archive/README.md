# Archive - Python Prototypes

This folder contains the original Python prototypes that were used during the initial development phase of the 3D Labyrinth Game. These files are **deprecated** and are kept only for historical reference.

## Archived Files

### Core Python Files
- **`main.py`** - Original main entry point for the Python prototype
- **`maze_generator.py`** - Initial maze generation algorithm implementation
- **`player.py`** - Player movement and game logic prototype
- **`renderer_3d.py`** - 3D rendering attempts using pygame
- **`requirements.txt`** - Python dependencies for the prototype

## Migration Status

All functionality from these Python prototypes has been **completely reimplemented** in Godot Engine 4.x using GDScript. The current production implementation is found in the `/scripts/` folder:

- `01_maze_generator.gd` - Replaces `maze_generator.py`
- `02_maze_renderer.gd` - Replaces `renderer_3d.py`  
- `03_player_controller.gd` - Replaces `player.py`
- `04_game_ui.gd` - New UI system (no Python equivalent)

## Why Archived?

The project was migrated from Python/pygame to Godot Engine for several reasons:
- **Better 3D Performance**: Native 3D engine vs pygame 3D simulation
- **Easier Development**: Visual editor and scene system
- **Cross-Platform**: Native builds for multiple platforms
- **Advanced Features**: Built-in physics, materials, lighting, audio

## Usage Warning

⚠️ **These files are not functional and should not be used.** They are incomplete prototypes that were abandoned in favor of the Godot implementation. 

For the current working game, use the GDScript files in `/scripts/` with Godot Engine 4.x.

---

*Last Updated: December 2024*
*Status: Archived - Historical Reference Only*