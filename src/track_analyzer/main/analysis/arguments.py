from argparse import ArgumentParser


class Arguments:
    def __init__(self):
        self.parser = ArgumentParser(description='Analyze trackfiles and store information in MongoDB.')
        self.parser.add_argument("--file_directory", help="Directory of GPX files to analyze.")

    def get_file_directory(self):
        args = self.parser.parse_args()
        return args.file_directory
