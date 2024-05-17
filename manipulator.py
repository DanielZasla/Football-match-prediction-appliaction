import pickle
import pandas as pd
from time import time as t
from collections import Counter,defaultdict

test = pd.read_csv("test_set.csv")
test = test[['home_team_api_id', 'away_team_api_id']]
teams = pd.read_csv("teams.csv")
teams = teams[['team_api_id','team_long_name']]
id2name = {}
name2id = {}
for i in teams.iterrows():
    id2name[i[1][0]] = i[1][1]
    name2id[i[1][1]] = i[1][0]
print(name2id)
print(id2name)

team1 = []
games = []
for i in test.iterrows():
    i = i[1]
    if id2name[i[0]] not in team1:
        team1.append(id2name[i[0]])
    # if id2name[i[1]] not in team1:
    #     team1.append(id2name[i[1]])
    games.append((id2name[i[0]], id2name[i[1]]))
mapper = {}
for t in team1:
    mapper[t] = []
    for g in games:
        if g[0]==t:
            if g[1] not in mapper[t]:
                mapper[t].append(g[1])
print(mapper)
pickle.dump(mapper,open("mapper.dict","wb"))