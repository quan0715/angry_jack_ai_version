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
    group.add_argument("-i", "--inherit", type=str)

    parser.add_argument("-l", "--save_log", action="store_const", const=True, default=False)
    parser.add_argument("-d", "--display", action="store_const", const=True, default=False)

    args = parser.parse_args()

    simulation: Optional[Simulation] = None
    if args.train:
        if args.inherit:
            if os.path.isfile(file_path:=('resources/' + args.inherit + '.pkl')):
                try:
                    snake = Snake.load(file_path)
                except:
                    print("Error: Invalid file")
                    return
            else:
                print("Error: No file found for " + file_path)
                return
            simulation = Simulation(save_log=args.save_log, init_snake=snake)
        else:
            simulation = Simulation(save_log=args.save_log)

    if args.test:
        if os.path.isfile(file_path:=('resources/' + args.test + '.pkl')):
            simulation = Simulation()
            try:
                snake = Snake.load(file_path)
                simulation.test_snake(snake)
            except:
                print("Error: Invalid file")
                return
        else:
            print("Error: No file found for " + file_path)
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
