import os
import uuid

# class SessionManager(object):
#     sessions = {}
#
#     @classmethod
#     def get(cls, id):
#         return cls.sessions.get(id)
#
#     @classmethod
#     def new_user(cls, user_name=''):
#         id = str(uuid.uuid1())
#         cls.sessions[id] = User(id, user_name)
#         return id


class User(object):
    def __init__(self, uuid=None, user_name=None):
        self._uuid = uuid
        self.working_dir = None
        self.mount_dir = None
        if user_name:
            self.user_name = user_name
        self.credentials = None

    @property
    def user_name(self):
        return self._user_name

    @user_name.setter
    def user_name(self, user_name):
        self._user_name = user_name
        current_directory = os.path.expanduser('~')
        self.working_dir = os.path.join(current_directory, '.gdfuse', user_name)
        self.mount_dir = os.path.join(current_directory, 'mount', user_name)

    def set_fields(self, data):
        self._uuid = data['id']
        self.user_name = data['name']
        return self

    def __iter__(self):
        for k, v in {
            'id': self._uuid,
            'user_name': self.user_name,
            'fuse_dir': self.working_dir,
            'mount_dir': self.mount_dir,
        }.iteritems():
            yield k, v
