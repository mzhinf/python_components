from unittest import TestCase

from components.sftp.sftp_utils import SFTPUtils

CONFIG = {
    'hostname': 'localhost',
    'port': 2222,
    'username': 'root',
    'password': '123456'
}


class TestSFTPUtils(TestCase):

    def setUp(self):
        self.sftp = SFTPUtils(**CONFIG)

    def test_sftp_tree(self):
        self.sftp.connect_sftp()
        tree = self.sftp.sftp_tree()
        self.sftp.close_sftp()
        out_put = '\n' + '\n'.join(tree) + '\n'
        print(out_put)
