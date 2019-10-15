import pandas as pd
import numpy as np
import random
import clean
import cluster_data
import pca
import hierarchical
#import data

cancer_data = np.array(pd.read_excel("./data/BreastCancerData.xlsx", sheet_name="data", dtype=object))
print(cancer_data)

#clean data
cleanData = clean.cleanMatrix()
cleanData.data = cancer_data
cleanData.set_gene_site_column([0,1], True)
cleanData.omit_columns([16,17,18])
cleanData.clean_rows()

cancer_data = cleanData.data

#insert random data into cells
print(cancer_data[0])
for i in range(len(cancer_data)):
    for j in range(1, len(cancer_data[i])):
        cancer_data[i][j] = random.uniform(-2, 3)
        #todo need to get float values
        
print(cancer_data[0])

data_pipeline = cluster_data.PrepareClusterData("./data/KSA_human.txt")
print("got past pipeline")
data_pipeline.CancerData = cancer_data
data_pipeline.replace_with_average()

#fix kinases
#kinase alias name fix here
data_pipeline.convert_kinases("./data/KSA_human.txt")
tempKinases = np.array(pd.read_csv("./results/newPhosKinaseFile.txt"))


#fix kinase substrates columns
for i in range(len(data_pipeline.phosphositePlusKinaseData[:,1])-1):
    data_pipeline.phosphositePlusKinaseData[i,0] = tempKinases[i]
    data_pipeline.phosphositePlusKinaseData[i,1] = str(data_pipeline.phosphositePlusKinaseData[i,1]) + "-" + str(data_pipeline.phosphositePlusKinaseData[i,2])

data_pipeline.phosphositePlusKinaseData = data_pipeline.phosphositePlusKinaseData[:,0:-1]

#get unique kinases
data_pipeline.create_unique_kinases()
#get substrate matrixes 
subMatrix = data_pipeline.get_kinase_substrate_matrixes(2)

#apply pca to my matrix
X = []
labels = []
Xpoor = []
labelsPoor = []
kinaseFeatures, poorKFeats, richKFeats, pfile = pca.getSVDdata("./data/KSA_human.txt", 10, obs="somethin", pfile=data_pipeline.fileName, matrix=subMatrix)
for kinase, vector in kinaseFeatures.items():
    X.append(vector)
    labels.append(kinase)

for kinase, vector in poorKFeats.items():
    Xpoor.append(vector)
    labelsPoor.append(kinase)

print("before hier")
HierCluster = hierarchical.Hierarchical()
print("after hier")
#add data to hiercluster
HierCluster.X = X
HierCluster.labels = labels
HierCluster.kinaseFeatures = kinaseFeatures
HierCluster.poorKFeats = poorKFeats
HierCluster.richKFeats = richKFeats
HierCluster.pfile = pfile
HierCluster.clusterMethod("notpca", 12, pfile)
