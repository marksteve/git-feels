from flask import (
  Blueprint,
  jsonify,
  render_template,
  request,
  current_app
)
import requests
#from pattern.en import sentiment

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

  current_app.logger.debug(get_sentiment())

  # Iterate in each commit and save to array
  messages = []
  for commit in res.json() :
    messages.append(commit['commit']['message'])

  return jsonify(messages = messages)

def get_sentiment():
  x = 1 + 1
  return x