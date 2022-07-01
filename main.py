import time
import requests
import argparse
import logging
import logging.config
from config import COMPOUNDS, URL


def get_compound_info(c: str) -> dict:
    """makes request for URL and return this information

    Args:
      c (str): compound name

    Returns:
      information of compound as dictionary
    """

    x = requests.get(f"{URL}{c}").json()
    x = x[c][0]

    return {"compound": c,
            "name": x["name"],
            "formula": x["formula"],
            "inchi": x["inchi"],
            "inchi_key": x["inchi_key"],
            "smiles": x["smiles"],
            "cross_links_count": len(x["cross_links"])}


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

    for compound in compounds:
        if compound not in COMPOUNDS:
            logger.warning(f'compound {compound} is not available')
            continue

        print(get_compound_info(compound)["name"])
        logger.info(f'request for compound {compound}')
        time.sleep(1)
