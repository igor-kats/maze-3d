extends Node3D
class_name MazeGenerator

var maze = []
var width = 11
var height = 11

func _ready():
	generate_maze()
	print("Maze generated!")

func generate_maze():
	# Initialize maze with walls
	maze = []
	for y in range(height):
		var row = []
		for x in range(width):
			row.append(1)  # 1 = wall, 0 = path
		maze.append(row)
	
	# Start from center
	var start_x = width / 2
	var start_y = height / 2
	if start_x % 2 == 0:
		start_x += 1
	if start_y % 2 == 0:
		start_y += 1

	# Generate maze using recursive backtracking
	carve_path(start_x, start_y)
	ensure_starting_area(start_x, start_y)
	add_crossroads()
	create_exit()

func carve_path(x: int, y: int):
	maze[y][x] = 0  # Mark as path
	
	# Get random directions
	var directions = [[0, 2], [2, 0], [0, -2], [-2, 0]]
	directions.shuffle()
	
	for dir in directions:
		var dx = dir[0]
		var dy = dir[1]
		var nx = x + dx
		var ny = y + dy
		
		# Check if new position is valid and unvisited
		if (nx > 0 and nx < width - 1 and 
			ny > 0 and ny < height - 1 and 
			maze[ny][nx] == 1):
			
			# Carve wall between current and next cell
			maze[y + dy / 2][x + dx / 2] = 0
			carve_path(nx, ny)

func ensure_starting_area(start_x: int, start_y: int):
	# Clear 3x3 area around start
	for dy in range(-1, 2):
		for dx in range(-1, 2):
			var new_x = start_x + dx
			var new_y = start_y + dy
			if (new_x >= 0 and new_x < width and new_y >= 0 and new_y < height):
				maze[new_y][new_x] = 0

func add_crossroads():
	var num_passages = (width * height) / 50
	
	for i in range(num_passages):
		for attempt in range(50):
			var x = randi() % (width - 2) + 1
			var y = randi() % (height - 2) + 1
			
			if maze[y][x] == 1:
				var adjacent_paths = 0
				var directions = [[0, 1], [1, 0], [0, -1], [-1, 0]]
				
				for dir in directions:
					var nx = x + dir[0]
					var ny = y + dir[1]
					if (nx >= 0 and nx < width and ny >= 0 and ny < height and maze[ny][nx] == 0):
						adjacent_paths += 1
				
				if adjacent_paths >= 2:
					if randf() < 0.3:
						maze[y][x] = 0
						break

func create_exit():
	var edges = []
	
	# Top and bottom edges
	for x in range(1, width - 1, 2):
		if maze[1][x] == 0:
			edges.append([x, 0])
		if maze[height - 2][x] == 0:
			edges.append([x, height - 1])
	
	# Left and right edges
	for y in range(1, height - 1, 2):
		if maze[y][1] == 0:
			edges.append([0, y])
		if maze[y][width - 2] == 0:
			edges.append([width - 1, y])
	
	if edges.size() > 0:
		var exit_pos = edges[randi() % edges.size()]
		maze[exit_pos[1]][exit_pos[0]] = 2  # 2 = exit

func get_center_position():
	return Vector2(width / 2, height / 2)

func get_exit_position():
	for y in range(height):
		for x in range(width):
			if maze[y][x] == 2:
				return Vector2(x, y)
	return Vector2(0, 0)

func is_wall(x: int, y: int) -> bool:
	if x < 0 or x >= width or y < 0 or y >= height:
		return true
	return maze[y][x] == 1