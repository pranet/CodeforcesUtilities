from codeforces import Codeforces
import json
data = sorted(Codeforces.get_all_tags().keys())
with open('tags.txt', 'w') as outfile:
    json.dump(data, outfile)
