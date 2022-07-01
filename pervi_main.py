from sqlalchemy.orm import sessionmaker
from local_settings import postgresql as settings
from sqlalchemy import Table, Column, MetaData, Integer, Computed, Identity, String
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base


def get_engine(user, passwd, host, port, db):
    url = f"postgresql://{user}:{passwd}@{host}:{port}/{db}:"
    engine = create_engine(url, pool_size=50, echo=False)
    return engine


def get_engine_from_settings():
    keys = ['pguser', 'pgpasswd', 'pghost', 'pgport', 'pgdb']
    if not all(key in keys for key in settings.keys()):
        raise Exception('Bad config file')

    return get_engine(settings['pguser'],
                      settings['pgpasswd'],
                      settings['pghost'],
                      settings['pgport'],
                      settings['pgdb'])


def get_session():
    inner_engine = get_engine_from_settings()
    inner_session = sessionmaker(bind=inner_engine)()
    return inner_session


Base = declarative_base()

class CompoundData(Base):
    __tablename__ = "compound_data"

    compound = Column(String, primary_key=True)
    name = Column(String)

    def __str__(self):
        return f'{self.compound}: {self.name}'


# engine = get_engine_from_settings()
# Base.metadata.create_all(engine)

# session = get_session()
# session.close()
# engine = session.get_bind()
# engine.dispose()


# meta = MetaData()
#
# data = Table(
#     "data",
#     meta,
#     Column('id', Integer, Identity(start=42, cycle=True), primary_key=True),
#     Column('data_zoro', String)
# )
#
# engine = get_engine_from_settings()
# meta.create_all(engine)
#
# conn = engine.connect()
# query_1 = data.insert(1,"Rame")
# conn.execute(query_1)
