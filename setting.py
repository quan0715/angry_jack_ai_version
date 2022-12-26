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
    window_width: int = 900
    window_height: int = 600
    network_window_width: int = 450
    network_window_height: int = 560
    snake_game_display_pos = (480, 20)
    neural_screen_pos = (20, 20)
    background_color = Color("#000000")
    label_color = Color("#FFFFFF")
    text_color = Color("#FFFFFF")
    testing_color = Color("#5C5C5C")
    label_size = 20
    first_node_pos = (10, 10)
    node_space = 1
    layer_space = 120
    node_not_active_color = Color('#FFFFFF')
    node_active_color = Color('#79FF79')
    node_boarder_color = Color('#272727')
    node_size = 8
    line_not_active_color = Color('#80FFFF')
    line_active_color = Color('#FF0000')
    line_width = 1

class NetworkConfig:
    layers_node_num = [32, 20, 12, 4]