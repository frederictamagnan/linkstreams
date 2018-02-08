# -*- coding: utf-8 -*-
import math
import numpy as np
import matplotlib.pyplot as plt


import Profiling_Community_Dynamics.generator as gen


def distEntropy(linkstream, start = None, delta = None):
    """
    Calculate the entropy of a Linkstream object  

    :param linkstream: A linkstream object.
    :param start: The start time.
    :param delta: A time window on which the entropy is calculated.
    :return: the entropy of the Linkstream 
    """    
    if linkstream == None:
        return 0
    
    df = linkstream.linkstream.astype(int)
    
    if start != None and delta != None:
        df = df.loc[df['t'] >= start]
        df = df.loc[df['t'] <= start + delta]
        
    elif start != None and delta == None:
        df = df.loc[df['t'] >= start]
    
    allUsers = df['u'].values.tolist() + df['v'].values.tolist()
    allUsers = list(set(allUsers))
    
    if len(allUsers) == 0:
        return 0
        
    users = {}
    for i in range(len(allUsers)):
        users[i] = allUsers[i]
    
    maxValue = len(allUsers)
   
    df2 = df.drop('t',1)
    
    list2 = list(zip(df2['u'].values.tolist(), df2['v'].values.tolist()))
    
    deg2=[0]*maxValue
    
    for row in list2:
      
        deg2[list(users.keys())[list(users.values()).index(row[0])]]= deg2[list(users.keys())[list(users.values()).index(row[0])]]+1
        deg2[list(users.keys())[list(users.values()).index(row[1])]]= deg2[list(users.keys())[list(users.values()).index(row[1])]]+1

    Pk = [0]*len(set(deg2))
    nk = [0]*len(set(deg2))
    
    k=0
    for i in set(deg2):
        for j in deg2:
            if j == i:
                nk[k]=nk[k]+1
        k=k+1

    k=0
    for n in nk:
        Pk[k]=n/float(len(deg2))
        k=k+1
    Pk=list(zip(set(deg2),Pk))
    
    SumKPk = 0
    for i in Pk:
        SumKPk = SumKPk + i[0]*i[1]

    qK = [0]*(len(set(deg2)))

    for k in range(len(qK)):
        qK[k] = Pk[k][0]*Pk[k][1]/SumKPk

    H = 0
    for q in qK:
        if q >0:
            H = H - q*math.log(q)
    
    return H




def meanEntropy(linkstream, delta, step):
    """
    Calculate the mean Entropy of a linkstream 

    :param linkstream: A Linkstream object.
    :param delta: The time window on which each entropy is calculated.
    :param step: The progress step.
    :return: The mean Entropy of the linkstream
    """    
    endTime = linkstream.linkstream.max(axis = 0)['t']
    
    entropies = np.array([])
    start = 0
    
    while start < endTime:
        entropies = np.append(entropies, distEntropy(linkstream, start, delta))
        start = start + step
    
    return np.mean(entropies)



def matrixComp(mat1, mat2, n_estimators = 1000):
    """
    Compare two probability matrices 

    :param mat1: First probability matrix.
    :param mat2: Second probability matrix.
    :param n_estimators: number of iteratons.
    :return: a list containing the mean, std deviation and mediane of the entropy of the linkstream created based on each matrix
    """
    
    Entrop1 = np.array([])
    Entrop2 = np.array([])
    delts = np.array([])
    for i in range (n_estimators):
        ls1 = gen.generator(matrix=mat1)
        ls2 = gen.generator(matrix=mat2)
        
        endTime = ls2.linkstream.max(axis = 0)['t']
        delta = endTime/5
        
        Entrop1 = np.append(Entrop1,distEntropy(ls1))
        Entrop2 = np.append(Entrop2,distEntropy(ls2))
        delts = np.append(delts, distEntropy(ls2, delta, delta))
        
    return np.matrix([[np.std(Entrop1), np.mean(Entrop1), np.median(Entrop1)], [np.std(Entrop2), np.mean(Entrop2), np.median(Entrop2)]])
    
def vizualisation_entropy(linkstream, step = 1, startTime = None, endTime = None, delta=None):
     """
     Vizualize the entropy over time 

     :param linkstream: A linkstream object.
     :param step: the time between two samples.
     :param startTime: the start time.
     :param endTime: the end time.
     :param delta: the time window on which the entropy is calculated. If None, the entropy is calculated from the startTime.
     """
     
     df=linkstream.linkstream
     
     if startTime is None: # If startTime is not assigned, it is assigned to be first timestamp in linkstream.
         startTime = min(df.loc[:, linkstream.column_timestamp])
     if endTime is None: # If endTime is not assigned, it is assigned to be last timestamp in linkstream.
         endTime = max(df.loc[:, linkstream.column_timestamp])
     
     y=[]
     x=[]
     
     iterator = startTime
     if delta is None or delta <=0 :
         while iterator<endTime-step:
             x.append(iterator)
             y.append(distEntropy(linkstream,iterator))
             iterator=iterator+step
         plt.plot(x,y,)
         plt.ylabel("Linkstream entropy")
         plt.xlabel("time")
         plt.show()	
     else:
          while iterator<endTime-step:
             x.append(iterator)
             y.append(distEntropy(linkstream,iterator, delta))
             iterator=iterator+step
     
          plt.plot(x,y,)
          plt.ylabel("Linkstream delta entropy")
          plt.xlabel("time")
          plt.title("delta = " + str(delta))
          plt.show()	
