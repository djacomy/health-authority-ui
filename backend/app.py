from flask import Flask
from flask_cors import CORS


def create_app(config_obj):
    app = Flask(__name__)
    app.config.from_object(config_obj)

    CORS(
        app,
        resources={r"/*": {"origins": "*"}},
        headers=['Content-Type', 'X-Requested-With', 'Authorization']
    )
    from healthautority.route import blueprint
    app.register_blueprint(blueprint, url_prefix="/")
    return app
