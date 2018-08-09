import os
from collections import OrderedDict
from csv import DictReader, DictWriter


class ConfigManager(object):
    def __init__(self, session):
        self.session = session
        self._create_dir()

    def _create_dir(self):
        for dir in self.session.working_dir, self.session.mount_dir:
            if not os.path.exists(dir):
                os.makedirs(dir)

    def _get_config(self, config_name):
        with open('settings/default/{}'.format(config_name), 'r') as csvfile:
            content = csvfile.readlines()
            return OrderedDict(x.strip().split('=') for x in content)

    def _save_config(self, config, config_name):
        with open(os.path.join(self.session.working_dir, config_name), 'w') as csvfile:
            for item in config.items():
                csvfile.writelines('='.join(item) + '\n')

    def make_config(self, **kwargs):
        config = self._get_config('config')
        config.update({
            'client_id': kwargs['_client_id'],
            'client_secret': kwargs['_client_secret'],
        })
        self._save_config(config, 'config')

        config = self._get_config('state')
        config.update(
            {
                'auth_request_id': kwargs['_id_token'] or '',
                'last_access_token': kwargs['token'],
                'refresh_token': kwargs['_refresh_token'],
            }
        )
        self._save_config(config, 'state')

    def mount_disk(self):
        os.system('fusermount -u "{}"'.format(self.session.mount_dir))
        os.system(
            'google-drive-ocamlfuse -label "{}" -o uid=$(id -u),gid=$(id -g),allow_other "{}"'.format(
                self.session.user_name, self.session.mount_dir
            )
        )


class DbFile(object):
    file = 'mount.csv'
    fieldnames = ['id', 'user_name', 'fuse_dir', 'mount_path', 'mounted']

    @classmethod
    def add(cls, session):
        with open(cls.file, 'w') as csvfile:
            writer = DictWriter(csvfile, fieldnames=cls.fieldnames)
            data = dict(session)
            writer.writerow(dict(data, mounted=True))
