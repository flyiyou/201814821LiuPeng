import VSM
import KNN
import math
import os
import re


#统计每个单词在每一类中的词频,并生成20个向量,得到每个单词在每类下的词频，每类的单词总数和每类的单词种类数量
def count_train(path,dict):
    files = os.listdir(path)   # 得到20个文件夹列表
    traindict = {}   #20个文件夹名list
    filewordnum = []
    wordcount =0
    for file in files :  #遍历20个文件夹
        wordnum=0  #这一类下单词总数
        categorynum = 0 #单词种类数
        file_dict = {}
        for key in dict.keys():
            file_dict[key]=0
        traindict[file]=file_dict
        textfile = os.listdir(path+"/"+file)   #得到文件夹里面text列表
        for text in textfile: #遍历文件夹下每个text
            worddata = open(path + "/" + file + "/" + text,"rb")
            text_t = worddata.read().decode('utf-8','ignore')
            textlow = text_t.lower()
            preword = re.sub('[^a-zA-Z]',' ',textlow)  #去除非字母字符
            words = preword.split()
            for word in words:
                if word in file_dict:
                        file_dict[word]+=1
                        wordnum +=1
                        wordcount +=1
        filewordnum.append(wordnum)
        with open(path+"/"+str(file), "a", encoding="utf-8") as output:
                    for key in file_dict.keys():
                        output.write(str(traindict[file][text][key])+" ") 
                    output.write("\n")
    return traindict,filewordnum,wordcount


#统计训练集每个文本中的单词词频并计算概率
def NBC(path,traindict,filewordnum,wordcount):
    possible = []
    currect =0
    fileindex=0
    for file in traindict.keys():
        fileindex +=1
        currectnum=0
        textnum=0
        for text in traindict[file].keys():
            textnum+=1
            TFdict = {}
            traindict[file][text] = {}
            worddata = open(path + "/" + file + "/" + text,"rb")
            text_t = worddata.read().decode('utf-8','ignore')
            textlow = text_t.lower()
            preword = re.sub('[^a-zA-Z]',' ',textlow)  #去除非字母字符
            words = preword.split()
            file_dict = {}
            pro =0
            for key in dict.keys():
                file_dict[key]=0
            for word in words:
                if word in file_dict:
                    file_dict[word]+=1
            for key in traindict.keys():
                for word in words:
                    i=0
                    if word in traindict[key]:
                        xcpro= log((traindict[key][word] + 0.0001) / (filewordnum[i]+ wordcount) / (filewordnum[i]/wordcount))
                        pro+=xcpro
                possible.append[pro]
            index=possible.index(max(possible))
            if index==fileindex:
                currectnum+=1
            currect = float(currect/textnum)


if __name__ == '__main__':                   
    path='./data/20news-18828'
    mkdir_path='./data/20news_fre'
    train_path='./data/train_vsm'
    test_path='./data/test_vsm'
    raw_dict = {}
    final_dict = {}
    Filedict = VSM.Get_File(path)
    VSM.Split_Static(Filedict,path)
    VSM.IDF(Filedict,raw_dict)
    final_dict=VSM.TF_IDF(path,Filedict,raw_dict)
    traindict,filewordnum,wordcount=count_train(train_path,final_dict)
    NBC(test_path,traindict,filewordnum,wordcount)

    

