import json
from collections import defaultdict

import matplotlib.pyplot as plt
import numpy
from matplotlib import rcParams

from codeforces import Codeforces


class ReportCardMaker(object):
    def __init__(self, judge: Codeforces):
        self.judge = judge
        with open('tags.txt') as infile:
            self.all_tags = json.load(infile)
        self.index = dict()
        for i, tag in enumerate(self.all_tags):
            self.index[tag] = i

    def plot(self, cnts, users, total_cnts, total):
        rcParams.update({'figure.autolayout': True})
        x = numpy.arange(len(self.all_tags))
        total_width = 0.5
        n = len(cnts)
        width_per_bar = total_width / n
        colors = ['r', 'g', 'b', 'y', 'm', 'k', 'w']
        offsets = numpy.arange(-(n - 1), n + 1, 2)

        if total:
            plt.bar(x, total_cnts, align='center', color='c', width=total_width, label="Total")

        for i, cnt in enumerate(cnts):
            plt.bar(x + offsets[i] * (width_per_bar / 2.0), cnt, align='center', color=colors[i % len(colors)],
                    width=width_per_bar,
                    label=users[i])

        plt.legend()
        plt.xticks(x, self.all_tags, rotation=90)
        plt.show()

    def get_user_data(self, user):
        cnt = defaultdict(int)
        problems = self.judge.get_problems_solved_by_user(user)
        for problem in problems:
            tags = problem.tags
            for tag in tags:
                cnt[tag] += 1
        return cnt

    def get_problem_data(self):
        return self.judge.get_all_tags()

    def display_report(self, users, total):
        if len(users) >= 5:
            raise Exception("Please specify 5 or fewer users to compare")

        cnts = []
        for user in users:
            tags_data = self.get_user_data(user=user)
            cnt = []
            for tag in self.all_tags:
                cnt.append(tags_data[tag])
            cnts.append(cnt)
        tags_data = self.get_problem_data()

        total_cnts = []
        for tag in self.all_tags:
            total_cnts.append(tags_data[tag])

        self.plot(cnts, users, total_cnts, total)


reportCardMaker = ReportCardMaker(Codeforces)
reportCardMaker.display_report(["xennygrimmato", "pranet"], total=False)
