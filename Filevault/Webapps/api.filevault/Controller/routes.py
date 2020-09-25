from .routesfunc import *

def setuproute(app, call):
    @app.route('/',                    ['OPTIONS', 'GET'],         lambda x = None: call([version]))
    @app.route('/',                    ['OPTIONS', 'POST'],        lambda x = None: call([check_init, get_public]))
    @app.route('/test/rsa',            ['OPTIONS', 'GET'],         lambda x = None: call([generate_rsa]))
    @app.route('/test/rsa/<>',         ['OPTIONS', 'GET'],         lambda x = None: call([generate_rsa]))
    @app.route('/test/unencode',       ['OPTIONS', 'POST'],        lambda x = None: call([check_init, unencode]))
    @app.route('/file',                ['OPTIONS', 'POST'],        lambda x = None: call([check_init, unencode, new_file]))
    @app.route('/file/content',        ['OPTIONS', 'POST'],        lambda x = None: call([check_init, unencode, get_file]))
    @app.route('/init',                ['OPTIONS', 'POST'],        lambda x = None: call([init]))
    @app.route('/init',                ['OPTIONS', 'GET'],         lambda x = None: call([infos]))
    def base():
        return
