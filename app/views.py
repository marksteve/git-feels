from flask import Blueprint, jsonify

bp = Blueprint('pages', __name__)


@bp.route('/')
def index():
  return "Hello, world"


@bp.route('/analyze', methods=['POST'])
def analyze():
  # Get all commits from repo
  # Tip: r.links["next"]
  # from pattern.en import sentiment
  return jsonify()
