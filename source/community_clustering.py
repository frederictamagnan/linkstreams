from data_extraction import *
from sklearn.cluster import *
from pandas.io.parsers import read_csv
from sklearn.preprocessing import StandardScaler
import numpy as np


def dbscan_delta_density_clustering(deltadensity_result, eps, min_sample):
    to_clustering = deltadensity_result.drop('community_id', axis = 1)
    db = DBSCAN(eps=eps, min_samples=min_sample).fit(to_clustering)
    core_samples_mask = np.zeros_like(db.labels_, dtype=bool)
    core_samples_mask[db.core_sample_indices_] = True
    group = pd.Series(db.labels_, name='group')
    count = pd.Series(group).value_counts()
    print(count)
    return_df = pd.concat([deltadensity_result, group], axis=1)
    return return_df
    # n_clusters_ = len(set(labels)) - (1 if -1 in labels else 0)
    # print(n_clusters_)


def dbscan_derivative_clustering(deltadensity_result, eps, min_sample, n_diff=1):
    to_diff = deltadensity_result.drop('community_id', axis=1)
    diff = []
    for i in range(0,len(deltadensity_result)):
        diff.append(list(np.diff(to_diff.loc[i, ],n=n_diff)))
    to_clustering = pd.DataFrame(diff)
    # to_clustering = StandardScaler().fit_transform(to_clustering)
    db = DBSCAN(eps=eps, min_samples=min_sample).fit(to_clustering)
    core_samples_mask = np.zeros_like(db.labels_, dtype=bool)
    core_samples_mask[db.core_sample_indices_] = True
    group = pd.Series(db.labels_, name='group')
    count = pd.Series(group).value_counts()
    print(count)
    return_df = pd.concat([deltadensity_result,group],axis=1)
    return return_df

def kmeans_derivative_clustering(deltadensity_result, n_cluster, n_diff=1):
    to_diff = deltadensity_result.drop('community_id', axis=1)
    diff = []
    for i in range(0, len(deltadensity_result)):
        diff.append(list(np.diff(to_diff.loc[i,], n=n_diff)))
    to_clustering = pd.DataFrame(diff)
    # to_clustering = StandardScaler().fit_transform(to_clustering)
    db = KMeans(n_clusters=n_cluster).fit(to_clustering)
    group = pd.Series(db.labels_, name='group')
    count = pd.Series(group).value_counts()
    print(count)
    return_df = pd.concat([deltadensity_result, group], axis=1)
    return return_df

def kmeans_deltadensity_clustering(deltadensity_result, n_cluster):
    to_clustering = deltadensity_result.drop('community_id', axis=1)
    # to_clustering = StandardScaler().fit_transform(to_clustering)
    db = KMeans(n_clusters=n_cluster).fit(to_clustering)
    group = pd.Series(db.labels_, name='group')
    count = pd.Series(group).value_counts()
    print(count)
    return_df = pd.concat([deltadensity_result, group], axis=1)
    return return_df


def describe_derivative_deltadensity_distance(deltadensity_result, n_diff=1):
    to_diff = deltadensity_result.drop('community_id', axis=1)
    diff = []
    for i in range(0, len(deltadensity_result)):
        diff.append(list(np.diff(to_diff.loc[i,],n=n_diff)))
    to_find_euclidean = pd.DataFrame(diff)
    euclidean_distance_list = []
    for i in range(0,len(to_find_euclidean)):
        for j in range(i+1,len(to_find_euclidean)):
            euclidean_distance_list.append(np.linalg.norm(to_find_euclidean.loc[i, ]-to_find_euclidean.loc[j, ]))
    print(pd.Series(euclidean_distance_list).describe())


def describe_deltadensity_distance(deltadensity_result):
    to_find_euclidean = deltadensity_result.drop('community_id', axis=1)
    euclidean_distance_list = []
    for i in range(0, len(to_find_euclidean)):
        for j in range(i+1, len(to_find_euclidean)):
            euclidean_distance_list.append(np.linalg.norm(to_find_euclidean.loc[i, ]-to_find_euclidean.loc[j, ]))
    print(pd.Series(euclidean_distance_list).describe())


result = read_csv('../data/delta_density_result/result_for_clustering.csv')
describe_derivative_deltadensity_distance(result, n_diff=2)
# dbscan_derivative_clustering(result, 0.00, 4)