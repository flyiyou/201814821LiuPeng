import os
import math
import numpy
import shutil
import VSM
import operator

#将词典分为训练词典和测试词典
def devide_dict(filedict):
    traindict = {}
    testdict = {}
    for file in filedict.keys():
        i=0
        traindict[file]= {}
        testdict[file]= {}
        for text in filedict[file].keys():
            if i<len(filedict[file])*0.8:
                traindict[file][text]=filedict[file][text]
            else:
                testdict[file][text]=filedict[file][text]
            i+=1
    return traindict ,testdict

#计算余弦相似度
def similar(train_list,test_list,dict_len):
    trainlen=0.0
    testlen=0.0
    instance=0.0
    cos=0.0
    i=0
    for n in range(dict_len):
        train_list[n]=float(train_list[n])
        test_list[n]=float(test_list[n])

    for i in range(dict_len):
        trainlen+=(train_list[i])*(train_list[i])
        testlen += (test_list[i])*(test_list[i])
        if (train_list[i]>0)and (test_list[i]>0):
            instance+=test_list[i]*train_list[i]
        i+=1
    cos= instance/(math.sqrt(trainlen)*math.sqrt(testlen))
    return cos

#用knn进行分类
def knn(tr_path,te_path,dict_len,k=10):
    right_num = 0
    
    simi_list = 0
    train_vector = []
    file_name = []
    for train_file in os.listdir(tr_path):  #得到训练向量列表，三维，文件夹号+二维向量
        file_name.append(str(train_file))
        flielist = []
        train_vector.append(flielist)
        tr_data = open(tr_path+"/"+train_file,"rb")
        tr_lines = tr_data.readlines()
        for line in tr_lines:
            numbers = line.split()
            flielist.append(numbers)
    for test_file in os.listdir(te_path):
        test_vector = []  #只存一维向量
        te_data = open(te_path+"/"+test_file,"rb")
        te_lines =te_data.readlines()
        test_num = 0
        for line in te_lines:
            test_vector = line.split()
            test_num+=1
            simi_list = []
            for i in range(len(train_vector)):
                for j in range(len(train_vector[i])):
                    cos=similar(test_vector,train_vector[i][j],dict_len)
                    simi_list.append([cos,test_file])
                    j+=1
                i+=1
            static = {}
            simi = sorted(simi_list)
            for n in range(len(simi)) :
                if simi[n][1] in static:
                    static[simi[n][1]]+=1
                else:
                    static[simi[n][1]]=1 
                n+=1
            outcome=sorted(static,key=lambda x:static[x])[-1]
            if outcome==test_file:
                right_num+=1
        currect_rate = 0.0
        currect_rate = right_num/test_num
        print(currect_rate)    
    
if __name__== "__main__":
    key=10
    #devide()
    path_all='./data/20news-18828'
    train_path='./data/train_vsm'
    test_path='./data/test_vsm'
    raw_dict = {}
    final_dict = {}
    All_dict = VSM.Get_File(path_all)
    VSM.Split_Static(All_dict,path_all)
    VSM.IDF(All_dict,raw_dict)
    final_dict=VSM.TF_IDF(path_all,All_dict,raw_dict)
    train_dict ,test_dict =devide_dict(All_dict)
    VSM.Build_VSM(train_path,train_dict,final_dict)
    VSM.Build_VSM(test_path,test_dict,final_dict)
    knn(train_path,test_path,len(final_dict))