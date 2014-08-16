from flask import (
  Blueprint,
  jsonify,
  render_template,
  request,
  current_app
)
import requests
from pattern.en import sentiment
from pattern.en.wordlist import PROFANITY

bp = Blueprint('pages', __name__)


@bp.route('/')
def index():
    # Render template
    return render_template('index.html')


@bp.route('/analyze', methods=['GET'])
def analyze():
  # Get params
  username = request.args.get('gh-username', '')
  repo = request.args.get('gh-repo', '')

  # Get all commits from repo
  url = "https://api.github.com/repos/{}/{}/commits".format(username,repo)
  res = requests.get(url)

  # Iterate in each commit and save to array
  data = []
  for commit in res.json() :
    message = commit['commit']['message']
    profanity = any([word in PROFANITY for word in message.split()])

    data.append(dict(
      message=message,
      sentiment=sentiment(message),
      profanity=profanity
    ))

  return jsonify(data = data)
