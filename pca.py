import numpy as np
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
from numpy import linalg
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import AgglomerativeClustering
import pickle
import pandas as pd
import seaborn as sns
import os
import cluster_data
import graph
import stats
import math
#start pca 

#grab kinase bucket matrixes
def getMatrix(kinase):
    clusterStructure = cluster_data.ClusterData(kinase)
    myMatrix = clusterStructure.get_kinase_substrate_matrixes(2)
    psiteCount = len(clusterStructure.CancerData[:,1])
    kinaseCount = len(myMatrix.keys())
    tsampleCount = len(clusterStructure.CancerData[1])
    afterStat = stats.Statistics() 
    afterStat.set_table(psiteCount, kinaseCount, tsampleCount)
    afterStat.plotTable()
    return myMatrix, clusterStructure.fileName


#get SVDs of each kinase bucket and write it to svd txt file
def getSVDdata(kinase, threshold):
    poorKinaseFeature = {}
    richKinaseFeature = {}
    substrateCount = 0
    kinaseFeature = {}
    matrix, pfile = getMatrix(kinase)
    
    with open("./results/" + str(pfile)[:-5] + "svd.txt", 'w+') as f: 
        f.write("Method Singular Value Decomposition(One of the PCA methods)\n")
        f.write("X = U(SIG)V*\n\n")
        f.write("X shape (nxm)\n\n")
        f.write("U shape (nxn)\n\n")
        f.write("(SIG) shape (nx1)\n\n")
        f.write("V shape (nxm)\n\n")

        
        for kinase, data in matrix.items():
            bucket = []
            substrateCount = len(data.values())
            for substrate in data.values():
                bucket.append(substrate)


            kinaseFeature[kinase], u, s, vt = getFeatureVector(kinase, bucket, 2)
            if substrateCount > threshold:
                richKinaseFeature[kinase] = kinaseFeature[kinase]
            else:
                poorKinaseFeature[kinase] = kinaseFeature[kinase]

            f.write("Kinase " + str(kinase) + "\n" + "Singular Vector U \n" + str(u) + "\n" + "Singular Values \n" + str(s) + "\n" + "Singular Vector V (transpose) \n" + str(vt) + "\n\n")
            
    
    return kinaseFeature, poorKinaseFeature, richKinaseFeature, pfile

#get principal components of kinase buckets
def getPcaVectors(matrix):
    pca = PCA(n_components=2)
    matrix = StandardScaler().fit_transform(matrix)
    pcs = pca.fit_transform(matrix)
    pcDf = pd.DataFrame(data=pcs, columns=['principal component 1', 'principal component 2'])
    return pcDf


#get kinase feature vector
def getFeatureVector(kinase, matrix, dim):
    #todo center data
    #todo pickle data
    #transpose matrix
    matrix = np.transpose(matrix)
    
    #standardize data scale 
    ss = StandardScaler()
    #matrix = ss.fit_transform(matrix)
    #print(matrix)

    #pcs = getPcaVectors(matrix)
    u, s, vt = linalg.svd(matrix, full_matrices=False)
    

    #get variance
    var_explained = np.round(s**2/np.sum(s**2), decimals=3)
    sns.barplot(x=list(range(1,len(var_explained)+1)),
        y=var_explained, color="limegreen")
        
    plt.xlabel("PCS")
    plt.ylabel("Percent Variance Explained")
    plt.savefig('./results/svd_variance.png', dpi=100)
    
    #get first column of V   (6*6) (6*27) ((6*27)->VT)  / (27*27) (27*6) ((27*6) -> VT)  X-> (27*6) V -> (6*27)  VR-> (6 * 1)  X* VR -> (27*6)(6*1) -> (27*1)
    v = np.transpose(vt)
    #vR
    v = v[:,:dim]
    #get scores XVR
    vec = np.matmul(matrix, v)
    

    if not os.path.exists('./data/pickles/xvr'):
        dbfile = open('./data/pickles/xvr', 'ab')

        pickle.dump(vec, dbfile)
        dbfile.close()

    return vec, u, s, vt


def plotPCA(X, Y):
    plt.figure()
    plt.plot(X, Y, 'o')
    plt.show()
