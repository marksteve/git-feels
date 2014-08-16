from flask import Blueprint, jsonify, render_template

bp = Blueprint('pages', __name__)


@bp.route('/')
def index():
  return render_template('index.html')


@bp.route('/analyze', methods=['POST'])
def analyze():
  # Get all commits from repo
  # Tip: r.links["next"]
  # from pattern.en import sentiment
  return jsonify()
