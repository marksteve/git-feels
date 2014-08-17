import requests
from flask import Blueprint, current_app, jsonify, render_template, request
from pattern.en import sentiment
from pattern.en.wordlist import PROFANITY

bp = Blueprint('pages', __name__)

ACCESS_TOKEN = "a4db24a6e646ad71d1c11bbd76932eeefdbeda08"


def get_github_list(url):
  res = requests.get(
    url,
    auth=(ACCESS_TOKEN, 'x-oauth-basic'),
  )
  for result in res.json():
    yield result
  next = res.links.get('next')
  if next:
    for result in get_github_list(next['url']):
      yield result


class GitFeels(object):

  def __init__(self, repo_name, commits):
    self.repo_name = repo_name
    self.commits = commits

  @classmethod
  def from_github(cls, user, repo):
    results = get_github_list(
      "https://api.github.com/repos/{}/{}/commits".format(
        user, repo
      )
    )
    commits = {}
    for result in results:
      author = result.get('author')
      if not author:
        author = result['commit']['author']
        author.update(
          id=author['email'],
          avatar_url='http://www.gravatar.com/avatar/00000000000000000000000000000000?d=mm',
        )
      commits.setdefault(author['id'], dict(
        author=author,
      ))
      commits[author['id']].setdefault(
        'commits',
        [],
      ).append(dict(
        date=result['commit']['author']['date'],
        message=result['commit']['message'],
      ))
    return cls('/'.join([user, repo]), commits.values())

  def count_profanities(self, message):
    return len(filter(
      lambda word: word in PROFANITY,
      message.lower().split()
    ))

  def get_report(self):
    report = dict(
      repo_name=self.repo_name,
      authors=[],
    )
    for author_commits in self.commits:
      pos, neg = 0, 0
      profanities = 0
      for commit in author_commits['commits']:
        polarity, subjectivity = sentiment(commit['message'])
        if polarity < 0:
          neg -= polarity
        else:
          pos += polarity
        # TODO: What do we do with subjectivity?
        profanities += self.count_profanities(commit['message'])
      report['authors'].append(dict(
        pos=pos,
        neg=neg,
        profanities=profanities,
        **author_commits['author']
      ))
    return report


@bp.route('/')
def index():
  # Render template
  return render_template('index.html')


@bp.route('/analyze', methods=['POST'])
def analyze():
  user, repo = request.json['user_repo'].split('/')
  gf = GitFeels.from_github(user, repo)
  return jsonify(report=gf.get_report())

