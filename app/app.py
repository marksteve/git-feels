from flask import Flask

from .views import bp


def create_app(**config):
  app = Flask(__name__)
  app.config.update(**config)
  app.register_blueprint(bp)
  return app
