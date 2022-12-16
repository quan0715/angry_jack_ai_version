import random

class Position:
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
    def random_position(cls, max_x: int = 0, max_y: int = 100):
        random_x = random.randint(0, max_x)
        random_y = random.randint(0, max_y)
        return Position(random_x, random_y)

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
    pass


class Game:
    X_MAX = 100
    Y_MAX = 100
    def __init__(self):
        self.snake: Snake = Snake()

    def check_status(self):
        pass

    def game_init(self):
        food = Food.new_food()


def main():
    snake = Snake()
    status = "start"
    game = Game()
    while status != "stop":

        status = game.check_status()


if __name__ == "main":
    main()