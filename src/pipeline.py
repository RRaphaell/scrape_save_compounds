import time
import requests
from src.config import URL, COMPOUNDS, DELAY
from src.sql.sql_conneciton import CompoundConnection


class Pipeline:
    def __init__(self, compounds, logger):
        self.compounds = compounds
        self.logger = logger

    def run(self):
        compound_connection = CompoundConnection()

        for compound in self.compounds:
            if compound not in COMPOUNDS:
                self.logger.warning(f'compound {compound} is not available')
                continue

            compound_info = self._get_compound_info(compound)
            success = compound_connection.insert_values(compound_info)
            if success:
                self.logger.info(f'request for compound {compound}')
            else:
                self.logger.warning(f'request for compound {compound} is denied, because it already exists')

            time.sleep(DELAY)

    def _get_compound_info(self, c: str) -> dict:
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


