import pandas as pd
from src.sql.sql_settings import postgresql as settings
from sqlalchemy import Table, Column, MetaData, Integer, String
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from typing import Dict


class CompoundConnection:
    def __init__(self):
        """Defining the class values and creating data table
        """
        self.meta = MetaData()

        self.compounds_table = Table("compounds", self.meta,
                                     Column("compound", String, primary_key=True),
                                     Column('name', String, nullable=False),
                                     Column('formula', String, nullable=False),
                                     Column('inchi', String, nullable=False),
                                     Column('inchi_key', String, nullable=False),
                                     Column('smiles', String, nullable=False),
                                     Column('cross_links_count', Integer, nullable=False))

        self.engine = self._get_engine()
        self.connection = None

    def start_connection(self):

        if self.connection is None:
            self.connection = self.engine.connect()

    def insert_values(self, values: Dict[str, str]) -> bool:
        """Inserting values into database

        Args:
          values (dict of [str, str]): compounds(s) name(s)

        Returns:
          information if value was inserted or not
        """
        self.start_connection()

        # check if compound already exists
        query = self.compounds_table.select().where(self.compounds_table.c.compound == values["compound"])
        query_res = self.connection.execute(query)
        if not query_res.rowcount:
            query = self.compounds_table.insert().values(**values)
            self.connection.execute(query)
            return True

        return False

    def _get_engine(self) -> Engine:
        keys = ['pguser', 'pgpasswd', 'pghost', 'pgport', 'pgdb']
        if not all(key in keys for key in settings.keys()):
            raise Exception('Bad config file')

        engine = CompoundConnection._create_engine(settings['pguser'],
                                                   settings['pgpasswd'],
                                                   settings['pghost'],
                                                   settings['pgport'],
                                                   settings['pgdb'])

        self.meta.create_all(engine)
        return engine

    @staticmethod
    def _create_engine(user: str, passwd: str, host: str, port: int, db: str) -> Engine:
        url = f"postgresql://{user}:{passwd}@{host}:{port}/{db}"
        engine = create_engine(url)
        return engine

    def show_table(self):
        self.start_connection()
        query = self.compounds_table.select()
        query_res = self.connection.execute(query)

        df = pd.DataFrame(query_res.fetchall())
        df.columns = query_res.keys()
        df = df.applymap(lambda x: x[:10]+'...' if len(str(x)) > 10 else x)
        print(df)
