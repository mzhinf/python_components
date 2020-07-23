from unittest import TestCase

from sqlalchemy import Column, String, Integer

from components.database.sql_utils import SQLUtils

from .. import MAX_RETRIES, fake, logger

CONFIG = {
    'uri': {
        'dialect': 'mysql',
        'driver': 'pymysql',
        'database': 'component',
        'host': 'localhost',
        'port': 3307,
        'username': 'root',
        'password': '123456'
    },
    'echo': False  # log all sql statements
}

db = SQLUtils()


class TestModel(db.Model):
    __tablename__ = 'test_model'

    id = Column(Integer, primary_key=True)
    name = Column(String(50))


class TestSQLUtils(TestCase):

    def setUp(self):
        logger.info('Do setUp()')
        self.table_name = 'test_model'
        self.db = db
        self.db.init_utils(CONFIG)
        self.db.test_connect()
        # Create table
        self.create_table()

    def tearDown(self):
        logger.info('Do tearDown()')
        # Drop tables
        self.db.drop_all()

    def create_table(self):
        # Get current all tables
        pre_all_tables = self.db.get_table_names()
        # Delete the table if it exists, and update pre_all_tables
        if self.table_name in pre_all_tables:
            self.db.drop_tables([self.table_name])
            pre_all_tables = self.db.get_table_names()
        # Create tables
        self.db.create_all()
        # Get all current tables again
        now_all_tables = self.db.get_table_names()
        # Difference tables
        created_tables = set(now_all_tables).difference(set(pre_all_tables))
        self.assertIn(self.table_name, created_tables)

    def test_db_connect(self):
        ret, info = self.db.test_connect()
        self.assertTrue(ret)

    def test_crud(self):
        # Create session
        current_session = self.db.get_session()
        test_list = [TestModel(name=fake.name()) for _ in range(MAX_RETRIES)]
        # - Create -
        for test_model in test_list:
            current_session.add(test_model)
        current_session.commit()
        # - Read -
        data_list = current_session.query(TestModel).order_by(TestModel.id).all()
        for idx, query_data in enumerate(data_list):
            self.assertEqual(query_data, test_list[idx])
        # - Update -
        update_idx = fake.random.randint(0, len(test_list) - 1)
        data = data_list[update_idx]
        data.name = fake.name()
        current_session.commit()
        # check update
        updated_data = current_session.query(TestModel).filter(TestModel.id == data.id).first()
        self.assertEqual(data, updated_data)
        # - Delete -
        delete_idx = fake.random.randint(0, len(test_list) - 1)
        data = data_list[delete_idx]
        current_session.query(TestModel).filter(TestModel.id == data.id).delete()
        current_session.commit()
        # check delete
        updated_data = current_session.query(TestModel).filter(TestModel.id == data.id).first()
        self.assertIsNone(updated_data)
        # Close session
        self.db.remove_session()

    def test_session(self):
        current_session = self.db.get_session()
        self.assertEqual(current_session, self.db.get_session())
        self.db.remove_session()
