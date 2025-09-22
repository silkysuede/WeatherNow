from flask import Flask

def create_app(config_file=None):
    app = Flask(__name__, instance_relative_config=False)
    
    if config_file is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(config_file)
    
    with app.app_context():
        from app.routes import routes
        app.register_blueprint(routes)
    
    return app