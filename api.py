import os
from user import User

import file
import google_auth_oauthlib.flow
import requests
import system_call
from flask import redirect, request
from flask_restful import Resource
from settings import Settings

os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'


class BaseHandler(Resource):
    flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
        Settings['CLIENT_SECRETS_FILE'], scopes=Settings['SCOPES']
    )

    def authorize(self):
        self.flow.redirect_uri = Settings['URL_OAUTH_REDIRECT'].format(request.host)
        return self.flow.authorization_url(
            # Enable offline access so that you can refresh an access token without
            # re-prompting the user for permission. Recommended for web server apps.
            access_type='offline',
            # Enable incremental authorization. Recommended as a best practice.
            include_granted_scopes='true',
            prompt='select_account',
            #response_type='code'
        )


class MainHandler(BaseHandler):
    def get(self, *args, **kwargs):
        if request.path == '/oauth':
            authorization_url, state = self.authorize()
            return redirect(authorization_url)
        elif request.path == '/oauth2callback':
            self.flow.fetch_token(authorization_response=request.url)
            user = User()
            user.credentials = self.flow.credentials.__dict__

            result = requests.get(
                'https://www.googleapis.com/oauth2/v1/userinfo?access_token={}'.format(user.credentials.get('token'))
            )

            user.set_fields(result.json())

            self.config_manager = file.ConfigManager(user=user)
            self.config_manager.make_config(**user.credentials)
            system_call.mount_disk(user)

            file.DbFile.add(user)
            redirect('/templates')


class MountsHandler(Resource):
    def get(self):
        return {
            'result': [
                {
                    'id': value['id'],
                    'folder': value['mount_dir'],
                    'service': 'google',
                    'account': value['user_name'],
                } for value in file.DbFile.get_all().values()
            ]
        }

    def post(self):
        pass
