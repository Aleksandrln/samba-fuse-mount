import os

import google_auth_oauthlib.flow
import tornado.web
import tornado.web
import requests
from settings import Settings
import file , system_call
from session import SessionManager

os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

class BaseHandler(tornado.web.RequestHandler):
    flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(Settings['CLIENT_SECRETS_FILE'],
                                                                   scopes=Settings['SCOPES'])

    def get_current_user(self):
        user_id = self.get_secure_cookie('user_id')
        user = SessionManager.get(user_id)
        if not user:
            user_id = SessionManager.new_user()
            self.set_secure_cookie('user_id', user_id)

        return SessionManager.get(user_id)

    def authorize(self):
        self.flow.redirect_uri = Settings['URL_OAUTH_REDIRECT'].format(self.request.host)
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
        if self.request.path == '/':
            authorization_url, state = self.authorize()
            self.redirect(authorization_url)
        elif self.request.path == '/oauth2callback':
            self.flow.fetch_token(authorization_response=self.request.full_url())
            session = self.current_user
            session.credentials = self.flow.credentials.__dict__

            result = requests.get(
                'https://www.googleapis.com/oauth2/v1/userinfo?access_token={}'.format(session.credentials.get('token')))
            self.current_user.set_fields(result.json())

            self.config_manager = file.ConfigManager(session=session)
            self.config_manager.make_config(**session.credentials)
            system_call.mount_disk(session)

            file.DbFile.add(self.current_user)
            #self.write(self.request.full_url())
            self.finish()
