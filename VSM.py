import os
import math
from textblob import TextBlob
from textblob import Word
#获取文件
def Get_Split_File (path):
    """
    path：文件路径
    return: 返回二维列表
    二维字典：第一层是20个文件夹名称，第二层是文件夹下文件名称
    """
    files = os.listdir(path)   # 得到20个文件夹列表
    filedict = {}   #20个文件夹名list
    for file in files :  #遍历20个文件夹
        textfile = os.listdir(path+"/"+file)   #得到文件夹里面text列表
        textdict = {}
        filedict[file] = {}    #每个文件夹下text列表
        for text in textfile: #遍历文件夹下每个text
            #IFdict = {}
            textdict[text] = {}
        filedict[file]=textdict    
    return filedict

#分词并计算IF
def Split_Static(filedict,path):
    for file in filedict.keys():
        for text in filedict[file].keys():
            IFdict = {}
            filedict[file][text] = {}
            worddata = open(path + "/" + file + "/" + text,"r",encoding="ISO-8859-1")
            lines=worddata.readlines()
            for line in lines:
                line = line.lower()
                line_replace = TextBlob(str(line).replace("\\\\n", " ").replace("\\\\t", " ").replace("\\"," ").replace("'"," ").replace("/"," "))
                for word in line_replace.words:
                    if not (word in IFdict):
                        IFdict[word]=line_replace.words.count(word)
            filedict[file][text] = IFdict
    return filedict
#计算IDF
def IDF(filedict,dict):
    for file in filedict.keys():
        for text in filedict[file].keys():
            for word in filedict[file][text].keys():
                if not (word in dict):
                    dict[word]=1
                else :
                    dict[word]+=1
    print(len(dict))
    with open("./data"+"/"+"all_fre"+".txt", "w+", encoding="utf-8") as output:
	    for key in dict.keys():
		    output.write(key + ":" + str(dict[key]) + "\n")
    for key in dict.keys():
        idf = math.log10(18829/dict[key])
        dict[key]=idf

#计算IF*IDF并筛选词典
def IF_IDF(path,filedict,dict):
    dict_t = {}
    for key in dict.keys():
        dict_t[key]=0
    for file in filedict.keys():
        for text in filedict[file].keys():
            for word in list(filedict[file][text]):
                if word in dict:
                    IF=filedict[file][text][word]
                    IFIDF=IF*dict[word]
                    filedict[file][text][word]=IFIDF
                    if IFIDF<=1.2:          #########################
                        filedict[file][text].pop(word)
                        dict.pop(word)
                    else :
                        dict[word]=IFIDF
            '''with open(path+"/"+file+"/"+text+"_frequence.text", "w+", encoding="utf-8") as output:
                for key in dict.keys():
                    output.write(key + ":" + str(dict[key]) + "\n")'''
    print(len(dict))
#生成向量空间并保存，每个文本一个
def Build_VSM(path,filedict,dict):
    os.mkdir(path)
    dict_t = {}
    for file in filedict.keys():
        filepath = path +"/" +file
        os.mkdir(filepath)
        for text in filedict[file].keys():
            for key in dict.keys():
                dict_t[key] = 0
            for word in filedict[file][text].keys():
                if word in dict_t:
                    dict_t[word]=1
            with open(filepath+"/"+text+"_fre.text", "w+", encoding="utf-8") as output:
                for key in dict.keys():
                    output.write(key + ":" + str(dict[key]) + " ")    

            
            


if __name__ == '__main__':                   
    path='./data/20news-18828'
    mkdir_path='.data/20news_fre'
    dict = {}
    Filedict = Get_Split_File(path)
    Split_Static(Filedict,path)
    IDF(Filedict,dict)
    IF_IDF(path,Filedict,dict)
    Build_VSM(mkdir_path,Filedict,dict)


                





        





