import argparse
import sys
from track_analyzer.main.commands.analysis_main import analysis_main
from track_analyzer.main.commands.simulation_main import simulation_main


class Arguments(object):
    def __init__(self):
        self.parser = argparse.ArgumentParser(description='Pretends to be a cli.',
                                              usage='blvr-sim <command> [args]\n' +
                                                    "The most commonly used git commands are:\n" +
                                                    "analyze     Create bla bla bla analyze\n" +
                                                    "simulate    Simulates bla bla bla\n")
        self.parser.add_argument('command', help="Subcommand to run")
        args = self.parser.parse_args(sys.argv[1:2])
        if not hasattr(self, args.command):
            print('Unrecognized command')
            self.parser.print_help()
            exit(1)
        # use dispatch pattern to invoke method with same name
        getattr(self, args.command)()

    def analyze(self):
        parser = argparse.ArgumentParser(
            description='analyze results')
        # prefixing the argument with -- means it's optional
        parser.add_argument('file_directory', help="Directory of GPX files to analyze.")
        # now that we're inside a subcommand, ignore the first
        # TWO argvs, ie the command (git) and the subcommand (commit)
        args = parser.parse_args(sys.argv[2:])
        print('Running git commit, amend=%s' % args.amend)
        analysis_main(args.file_directory)

    def simulate(self):
        parser = argparse.ArgumentParser(
            description='analyze results')
        # prefixing the argument with -- means it's optional
        parser.add_argument('--origin_node', help="Node to start simulation")
        parser.add_argument('--distance', help="Distance to start simulation.")
        # now that we're inside a subcommand, ignore the first
        # TWO argvs, ie the command (git) and the subcommand (commit)
        args = parser.parse_args(sys.argv[2:])
        print('Running trackas command: simulate')
        simulation_main(args.origin_node, args.distance)
