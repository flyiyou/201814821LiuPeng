import json
import numpy as np
from sklearn import metrics
from sklearn.cluster import KMeans
from sklearn.cluster import DBSCAN
from sklearn.cluster import MeanShift
from sklearn.cluster import SpectralClustering
from sklearn.cluster import AgglomerativeClustering
from sklearn.cluster import estimate_bandwidth
from sklearn.mixture import GaussianMixture
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

def k_means(x, y):
   
    max_label = max(label)
    k_means = KMeans(n_clusters=max_label)
    k_means.fit_transform(data)
    k_means_labels = k_means.labels_
    temp_path = "E:\\研一上学期\\Data mining\\作业\\实验三\\k_means_label.csv"
    np.savetxt(temp_path, k_means_labels, fmt="%d", delimiter=",")

    k_means_nmi = metrics.normalized_mutual_info_score(label, k_means_labels)
    print("k_means方法的NMI值是 ", k_means_nmi)


def main():
    vsm()

if __name__ == '__main__':
    main()