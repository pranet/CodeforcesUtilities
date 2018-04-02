from functional import seq
from codeforces import Codeforces


class ProblemSuggester(object):
    def __init__(self, judge: Codeforces):
        self.judge = judge

    def get_problems_solved_by_everyone(self, users):
        return set.intersection(*map(self.judge.get_problems_solved_by_user, users))

    def get_problems_solved_by_anyone(self, users):
        return set.union(*map(self.judge.get_problems_solved_by_user, users))

    def suggest(self, set_a, set_b, weight_limit=100000, count=5):
        candidate_problems = self.get_problems_solved_by_everyone(set_a) - self.get_problems_solved_by_anyone(set_b)
        self.judge.add_problem_weights(candidate_problems)
        candidate_problems = seq(candidate_problems).filter(lambda x: x.weight <= weight_limit)
        return sorted(candidate_problems, key=lambda x: x.weight, reverse=True)[:count]

set_a = {"ujzwt4it"}
set_b = {"pranet"}
codeforces_problem_suggester = ProblemSuggester(Codeforces)
suggestions = codeforces_problem_suggester.suggest(set_a=set_a, set_b=set_b, weight_limit=2000, count=10000)
print(len(suggestions))
for suggestion in suggestions:
    print(suggestion)