import argparse
import sys
from track_simulator.main.commands.analysis_main import analysis_main
from track_simulator.main.commands.simulation_main import simulation_main


class Arguments(object):
    def __init__(self):
        self.parser = argparse.ArgumentParser(
            description='TrackSimulator CLI. Analyze, simulate and generate GPX tracks',
            usage='blvr-sim <command> [args]\n' +
                  "The most commonly used git commands are:\n" +
                  "analyze Analyze GPX tracks, generate results and store information"
                  "in mongoDB\n" +
                  "simulate Generate track given analysis information stored in mongoDB\n")
        self.parser.add_argument('command', help="Subcommand to run")
        args = self.parser.parse_args(sys.argv[1:2])
        if not hasattr(self, args.command):
            print('Unrecognized command')
            self.parser.print_help()
            exit(1)
        # use dispatch pattern to invoke method with same name
        getattr(self, args.command)()

    def analyze(self):
        """
        Method from Arguments to analyze tracks. It runs analysis_main passing parameters.
        """
        parser = argparse.ArgumentParser(
            description='analyze results')
        parser.add_argument('file_directory', help="Directory path of GPX files to analyze.")
        parser.add_argument('--north_component', help="North component of limited area.")
        parser.add_argument('--south_component', help="South component of limited area.")
        parser.add_argument('--east_component', help="East component of limited area.")
        parser.add_argument('--west_component', help="West component of limited area.")
        args = parser.parse_args(sys.argv[2:])
        print("Running git commit, analysis. Route: '{0}'".format(args.file_directory))
        analysis_main(args.file_directory, args.north_component, args.south_component, args.east_component,
                      args.west_component)

    def simulate(self):
        """
        Method from Arguments to simulate tracks. It runs simulation_main passing arguments.
        """
        parser = argparse.ArgumentParser(
            description='analyze results')
        # prefixing the argument with -- means it's optional
        parser.add_argument('-distance', help="Distance to start simulation.")
        parser.add_argument('--north_component', help="North component of limited area.")
        parser.add_argument('--south_component', help="South component of limited area.")
        parser.add_argument('--east_component', help="East component of limited area.")
        parser.add_argument('--west_component', help="West component of limited area.")
        parser.add_argument('--origin_node', help='Node to start simulation.')
        parser.add_argument('--data', help="Data to import from database. (Graph_Analysis_mm-dd-YYYY)")
        parser.add_argument('--quantity', help="Number of tracks to generate.")
        args = parser.parse_args(sys.argv[2:])
        simulation_main(args.origin_node, args.distance, args.data, args.quantity, args.north_component, args.south_component, args.east_component,
                      args.west_component)
