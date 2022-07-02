import argparse
import logging.config
from src.config import COMPOUNDS
from src.pipeline import Pipeline


if __name__ == "__main__":
    my_parser = argparse.ArgumentParser()

    # Add the arguments
    my_parser.add_argument('-c',
                           '--compounds',
                           nargs='+',
                           help=f'compound names from this list {COMPOUNDS}')

    # retrieve arguments
    compounds = my_parser.parse_args().compounds
    compounds = COMPOUNDS if compounds is None else compounds  # scrape all compounds as default

    # create logger
    logging.config.fileConfig(fname='log.conf')
    logger = logging.getLogger('root')

    # run pipeline
    pipeline = Pipeline(compounds, logger)
    pipeline.run()
