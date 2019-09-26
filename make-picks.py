import requests
import time
import re

from bs4 import BeautifulSoup
from tqdm import tqdm

# Constants
SPREAD_URL = "https://www.thelines.com/nfl-lines-every-week-2019/"
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}

# Get all the data


def get_data():
    response = requests.get(SPREAD_URL, headers=HEADERS)
    soup = BeautifulSoup(response.text, "html.parser")
    weeks = soup.findAll("table", {"class": "tablepress"})

    # Format into array of tuples ([teams], spread)
    games = []
    team_names = set()

    # Process each week
    for week in weeks:

        teams = week.findAll("td", {"class": "column-1"})
        spreads = week.findAll("td", {"class": "column-2"})
        games.append(dict())

        for i in range(len(teams)):

            # Team names
            t = teams[i].text.split("\n")
            t1 = re.sub("\(.*\)", "", t[0]).strip()
            t2 = re.sub("\(.*\)", "", t[1]).strip()
            team_names.add(t1)
            team_names.add(t2)

            # Spread
            g = spreads[i].text.split("\n")
            g1 = 0.0 if g[0] == "PK" else float(g[0])
            g2 = 0.0 if g[1] == "PK" else float(g[1])

            # Game
            games[len(games)-1][t1] = g2
            games[len(games)-1][t2] = g1

    return games, list(team_names)


# Compute the sum for the given choices
def compute(games, choices):
    sum = 0
    for i in range(len(choices)):
        if choices[i] not in games[i]:
            return -1
        sum += games[i][choices[i]]
    return sum


# Calculate based on a set of choices
def calculate(games, teams):
    best_sum = 0
    best_list = []

    for choice in tqdm(permutations(teams, len(games))):
        v = compute(games, choice)
        if v == best_sum:
            best_list.append(choice)
        elif v > best_sum:
            best_list = [choice]

    return best_list


best_sum = 0
best_list = []

# A more efficient permutation-based approach


def efficient_permute(games, teams, current, current_sum):
    global best_sum, best_list

    # Hit length
    if len(current) == len(games):
        if current_sum == best_sum:
            best_list.append(current)
        elif current_sum > best_sum:
            best_sum = current_sum
            best_list = [current]
        return

    top = True if len(current) == 0 else False

    # Still need to add more teams
    if top:
        for t in tqdm(teams):
            if t in games[len(current)] and games[len(current)][t] > 0 and t not in current:
                efficient_permute(games, teams, current +
                                  [t], current_sum + games[len(current)][t])
    else:
        for t in teams:
            if t in games[len(current)] and games[len(current)][t] > 0 and t not in current:
                efficient_permute(games, teams, current +
                                  [t], current_sum + games[len(current)][t])


# Main
g, t = get_data()
# print(efficient_permute(g, t, [], 0))

n_teams = 32
n_weeks = len(g)
iter_s = 350000.0

n_v = (n_teams * n_weeks) ** 2
n_e = (n_teams ** 2) * n_weeks
O = n_v * n_e
