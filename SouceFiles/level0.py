import json
import numpy as np
from python_tsp.heuristics import solve_tsp_local_search

f = open("InputData\\level0.json")
data = json.load(f)
f.close()

n_neighbourhoods = data["n_neighbourhoods"]
n_restaurants = data["n_restaurants"]

dist_matrix = []
dist = [0]
dist.extend(data["restaurants"]["r0"]["neighbourhood_distance"])

i = 0
for n in data["neighbourhoods"]:
    dist = [data["restaurants"]["r0"]["neighbourhood_distance"][i]]
    dist.extend(data["neighbourhoods"][n]["distances"])
    i += 1
    dist_matrix.append(dist)

distance_matrix = np.array(dist_matrix)

permutation, distance = solve_tsp_local_search(distance_matrix)
opDict = {}
pathDict = {}
path = ["r0"]
for n in permutation:
    path.append("n" + str(n))
path.append("r0")
pathDict["path"] = path
opDict["v0"] = pathDict

json_object = json.dumps(opDict, indent=4)
with open("Output\\level0_output.json", "w") as outfile:
    json.dump(opDict, outfile)