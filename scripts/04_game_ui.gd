extends Control
class_name GameUI

@onready var points_label: Label
var player: PlayerController

func _ready():
	# Create UI elements
	create_ui()
	
	# Find player and connect signal
	player = get_node("../Player")
	if player:
		player.points_changed.connect(_on_points_changed)
		_on_points_changed(0)  # Initialize display

func create_ui():
	# Create points label
	points_label = Label.new()
	points_label.text = "Points: 0"
	points_label.position = Vector2(20, 20)
	points_label.size = Vector2(200, 50)
	
	# Style the label
	var font = ThemeDB.fallback_font
	var font_size = 24
	points_label.add_theme_font_override("font", font)
	points_label.add_theme_font_size_override("font_size", font_size)
	points_label.add_theme_color_override("font_color", Color.WHITE)
	points_label.add_theme_color_override("font_shadow_color", Color.BLACK)
	points_label.add_theme_constant_override("shadow_offset_x", 2)
	points_label.add_theme_constant_override("shadow_offset_y", 2)
	
	add_child(points_label)

func _on_points_changed(new_points: int):
	if points_label:
		points_label.text = "Points: " + str(new_points)