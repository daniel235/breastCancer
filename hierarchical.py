from scipy.cluster.hierarchy import dendrogram, linkage
import scipy.spatial.distance as ssd
from sklearn.cluster import AgglomerativeClustering
from matplotlib import pyplot as plt 
import numpy as np

import pca

class Hierarchical:
    def __init__(self):
        self.kinaseFeatures = {}
        self.poorKFeats = {}
        self.richKFeats = {}
        self.kinaseFile = None
        self.dataFile = None
        self.X = []
        self.labels = []
        self.Xpoor = []
        self.labelsPoor = []
        self.Xrich = []
        self.labelsRich = []
        self.k = 0


    def clusterMethod(self, method):
        if method == "pca":
            #get kinase svd feature 
            self.kinaseFeatures, self.poorKFeats, self.richKFeats, pfile = pca.getSVDdata(self.kinaseFile, 10)
            for kinase, vector in self.poorKFeats.items():
                self.Xpoor.append(vector)
                self.labelsPoor.append(kinase)

            for kinase, vector in self.richKFeats.items():
                self.Xrich.append(vector)
                self.labelsRich.append(kinase)

        distMatrix = self.euclidDistance(self.Xpoor, self.labelsPoor)
    
        #condense distance matrix
        distArray = ssd.squareform(distMatrix) 
 
        arr = linkage(distArray, method='single')
        #kinase names
        plt.figure()
        dendrogram(arr, labels=self.labelsPoor, show_leaf_counts=True)
        plt.savefig(("./data/results/" + str(pfile)[:-5] + "poor.jpg"))
        plt.show() 

        distMatrix = self.euclidDistance(self.Xrich, self.labelsRich)
    
        #condense distance matrix
        distArray = ssd.squareform(distMatrix) 
 
        arr = linkage(distArray, method='single')
        #kinase names
        plt.figure()
        dendrogram(arr, labels=self.labelsRich, show_leaf_counts=True)
        plt.savefig(("./data/results/" + str(pfile)[:-5] + "rich.jpg"))
        plt.show() 


    def euclidDistance(self, matrix, labels):
        #for i in range(len(a)):
        #get euclid distance of a[i] and b[i]
        distMatrix = []
        row = []
        print("matr", matrix)

        for i in range(len(matrix)):
            a = matrix[i]
            aLabel = labels[i]
            for j in range(len(matrix)):
                b = matrix[j]
                bLabel = labels[j]
                if i == j:
                    row.append(0)
                else:
                    if(aLabel == 'SYK' and bLabel == 'LCK'):
                        print("syk and lck distance ", np.linalg.norm(a-b))

                    elif aLabel == 'PRKCA' and bLabel == 'MAPK9':
                        print("prkca and mapk9 distance ", np.linalg.norm(a-b))

                    row.append(np.linalg.norm(a-b))

            distMatrix.append(row)
            row = []
    
        return distMatrix
       
        

hierCluster = Hierarchical()
hierCluster.kinaseFile = "./data/KSA_human.txt" 
#hierCluster.dataFile = "./data/BreastCancerData.xlsx"
hierCluster.clusterMethod("pca")
