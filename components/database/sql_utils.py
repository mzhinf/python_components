from sqlalchemy import create_engine
from sqlalchemy.engine import reflection
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker

DB_URI_FORMAT = '{dialect}+{driver}://{username}:{password}@{host}:{port}/{database}'


class SQLUtils:

    def __init__(self, config=None):
        self.engine = None
        self.session = None
        self.Model = declarative_base()
        if config:
            self.init_utils(config)

    def init_utils(self, config):
        """
        Create engine and session

        :param config:
        :return:
        """
        if 'uri' not in config:
            raise ValueError('Missing uri in config')
        else:
            uri = DB_URI_FORMAT.format(**config['uri'])

        engine_config = config.copy()
        engine_config.pop('uri')

        if 'pool_size' not in engine_config:
            engine_config['pool_size'] = 10
        if 'pool_recycle' not in engine_config:
            engine_config['pool_recycle'] = 7200

        self.engine = create_engine(uri, **engine_config)
        self.session = scoped_session(sessionmaker(bind=self.engine))

    def test_connect(self):
        """ Test db connect. Usually used for health check """
        result = True
        output = 'Database connection is OK.'
        try:
            session = self.session()
            session.execute('SELECT 1')
        except Exception as error:
            result = False
            output = str(error)
        return result, output

    def create_all(self):
        """ Create tables by sqlalchemy create_all """
        self.Model.metadata.create_all(self.engine)

    def drop_all(self):
        """ Drop tables sqlalchemy drop_all """
        self.Model.metadata.drop_all(self.engine)

    def create_tables(self, table_list):
        """ Create tables by sql """
        if table_list:
            session = self.session()
            for sql in table_list:
                session.execute(sql)

    def drop_tables(self, table_list):
        """ Drop tables by sql """
        if table_list:
            drop_sql = 'DROP TABLE IF EXISTS `{}`'
            sql_list = [drop_sql.format(table) for table in table_list]
            session = self.session()
            for sql in sql_list:
                session.execute(sql)

    def get_table_names(self):
        insp = reflection.Inspector.from_engine(self.engine)
        return insp.get_table_names()

    def get_session(self):
        # TODO: check get session by this way
        return self.session()

    def remove_session(self):
        # TODO: check remove session by this way
        return self.session.remove()
