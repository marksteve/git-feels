import arrow
import requests
from pattern.en import sentiment
from pattern.en.wordlist import PROFANITY

from cachecontrol import CacheControl

cached_sess = CacheControl(requests.session())


ACCESS_TOKEN = "a4db24a6e646ad71d1c11bbd76932eeefdbeda08"


def get_github_list(url):
  res = cached_sess.get(
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
    commits = {}
    results = get_github_list(
      "https://api.github.com/repos/{}/{}/commits".format(
        user, repo
      ),
    )
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
      a = dict(
        pos=0,
        neg=0,
        profanities=0,
        commits_count=len(author_commits['commits']),
      )
      sentiment_series = {}

      pos_messages = []
      neg_messages = []

      for commit in reversed(author_commits['commits']):
        day = arrow.get(commit['date']).ceil('day').timestamp
        sentiment_series.setdefault(day, 0)

        polarity, subjectivity = sentiment(commit['message'])
        # TODO: What do we do with subjectivity?
        if polarity < 0:
          a['neg'] -= polarity
          pos_messages.append((polarity, commit['message']))
        else:
          a['pos'] += polarity
          neg_messages.append((-polarity, commit['message']))
        sentiment_series[day] += polarity

        profanities = self.count_profanities(
          commit['message'],
        )
        a['profanities'] += profanities

      sentiment_series = [
        dict(ts=ts, polarity=polarity) for
        (ts, polarity) in sorted(
          sentiment_series.items(),
          key=lambda x: x[0],
        )
      ]

      if pos_messages:
        pos_message = max(pos_messages, key=lambda m: m[0])[1]
      else:
        pos_message = None
      if neg_messages:
        neg_message = max(neg_messages, key=lambda m: m[0])[1]
      else:
        neg_message = None

      a.update(
        sentiment_series=sentiment_series,
        pos_message=pos_message,
        neg_message=neg_message,
        **author_commits['author']
      )

      report['authors'].append(a)

    report['authors'].sort(
      key=lambda a: -a["commits_count"]
    )

    return report

