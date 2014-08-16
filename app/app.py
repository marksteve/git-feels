from flask import Flask


def create_app(**config):
  app = Flask(__name__)
  app.config.update(**config)
  return app
