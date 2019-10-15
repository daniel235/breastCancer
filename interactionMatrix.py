import pandas as pd
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import pickle


#read unique kinases
filename = "./data/pickles/uniqueKinases"
with open(filename, 'rb+') as f:
    uniqueKinases = pickle.load(f)

#create matrix
interaction_matrix = np.zeros(shape=(len(uniqueKinases), len(uniqueKinases)))

print(interaction_matrix)

#get correlation values
filename = "./data/pickles/clusterGroups"
with open(filename, 'rb+') as f:
    cg = pickle.load(f)


#go through cluster groups
for i in range(len(cg)):
    for j in range(len(cg[i])):
        #inside the cluster group k
        for k in cg[i][j]:
            for l in cg[i][j]:
                if k != l:
                    #add instance to interaction matrix
                    #get index from unique kinases
                    index1 = uniqueKinases.index(k)
                    index2 = uniqueKinases.index(l)
                    interaction_matrix[index1, index2] += 1
                    interaction_matrix[index2, index1] += 1



print(uniqueKinases[0], interaction_matrix[0])

#visualize data 
fig, ax = plt.subplots()
im = ax.imshow(interaction_matrix)

ax.set_xticks(np.arange(len(uniqueKinases)))
ax.set_yticks(np.arange(len(uniqueKinases)))
ax.set_xticklabels(uniqueKinases)
ax.set_yticklabels(uniqueKinases)

plt.setp(ax.get_xticklabels(), rotation=45, ha="right", rotation_mode="anchor")

for i in range(len(uniqueKinases)):
    for j in range(len(uniqueKinases)):
        text = ax.text(j, i, interaction_matrix[i, j], ha="center", va="center", color="w")

ax.set_title("Interaction matrix")
fig.tight_layout()
plt.show()
