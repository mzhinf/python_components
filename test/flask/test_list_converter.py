import sys
from unittest import TestCase

from flask import Flask

from .. import fake, MAX_RETRIES, logger
from components.flask.list_converter import ListConverter


class TestListConverter(TestCase):

    def setUp(self):
        self.app = Flask(__name__)
        # Add list converter to flask app
        self.app.url_map.converters['list'] = ListConverter

        @self.app.route('/get_error')
        def get_error():
            try:
                raise Exception('Raise error')
            except Exception as error:
                self.app.logger.error('Unhandled exception. Error: %s', error, exc_info=sys.exc_info())
            return ''

        @self.app.route('/list_plus/<list:value_list>/')
        def list1(value_list):
            return 'Separator: {} {}'.format('+', value_list)

        @self.app.route('/list_or/<list(separator="|"):value_list>/')
        def list2(value_list):
            return 'Separator: {} {}'.format('|', value_list)

        @self.app.route('/')
        def index():
            return {'message': 'Hello World!'}, 200, [('X-Request-Id', '100')]

        self.ctx = self.app.app_context()
        self.ctx.push()
        self.client = self.app.test_client()

    def get(self, url):
        """ Mock get request """
        response = self.client.get(url)
        body = response.get_data(as_text=True)
        return body, response.status_code, response.headers

    def test_list_converter(self):
        """ Test all list converter """

        def test_a_single_case(join_type, base_url):
            """
            Test a single list converter

            :param join_type: str. '+', '|' and so on
            :param base_url: str. ListConverter base url for flask
                e.g
                route: @self.app.route('/list1/<list:value_list>/')
                base_url: '/list1'
            :return:
            """
            for count in range(1, MAX_RETRIES):
                # Use Faker to generate test data
                name_list = [fake.name() for _ in range(count)]
                name_str = join_type.join(name_list)
                url = '{}/{}/'.format(base_url, name_str)
                get_ret = 'Separator: {} {}'.format(join_type, name_list)
                body, code, headers = self.get(url)
                self.assertEqual(get_ret, body)
                logger.info('%s %s %s', body, code, headers)

        for join_type, base_url in [('+', '/list_plus'), ('|', '/list_or')]:
            test_a_single_case(join_type, base_url)

        self.get('/get_error')
