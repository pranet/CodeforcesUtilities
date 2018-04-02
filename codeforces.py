from collections import defaultdict

import requests
from functional import seq


class Problem(object):
    def __init__(self, contest_id, index, name, tags):
        self.contest_id = contest_id
        self.index = index
        self.name = name
        self.tags = tags
        self.weight = None

    def url(self):
        return "http://codeforces.com/problemset/problem/{}/{}".format(self.contest_id, self.index)

    def __repr__(self):
        return str({
            "weight": self.weight,
            "name": self.name,
            "url": self.url(),
            "tags": self.tags
        })

    def __hash__(self):
        return self.contest_id

    def __eq__(self, other):
        return self.contest_id == other.contest_id and self.index == other.index


class Codeforces(object):
    @staticmethod
    def generate_problem_weights():
        url = "http://codeforces.com/api/problemset.problems"
        problems = requests.get(url=url).json()['result']['problemStatistics']
        weights = defaultdict(dict)
        for problem in problems:
            weights[problem['contestId']][problem['index']] = problem['solvedCount']
        return weights

    @staticmethod
    def get_problems_solved_by_user(user: str):
        def add_to_set(st: set(), ele):
            st.add(ele)
            return st

        url = "http://codeforces.com/api/user.status?handle={}&from=1&count=100000".format(user)
        try:
            data = requests.get(url=url).json()['result']
        except Exception:
            raise Exception("Unable to fetch data for user {}".format(user))
        return seq(data) \
            .filter(lambda x: x['verdict'] == "OK") \
            .map(lambda x: Problem(x['problem']['contestId'], x['problem']['index'], x['problem']['name'],
                                   x['problem']['tags'])) \
            .reduce(lambda y, x: add_to_set(y, x), set())

    @staticmethod
    def add_problem_weights(problems):
        weights = Codeforces.generate_problem_weights()
        for problem in problems:
            try:
                problem.weight = weights[problem.contest_id][problem.index]
            except:
                problem.weight = 100000

    @staticmethod
    def get_all_tags():
        url = "http://codeforces.com/api/problemset.problems"
        problems = requests.get(url=url).json()['result']['problems']
        tags = defaultdict(int)
        for problem in problems:
            for tag in problem['tags']:
                tags[tag] += 1
        return tags
