extends Node3D
class_name MazeRenderer

@export var wall_height: float = 5.0
@export var wall_thickness: float = 0.1
@export var cell_size: float = 2.0

var maze_generator: MazeGenerator
var wall_material: StandardMaterial3D
var floor_material: StandardMaterial3D
var exit_material: StandardMaterial3D

func _ready():
	setup_materials()
	maze_generator = get_node("../MazeGenerator")
	if maze_generator:
		call_deferred("render_maze")

func setup_materials():
	# Wall material (gray)
	wall_material = StandardMaterial3D.new()
	wall_material.diffuse_color = Color(0.5, 0.5, 0.5)
	
	# Floor material (dark gray)
	floor_material = StandardMaterial3D.new()
	floor_material.diffuse_color = Color(0.2, 0.2, 0.2)
	
	# Exit material (green)
	exit_material = StandardMaterial3D.new()
	exit_material.diffuse_color = Color(0.0, 1.0, 0.0)
	exit_material.emission_color = Color(0.0, 0.3, 0.0)

func render_maze():
	if not maze_generator or maze_generator.maze.is_empty():
		return
	
	clear_existing_mesh()
	
	var maze = maze_generator.maze
	var width = maze_generator.width
	var height = maze_generator.height
	
	# Create floor
	create_floor(width, height)
	
	# Create walls
	for y in range(height):
		for x in range(width):
			if maze[y][x] == 1:  # Wall
				create_wall(x, y)
			elif maze[y][x] == 2:  # Exit
				create_exit_marker(x, y)

func clear_existing_mesh():
	for child in get_children():
		child.queue_free()

func create_floor(width: int, height: int):
	var floor_mesh = BoxMesh.new()
	floor_mesh.size = Vector3(width * cell_size, 0.1, height * cell_size)
	
	var floor_body = StaticBody3D.new()
	var floor_mesh_instance = MeshInstance3D.new()
	var floor_collision = CollisionShape3D.new()
	var floor_shape = BoxShape3D.new()
	
	floor_shape.size = floor_mesh.size
	floor_mesh_instance.mesh = floor_mesh
	floor_mesh_instance.material_override = floor_material
	floor_collision.shape = floor_shape
	
	floor_body.add_child(floor_mesh_instance)
	floor_body.add_child(floor_collision)
	floor_body.position = Vector3(width * cell_size / 2, -0.05, height * cell_size / 2)
	
	add_child(floor_body)

func create_wall(x: int, y: int):
	var wall_mesh = BoxMesh.new()
	wall_mesh.size = Vector3(cell_size - wall_thickness, wall_height, cell_size - wall_thickness)
	
	var wall_body = StaticBody3D.new()
	var wall_mesh_instance = MeshInstance3D.new()
	var wall_collision = CollisionShape3D.new()
	var wall_shape = BoxShape3D.new()
	
	wall_shape.size = wall_mesh.size
	wall_mesh_instance.mesh = wall_mesh
	wall_mesh_instance.material_override = wall_material
	wall_collision.shape = wall_shape
	
	wall_body.add_child(wall_mesh_instance)
	wall_body.add_child(wall_collision)
	wall_body.position = Vector3(x * cell_size + cell_size / 2, wall_height / 2, y * cell_size + cell_size / 2)
	
	add_child(wall_body)

func create_exit_marker(x: int, y: int):
	var exit_mesh = BoxMesh.new()
	exit_mesh.size = Vector3(cell_size * 0.8, 0.5, cell_size * 0.8)
	
	var exit_body = StaticBody3D.new()
	var exit_mesh_instance = MeshInstance3D.new()
	
	exit_mesh_instance.mesh = exit_mesh
	exit_mesh_instance.material_override = exit_material
	
	exit_body.add_child(exit_mesh_instance)
	exit_body.position = Vector3(x * cell_size + cell_size / 2, 0.25, y * cell_size + cell_size / 2)
	
	add_child(exit_body)

func get_world_position(maze_x: int, maze_y: int) -> Vector3:
	return Vector3(maze_x * cell_size + cell_size / 2, 0, maze_y * cell_size + cell_size / 2)

func get_maze_position(world_pos: Vector3) -> Vector2i:
	var x = int(world_pos.x / cell_size)
	var y = int(world_pos.z / cell_size)
	return Vector2i(x, y)