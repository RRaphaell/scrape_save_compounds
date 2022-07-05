import argparse
from src.config import COMPOUNDS
from src.pipeline import Pipeline


def create_parser():
    parser = argparse.ArgumentParser()

    # Add the arguments
    parser.add_argument('-c',
                        '--compounds',
                        nargs='+',
                        help=f'compound names from this list {COMPOUNDS}')
    parser.add_argument('-t',
                        '--table',
                        nargs='?',
                        const=True,
                        default=False,
                        help=f'print table')

    return parser


if __name__ == "__main__":
    arg_parser = create_parser()

    # retrieve arguments
    compounds = arg_parser.parse_args().compounds
    show_table = arg_parser.parse_args().table

    # run pipeline
    pipeline = Pipeline(compounds)
    if show_table:
        pipeline.compound_connection.show_table()
    else:
        pipeline.run()
