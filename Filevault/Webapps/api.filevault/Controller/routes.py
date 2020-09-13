from .routesfunc import *

def setuproute(app, call):
    @app.route('/',                    ['OPTIONS', 'GET'],         lambda x = None: call([get_public]))
    @app.route('/rsa',                 ['OPTIONS', 'GET'],         lambda x = None: call([generate_rsa]))
    @app.route('/rsa/<>',              ['OPTIONS', 'GET'],         lambda x = None: call([generate_rsa]))
    @app.route('/init',                ['OPTIONS', 'POST'],        lambda x = None: call([init]))
    def base():
        return
