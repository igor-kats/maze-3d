extends CharacterBody3D
class_name PlayerController

@export var movement_speed: float = 5.0
@export var mouse_sensitivity: float = 0.002
@export var jump_velocity: float = 4.5

var gravity: float = 9.8
var camera: Camera3D
var points: int = 0

signal points_changed(new_points: int)

func _ready():
	# Capture mouse cursor
	Input.set_mouse_mode(Input.MOUSE_MODE_CAPTURED)
	
	# Get camera reference
	camera = get_node("Camera3D")
	if not camera:
		print("Camera3D not found as child of player!")

func _input(event):
	# Handle mouse look
	if event is InputEventMouseMotion and Input.get_mouse_mode() == Input.MOUSE_MODE_CAPTURED:
		# Rotate player body horizontally (Y axis)
		rotate_y(-event.relative.x * mouse_sensitivity)
		
		# Rotate camera vertically (X axis) with limits
		if camera:
			camera.rotate_x(-event.relative.y * mouse_sensitivity)
			camera.rotation.x = clamp(camera.rotation.x, deg_to_rad(-90), deg_to_rad(90))
	
	# Toggle mouse capture with Escape
	if event.is_action_pressed("ui_cancel"):
		if Input.get_mouse_mode() == Input.MOUSE_MODE_CAPTURED:
			Input.set_mouse_mode(Input.MOUSE_MODE_VISIBLE)
		else:
			Input.set_mouse_mode(Input.MOUSE_MODE_CAPTURED)

func _physics_process(delta):
	# Handle gravity
	if not is_on_floor():
		velocity.y -= gravity * delta
	
	# Handle jump
	if Input.is_action_just_pressed("ui_accept") and is_on_floor():
		velocity.y = jump_velocity
	
	# Handle movement input
	var input_dir = Vector2.ZERO
	if Input.is_action_pressed("ui_right"):
		input_dir.x += 1
	if Input.is_action_pressed("ui_left"):
		input_dir.x -= 1
	if Input.is_action_pressed("ui_down"):
		input_dir.y += 1  
	if Input.is_action_pressed("ui_up"):
		input_dir.y -= 1
	
	# Apply movement relative to player's rotation
	if input_dir != Vector2.ZERO:
		var direction = (transform.basis * Vector3(input_dir.x, 0, input_dir.y)).normalized()
		velocity.x = direction.x * movement_speed
		velocity.z = direction.z * movement_speed
	else:
		velocity.x = move_toward(velocity.x, 0, movement_speed)
		velocity.z = move_toward(velocity.z, 0, movement_speed)
	
	move_and_slide()
	
	# Check for chest collection after movement
	check_chest_collection()

func add_point():
	points += 1
	points_changed.emit(points)
	print("Point collected! Total points: ", points)

func check_chest_collection():
	# Get all Area3D nodes in scene (chests)
	var maze_renderer = get_node("../MazeRenderer")
	if not maze_renderer:
		return
	
	for child in maze_renderer.get_children():
		if child is Area3D and child.name.begins_with("Chest_"):
			var distance = global_position.distance_to(child.global_position)
			if distance < 1.5:  # Collection range
				print("Collecting chest: ", child.name)
				child.queue_free()
				add_point()
				break  # Only collect one chest per frame