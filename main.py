import random


class Direction:
    UP = "UP"
    DOWN = "DOWN"
    LEFT = "LEFT"
    RIGHT = "RIGHT"


class Position:
    MAX_X: int = 0
    MAX_Y: int = 0

    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    def get_pos(self) -> tuple:
        return self.x, self.y

    def update_pos(self, x: int, y: int):
        # print(f"from {(self.x, self.y)} move to {(x, y)}")
        self.x = x
        self.y = y

    @classmethod
    def random_position(cls, ):
        random_x = random.randint(0, Position.MAX_X - 1)
        random_y = random.randint(0, Position.MAX_Y - 1)
        return Position(random_x, random_y)

    @classmethod
    def config(self, max_x: int = 100, max_y: int = 100) -> None:
        """
        configuration of the border
        :param max_x:
        :param max_y:
        :return: None
        """
        Position.MAX_X = max_x
        Position.MAX_Y = max_y

    def __repr__(self):
        return f"position (x: {self.x},y: {self.y})"


class Food:
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

    def __repr__(self):
        return f"Food: {id(self)} at {self.pos}"


class Snake:
    UNIT = 5

    def __init__(self):
        self.head_pos: Position = Position.random_position()
        self.bodies: [Position] = [self.head_pos]
        self.length = len(self)
        self.directions: [str] = [Direction.UP]

    def __len__(self):
        return len(self.bodies)

    def move_up(self):
        for body in self.bodies:
            body.update_pos(body.x, body.y + Snake.UNIT)

    def move_down(self):
        for body in self.bodies:
            body.update_pos(body.x, body.y - Snake.UNIT)

    def move_right(self):
        for body in self.bodies:
            body.update_pos(body.x + Snake.UNIT, body.y)

    def move_left(self):
        for body in self.bodies:
            body.update_pos(body.x - Snake.UNIT, body.y)

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


class GameMap:
    def __init__(self, border_width, border_height, unit):
        self.border_width = border_width
        self.snake: Snake = border_height
        self.unit = unit
class Game:
    def __init__(self, border_width, border_height, grid_length):
        self.game_map = GameMap(border_width, border_height, grid_length)
        self.snake: Snake = Snake()
        self.foods: list[Food] = []

    def check_status(self):
        pass

    def game_init(self):
        self.foods.append(Food.new_food())


def main():
    snake = Snake()
    status = "start"
    game = Game()
    while status != "stop":
        status = game.check_status()


if __name__ == "main":
    main()
