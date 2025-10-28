import argparse
from core.game import Game
from interfaces.cli_interface import run_cli
from interfaces.pygame_interface import run_pygame

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=["cli", "pygame"], default="cli")
    args = parser.parse_args()

    game = Game("data/scenarios/pelennor.json")

    if args.mode == "cli":
        run_cli(game)
    else:
        run_pygame(game)
