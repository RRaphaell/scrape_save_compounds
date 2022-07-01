from sql_settings import postgresql as settings
from sqlalchemy import Table, Column, MetaData, Integer, String
from sqlalchemy import create_engine


class CompoundConnection:
    def __init__(self):
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
        self.connection = self.engine.connect()

    def insert_values(self, values: dict):
        if self.connection is None:
            self.start_connection()

        # check if compound already exists
        query = self.compounds_table.select().where(self.compounds_table.c.compound == values["compound"])
        query_res = self.connection.execute(query)
        if not query_res.rowcount:
            query = self.compounds_table.insert().values(**values)
            self.connection.execute(query)
            return True

        return False

    def _get_engine(self):
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
    def _create_engine(user, passwd, host, port, db):
        url = f"postgresql://{user}:{passwd}@{host}:{port}/{db}"
        engine = create_engine(url)
        return engine
