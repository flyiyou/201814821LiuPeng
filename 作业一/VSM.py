import os
import math
from textblob import TextBlob
from textblob import Word
import re
#获取文件
def Get_File (path):
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
            #TFdict = {}
            textdict[text] = {}
        filedict[file]=textdict    
    return filedict

#分词并计算TF
def Split_Static(filedict,path):
    for file in filedict.keys():
        for text in filedict[file].keys():
            TFdict = {}
            filedict[file][text] = {}
            worddata = open(path + "/" + file + "/" + text,"rb")
            text_t = worddata.read().decode('utf-8','ignore')
            textlow = text_t.lower()
            preword = re.sub('[^a-zA-Z]',' ',textlow)  #去除非字母字符
            words = preword.split()
            for word in words:
                if not (word in TFdict):
                        TFdict[word]=1
                else :
                    TFdict[word]+=1
            '''lines=worddata.readlines()
            for line in lines:
                line = line.lower()
                line_replace = TextBlob(str(line).replace("\\\\n", " ").replace("\\\\t", " ").replace("\\"," ").replace("'"," ").replace("/"," "))
                for word in line_replace.words:
                    if not (word in TFdict):
                        TFdict[word]=1+math.log10(line_replace.words.count(word))'''
            filedict[file][text] = TFdict
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
    for key in dict.keys():
        idf = math.log10(18829/dict[key])
        dict[key]=idf
    with open("./data"+"/"+"all_fre"+".txt", "w+", encoding="utf-8") as output:
	    for key in dict.keys():
		    output.write(key + ":" + str(dict[key]) + "\n")   #保存IDF
    

#计算TF*IDF并筛选词典,返回更新后的词典
def TF_IDF(path,filedict,dict):
    fin_dict = {}
    #dict_t = {}
    #for key in dict.keys():
    #    dict_t[key]=0
    for file in filedict.keys():
        for text in filedict[file].keys():
            for word in list(filedict[file][text]):  #遍历到单词
                if word in dict:
                    TF=filedict[file][text][word]
                    TFIDF=round(TF*dict[word],4)#保留小数点后四位
                    filedict[file][text][word]=TFIDF
                    if (TFIDF >=15)and not(word in fin_dict):  #加到新词典
                        #print(str(word),TFIDF)
                        fin_dict[word]=dict[word]
                    '''if TFIDF>=2:          #########################
                        filedict[file][text].pop(word)
                        dict.pop(word)
                    else :
                        dict[word]=TFIDF '''
            '''with open(path+"/"+file+"/"+text+"_frequence.text", "w+", encoding="utf-8") as output:
                for key in dict.keys():
                    output.write(key + ":" + str(dict[key]) + "\n")'''

    with open("./data"+"/"+"final_dict"+".txt", "w+", encoding="utf-8") as output:
	    for key in fin_dict.keys():
		    output.write(key + ":" + str(dict[key]) + "\n")      #保存最终词典
    print(len(fin_dict))
    return fin_dict
#生成向量空间并保存，每个文件夹一个
def Build_VSM(path,filedict,fin_dict):
    if not os.path.exists(path):
        os.mkdir(path)
    #dict_t = {}
    for file in filedict.keys():
        #filepath = path +"/" +file
        #if not os.path.exists(filepath):
        #    os.mkdir(filepath)
        #for key in dict.keys():
            #dict_t[key] = 0
        for text in filedict[file].keys():
            '''for word in filedict[file][text].keys():
            if word in dict_t:
                dict_t[word]=1 '''
            if not os.path.exists(path+"/"+str(file)):
                with open(path+"/"+str(file), "a", encoding="utf-8") as output:
                    for key in fin_dict.keys():
                        if key in filedict[file][text]:
                            output.write(str(filedict[file][text][key])+" ") 
                        else:
                            output.write("0 ")
                    output.write("\n")

if __name__ == '__main__':                   
    path='./data/20news-18828'
    mkdir_path='./data/20news_fre'
    raw_dict = {}
    final_dict = {}
    Filedict = Get_File(path)
    Split_Static(Filedict,path)
    IDF(Filedict,raw_dict)
    final_dict=TF_IDF(path,Filedict,raw_dict)
    Build_VSM(mkdir_path,Filedict,final_dict)


                





        





