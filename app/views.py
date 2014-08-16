from flask import Blueprint

bp = Blueprint('pages', __name__)


@bp.route('/')
def index():
  return "Hello, world"

