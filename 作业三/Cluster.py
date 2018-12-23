import json
import numpy
from sklearn import metrics
from sklearn.cluster import KMeans
from sklearn.cluster import AffinityPropagation
from sklearn.cluster import DBSCAN
from sklearn.cluster import MeanShift
from sklearn.cluster import SpectralClustering
from sklearn.cluster import AgglomerativeClustering
from sklearn.cluster import estimate_bandwidth

from sklearn.feature_extraction.text import TfidfVectorizer

def vsm():
    """
    将文本转化为向量
    :return:
    """
    reader = open("data.txt",'r', encoding='utf-8')
    documents=[]
    labels=[]
    for line in reader:
        line=json.loads(line)
        documents.append(line['text'])
        labels.append(line['cluster'])
    tfidf2 = TfidfVectorizer(max_df=0.5, min_df=2, max_features=1000, use_idf=True,
                                 stop_words='english')
    data = tfidf2.fit_transform(documents).todense()

    return data,labels

def K_means(x,y):
    k = max(y)
    kmeans = KMeans(k).fit(x)
    pred = kmeans.predict(x)
    NMI = metrics.normalized_mutual_info_score(y,pred)
    print ("K_means:",NMI)

def Affinity_Propagation(x, y):
    aff = AffinityPropagation().fit(x)
    pred = aff.predict(x)
    NMI = metrics.normalized_mutual_info_score(y,pred)
    print ("Affinity_Propagation:",NMI)


def Mean_Shift(x, y):
    mean = MeanShift().fit(x)
    pred = mean.predict(x)
    NMI = metrics.normalized_mutual_info_score(y, pred)
    print ("Mean_Shift:",NMI)


def Spectral_Clustering(x, y):
    k = max(y)
    spec = SpectralClustering(k).fit(x)
    pred = spec.fit_predict(x)
    NMI = metrics.normalized_mutual_info_score(y, pred)
    print("Spectral_Clustering:",NMI)


def Agglomerative_Clustering(x, y):
    k = max(y)
    agg = AgglomerativeClustering(k).fit(x)
    pred = agg.fit_predict(x)
    NMI = metrics.normalized_mutual_info_score(y, pred)
    print("Agglomerative_Clustering:",NMI)




def Dbscan(x, y):
    dbscan = DBSCAN().fit(x)
    pred = dbscan.fit_predict(x)
    NMI = metrics.normalized_mutual_info_score(y, pred)
    print("Dbscan:",NMI)


def main():
    x,y=vsm()
    K_means(x,y)
    Affinity_Propagation(x,y)
    Mean_Shift(x,y)
    Spectral_Clustering(x,y)
    Agglomerative_Clustering(x,y)
    Dbscan(x,y)
if __name__ == '__main__':
    main()
