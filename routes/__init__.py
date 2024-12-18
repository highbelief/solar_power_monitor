from .auth_routes import auth_blueprint
from .data_routes import data_blueprint
from .log_routes import log_blueprint

def register_routes(app):
    app.register_blueprint(auth_blueprint, url_prefix='/api')
    app.register_blueprint(data_blueprint, url_prefix='/api')
    app.register_blueprint(log_blueprint, url_prefix='/api')
