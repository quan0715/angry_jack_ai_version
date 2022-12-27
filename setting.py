from typing import Tuple
from pygame import Color
class GameConfig:
    background_color = Color("#5C5C5C")  # the background color
    head_color: Color = Color("#FFC645")  # the color of snake head
    tail_color: Color = Color("#FFDF96")  # the color of snake tail(body)
    food_color: Color = Color("#93FFAB")  # the color of default food
    line_color: Color = Color("#FFFFFF")  # the color of auxiliary line
    map_max_width: int = 400  # the maximum value of the border width (Cartesian coordinate)
    map_max_height: int = 400  # the maximum value of the height width
    grid_width: int = 20  # the value of the grid width (rectangle)
    grid_max_width: int = map_max_width // grid_width  # Cartesian coordinate which unit equals to grid_with
    grid_max_height: int = map_max_height // grid_width

class GUIConfig:
    main_window_size: Tuple[int, int] = (900, 600)
    network_window_size: Tuple[int, int] = (450, 560)
    label_screen_size: tuple[int, int] = (400, 150)
    snake_game_display_pos: tuple[int, int] = (480, 20)
    neural_screen_pos: tuple[int, int] = (20, 20)
    label_size = 20
    first_node_pos = (10, 10)
    node_space = 1
    node_size = 8 # node radius
    line_width = 1
    font_family = 'ChivoMono-Medium.ttf'
    background_color = Color("#000000") # black
    label_color = Color("#FFFFFF") # white
    text_color = Color("#FFFFFF") # white
    testing_color = Color("#5C5C5C") # gray
    node_not_active_color = Color('#FFFFFF') # white
    node_active_color = Color('#79FF79') # green
    node_boarder_color = Color('#272727') # black
    line_not_active_color = Color('#80FFFF') # light blue
    line_active_color = Color('#FF0000') # red

class NetworkConfig:
    layers_node_num = [32, 20, 12, 4]