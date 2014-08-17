from flask import Blueprint, current_app, jsonify, render_template, request

from .git_feels import GitFeels

bp = Blueprint('pages', __name__)


@bp.route('/')
def index():
  # Render template
  return render_template('index.html')


@bp.route('/analyze', methods=['POST'])
def analyze():
  user, repo = request.json['user_repo'].split('/')
  gf = GitFeels.from_github(user, repo)
  return jsonify(report=gf.get_report())

