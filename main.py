import argparse
from src.config import COMPOUNDS
from src.pipeline import Pipeline


if __name__ == "__main__":
    my_parser = argparse.ArgumentParser()

    # Add the arguments
    my_parser.add_argument('-c',
                           '--compounds',
                           nargs='+',
                           help=f'compound names from this list {COMPOUNDS}')
    my_parser.add_argument('-t',
                           '--table',
                           nargs='?',
                           const=True,
                           default=False,
                           help=f'print table')

    # retrieve arguments
    compounds = my_parser.parse_args().compounds
    show_table = my_parser.parse_args().table

    # run pipeline
    pipeline = Pipeline(compounds)
    if show_table:
        pipeline.compound_connection.show_table()
    else:
        pipeline.run()
