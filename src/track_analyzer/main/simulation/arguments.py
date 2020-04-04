from argparse import ArgumentParser


class Arguments:
    def __init__(self):
        self.parser = ArgumentParser(description='Process graph data and simulate a route with the information.')
        self.parser.add_argument("--origin", help="Start point of the simulation.")
        self.parser.add_argument("--distance", help="Distance to simulate.")

    def get_origin_node(self):
        args = self.parser.parse_args()
        return args.origin

    def get_distance(self):
        args = self.parser.parse_args()
        return args.distance
