from flask import Flask

def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = 'costofliving_mykey01'
    from .view import routes
    app.register_blueprint(routes, url_prefix='/')

    return app