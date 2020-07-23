import io
from stat import S_ISDIR

import paramiko

from components.utils.logger import get_logger


logger = get_logger()


class SFTPUtils:

    def __init__(self, hostname, port, username, password=None, publickey=None, privatekey=None):
        self.hostname = hostname
        self.port = port
        self.username = username
        self.password = password
        self.publickey = publickey
        self.privatekey = privatekey
        self.transport = None
        self.sftp = None

    def connect_sftp(self):
        try:
            self.transport = paramiko.Transport((self.hostname, self.port))
            if self.password is not None:
                self.transport.connect(username=self.username, password=self.password)
            else:
                pkey = paramiko.RSAKey.from_private_key(io.StringIO(self.privatekey))
                self.transport.connect(username=self.username, pkey=pkey)
            self.sftp = paramiko.SFTPClient.from_transport(self.transport)
        except Exception as e:
            logger.error('Connect sftp error: %s', e)
            raise e

    def close_sftp(self):
        if self.sftp is not None:
            try:
                self.sftp.close()
            except Exception as e:
                logger.error('Close sftp error: %s', e)
            finally:
                self.sftp = None
        if self.transport is not None:
            try:
                self.transport.close()
            except Exception as e:
                logger.error('Close transport error: %s', e)
            finally:
                self.transport = None

    def sftp_sub_tree(self, path, pre_start_str, layers):
        sub_tree = list()
        file_list = self.sftp.listdir_attr(path)
        for idx, entry in enumerate(file_list):
            mode = entry.st_mode
            filename = entry.filename
            if idx == len(file_list) - 1:
                start_str = '└─ '
                sub_st_type = pre_start_str + '    '
            else:
                start_str = '├─ '
                sub_st_type = pre_start_str + '│  '
            sub_tree.append('{}{}{}'.format(pre_start_str, start_str, filename))
            if S_ISDIR(mode):
                sub_path = filename if path == '.' else '{}/{}'.format(path, filename)
                tree = self.sftp_sub_tree(sub_path, sub_st_type, layers + 1)
                sub_tree.extend(tree)
        return sub_tree

    def sftp_tree(self, path='.'):
        main_tree = list()
        file_list = self.sftp.listdir_attr(path)
        for idx, entry in enumerate(file_list):
            mode = entry.st_mode
            filename = entry.filename
            if idx == len(file_list) - 1:
                start_str = '└─ '
                sub_start_str = '    '
            else:
                start_str = '├─ '
                sub_start_str = '│  '
            main_tree.append('{}{}'.format(start_str, filename))
            if S_ISDIR(mode):
                sub_path = filename if path == '.' else '{}/{}'.format(path, filename)
                tree = self.sftp_sub_tree(sub_path, sub_start_str, 1)
                main_tree.extend(tree)
        return main_tree
