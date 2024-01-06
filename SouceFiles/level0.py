import json
import numpy as np
from python_tsp.exact import solve_tsp_dynamic_programming

f = open("InputData\\level0.json")
data = json.load(f)
f.close()

n_neighbourhoods = data["n_neighbourhoods"]
n_restaurants = data["n_restaurants"]

dist_matrix = []
dist = [0]
dist.extend(data["restaurants"]["r0"]["neighbourhood_distance"])
dist_matrix.append(dist)

i = 0
for n in data["neighbourhoods"]:
    dist = [data["restaurants"]["r0"]["neighbourhood_distance"][i]]
    dist.extend(data["neighbourhoods"][n]["distances"])
    i += 1
    dist_matrix.append(dist)

distance_matrix = np.array(dist_matrix)
print(distance_matrix)

permutation, distance = solve_tsp_dynamic_programming(distance_matrix)
opDict = {}
pathDict = {}
path = ["r0"]
for n in permutation:
    if n != 20:
        path.append("n" + str(n))
path.append("r0")
pathDict["path"] = path
opDict["v0"] = pathDict

json_object = json.dumps(opDict, indent=4)
with open("Output\\level0_output.json", "w") as outfile:
    json.dump(opDict, outfile)