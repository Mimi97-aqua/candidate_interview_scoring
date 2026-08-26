"""
Application entry point
"""
from flask import Flask
from routes.api import interviews


def create_app():
    """
    Application factory
    :return:
    """
    app = Flask(__name__)
    app.register_blueprint(interviews, url_prefix='/api')
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, port=5000, host='0.0.0.0')
