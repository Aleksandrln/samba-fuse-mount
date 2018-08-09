import tornado.web
import tornado.ioloop
import api


class Application(tornado.web.Application):
    def __init__(self, debug=False):
        handlers = [
            (r"/", api.MainHandler),
            (r"/oauth2callback", api.MainHandler),
            ]
        settings = dict(
            login_url='/auth/login',
            cookie_secret='awergjlpokj',
            # template_path=os.path.join(os.path.dirname(__file__), 'webim/templates'),
            # static_path=os.path.join(os.path.dirname(__file__), 'static'),
            xsrf_cookies=False,
            debug=debug,
        )
        tornado.web.Application.__init__(self, handlers, **settings)



if __name__ == "__main__":
    app = Application()
    app.listen(8080)
    tornado.ioloop.IOLoop.current().start()