from typing import Optional

from simulation import Simulation
from snake import Snake
from visualize_frame import VisualizeFrame

import os
import argparse
import pygame as pg


def main():
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group()
    group.add_argument("-t", "--train", action="store_const", const=True, default=True)
    group.add_argument("-v", "--test", type=str)

    parser.add_argument("-l", "--save_log", action="store_const", const=True, default=False)
    parser.add_argument("-d", "--display", action="store_const", const=True, default=False)

    args = parser.parse_args()

    simulation: Optional[Simulation] = None
    if args.train:
        simulation = Simulation(save_log=args.save_log)

    if args.test and os.path.isfile(args.test):
        simulation = Simulation()
        try:
            snake = Snake.load(args.test)
            simulation.test_snake(snake)
        except:
            print("Error: Invalid file")
            return

    if args.display:
        pg.init()
        pg.display.set_caption("Angry Jack Visualization")
        frame = VisualizeFrame(simulation)
        frame.run()
    else:
        simulation.run_simulation()


if __name__ == "__main__":
    main()
