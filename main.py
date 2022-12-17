import random
class Direction:
    UP = "UP"
    DOWN = "DOWN"
    LEFT = "LEFT"
    RIGHT = "RIGHT"

class GameMap:
    def __init__(self, map_width: int, map_height: int, unit: int):
        self.map_width: int = map_width
        self.map_height: int = map_height
        self.unit: int = unit
        self.grid_width: int = self.map_width // self.unit
        self.grid_height: int = self.map_height // self.unit

class Position:
    game_map: GameMap
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y
        self.grid_x = self.x * Position.game_map.unit
        self.grid_y = self.y * Position.game_map.unit
    def get_pos(self) -> tuple:
        return self.x, self.y,
    def get_gird_pos(self) -> tuple:
        return self.grid_x, self.grid_y,

    def update_pos(self, x: int, y: int):
        self.x = x
        self.y = y
        self.grid_x = self.x * Position.game_map.unit
        self.grid_y = self.y * Position.game_map.unit

    @classmethod
    def random_position(cls, ):
        random_x = random.randint(0, Position.game_map.grid_width - 1) // cls.game_map.unit
        random_y = random.randint(0, Position.game_map.grid_height - 1) // cls.game_map.unit
        return Position(random_x, random_y)
    @classmethod
    def setting(cls, game_map: GameMap):
        cls.game_map = game_map

    def __repr__(self):
        return f"position (x: {self.x},y: {self.y})"

class Food:
    game_map: GameMap
    def __init__(self):
        self.food_type = "default"  # for skilled food
        self.pos = Position.random_position()

    def be_eaten(self, snake):
        print(f"food {self} is eaten by {snake}")

    @classmethod
    def new_food(cls):
        f = Food()
        print(f"Generate new food: {f}")
        return f

    @classmethod
    def setting(cls, game_map: GameMap):
        cls.game_map: GameMap = game_map

    def __repr__(self):
        return f"Food: {id(self)} at {self.pos}"


class Snake:
    game_map: GameMap
    def __init__(self):
        self.head_pos: Position = Position.random_position()
        self.bodies: [Position] = [self.head_pos]
        self.length = len(self)
        self.directions: [str] = [Direction.UP]

    def __len__(self):
        return len(self.bodies)

    def move_up(self):
        for body in self.bodies:
            body.update_pos(body.x, body.y + Snake.game_map.unit)

    def move_down(self):
        for body in self.bodies:
            body.update_pos(body.x, body.y - Snake.game_map.unit)

    def move_right(self):
        for body in self.bodies:
            body.update_pos(body.x + Snake.game_map.unit, body.y)

    def move_left(self):
        for body in self.bodies:
            body.update_pos(body.x - Snake.game_map.unit, body.y)

    def moving(self):
        for next_direction in self.directions:

            if next_direction == Direction.UP:
                self.move_up()

            if next_direction == Direction.DOWN:
                self.move_down()

            if next_direction == Direction.LEFT:
                self.move_left()

            if next_direction == Direction.RIGHT:
                self.move_right()

            status = self.check_vaild()

    @classmethod
    def setting(cls,game_map: GameMap):
        cls.game_map: GameMap = game_map



class Game:
    def __init__(self, max_width, max_height, unit):
        self.game_map = GameMap(max_width, max_height, unit)
        Position.setting(self.game_map)
        Snake.setting(self.game_map)
        Food.setting(self.game_map)
        self.snake: Snake = Snake()
        self.foods: list[Food] = []

    def check_status(self):
        pass

    def game_init(self):
        self.foods.append(Food.new_foogit)

    def move(self, direction: str):
        self.snake.directions.append(direction)



def main():
    BORDER_WIDTH = 100
    game = Game()


if __name__ == "main":
    main()
