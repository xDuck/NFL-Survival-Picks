from collections import defaultdict
import requests
import time
import re
import math

from bs4 import BeautifulSoup
from tqdm import tqdm

# Constants
SPREAD_URL = "https://www.thelines.com/nfl-lines-every-week-2019/"
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}


def get_data():
    """
    Get the data from online
    """

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

            # Only add games where there was a clear winner from
            # the spread. Log spreads here too because the spread
            # is less important as it gets bigger
            if g1 > 0:
                games[len(games)-1][t1] = math.log(g1)
            elif g2 > 0:
                games[len(games)-1][t2] = math.log(g2)

    return games, list(team_names)


class Graph:
    """
    Represents a graph
    """

    def __init__(self, vertices):
        self.V = vertices  # No. of vertices
        self.graph = []  # default dictionary to store graph

    # function to add an edge to graph
    def addEdge(self, u, v, w):
        self.graph.append([u, v, w])

    # utility function used to print the solution
    def printArr(self, dist):
        print("Vertex   Distance from Source")
        for i in range(self.V):
            print("% d \t\t % lf" % (i, dist[i]))

    # The main function that finds shortest distances from src to
    # all other vertices using Bellman-Ford algorithm.  The function
    # also detects negative weight cycle
    def BellmanFord(self, src):

        # Step 1: Initialize distances from src to all other vertices
        # as INFINITE and parent array as -1
        dist = [float("Inf")] * self.V
        dist[src] = 0
        parent = [-1] * self.V

        # Step 2: Relax all edges |V| - 1 times. A simple shortest
        # path from src to any other vertex can have at-most |V| - 1
        # edges
        for i in tqdm(range(self.V - 1)):
            # Update dist value and parent index of the adjacent vertices of
            # the picked vertex. Consider only those vertices which are still in
            # queue
            # TODO: Don't update if vertex % 16 (?) is already in the mapping
            for u, v, w in self.graph:
                if dist[u] != float("Inf") and dist[u] + w < dist[v]:
                    dist[v] = dist[u] + w
                    parent[v] = u

        self.printArr(dist)
        return dist, parent


def vertexToTeam(v, teams):
    return teams[(v-1) % len(teams)]


def getPath(parent, v):
    if v < 0:
        return []
    else:
        return getPath(parent, parent[v]) + [v]


# Get data
print("Fetching latest spreads")
weeks, teams = get_data()
weeks = weeks[:5]

n_weeks = len(weeks)
n_teams = len(teams)

# Init graph
n_v = (n_teams * (n_weeks+1)) + 1
print("Building graph w/ %d vertecies" % n_v)
g = Graph(n_v)

# Start point is vertex 0 and it connects to every
# vertex 1->n_teams, so everything after this will offset
# vertex by 1 to account for start vertex
for i in range(n_teams):
    g.addEdge(0, i + 1, 0)

# Connect graph
for w, week in enumerate(weeks):
    for team, spread in week.items():
        u = w * n_teams + teams.index(team) + 1
        for i in range(n_teams):
            v = (w+1) * n_teams + i + 1
            # print("%d, %d" % (u, v))
            g.addEdge(u, v, -spread)

# Bellman ford
print("Running Bellman ford")
d, p = g.BellmanFord(0)

# Print result
for i in range(n_teams):
    v = n_teams * n_weeks + i
    path = getPath(p, v)
    for t in path:
        print(vertexToTeam(t, teams), end=", ")
    print()
