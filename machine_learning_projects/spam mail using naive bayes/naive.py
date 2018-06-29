import os
import numpy as np 
import setting
from collections import Counter
from sklearn.metrics import confusion_matrix
from sklearn.naive_bayes import MultinomialNB
from sklearn.model_selection import train_test_split
import pickle as cPickle
import json
import nltk
from nltk.stem.porter import *
from sklearn.model_selection import cross_val_score

np.set_printoptions(threshold=np.nan)

stemmer = PorterStemmer()
def make_Dictionary(train_dir_spam,train_dir_ham):
    emails = os.listdir(train_dir_spam)    
    all_words = []       
    for mail in emails:
        mail = os.path.join(train_dir_spam,mail)   
        with open(mail,encoding = 'latin1') as m:
            for i,line in enumerate(m):
                if i == 1:  
                    words = line.split()
                    check = []
                    for word in words:
                        if word.isalpha()== False or len(word)== 1 :
                            check.append(word)
                    for i in check:
                        words.remove(i)
                    all_words += words
    
    emails = os.listdir(train_dir_ham)
    for mail in emails:
        mail = os.path.join(train_dir_ham,mail)   
        with open(mail,encoding = 'latin1') as m:
            for i,line in enumerate(m):
                if i == 1:  
                    words = line.split()
                    check = []
                    for word in words:
                        if word.isalpha()== False or len(word)== 1 :
                            check.append(word)
                    for i in check:
                        words.remove(i)
                    all_words += words
    print(len(all_words))
    new_voc=set()
    new_all_words=[]
    for word in all_words:
        if word not in nltk.corpus.stopwords.words('english'):
            w = stemmer.stem(word)
            new_voc.add(w)
            new_all_words.append(w)
    new_voc = list(new_voc)
    dictionary = Counter(new_all_words)

    for w in dictionary:
        if dictionary[w] <2:
            new_voc.remove(w)
    print(len(new_voc))

    return new_voc

def extract_features(mail_dir_spam,mail_dir_ham,new_voc): 
    files = [os.path.join(mail_dir_spam,fi) for fi in os.listdir(mail_dir_spam)]
    files2 = [os.path.join(mail_dir_ham,fi) for fi in os.listdir(mail_dir_ham)] 
    #features_matrix = np.zeros((len(files)+len(files2),len(dictionary)),dtype=int)
    features_matrix = []
    print(len(files), len(files2))
    #train_labels = np.zeros((len(files)+len(files2)))
    train_labels=[]
    docID = 0
    for fil in files:
        doc=""
        with open(fil,encoding='latin1') as fi:
            for line in fi:
                doc = doc +" "+line.strip()
        tokens_doc= doc.split(" ")
        tokens_new=[]
        for w in tokens_doc:
            new_w=stemmer.stem(w)
            if (new_w in new_voc):
                tokens_new.append(new_w)
        doc_vecto=[0 for i in range(len(new_voc))]
        for w in tokens_new:
            doc_vecto[new_voc.index(w)]+=1
        label_vecto = 1
        features_matrix.append(doc_vecto)
        train_labels.append(label_vecto) 
    for fil in files2:
        doc=""
        with open(fil,encoding='latin1') as fi:
            for line in fi:
                doc = doc +" "+line.strip()
        tokens_doc= doc.split(" ")
        tokens_new=[]
        for w in tokens_doc:
            new_w=stemmer.stem(w)
            if (new_w in new_voc):
                tokens_new.append(new_w)
        doc_vecto=[0 for i in range(len(new_voc))]
        for w in tokens_new:
            doc_vecto[new_voc.index(w)]+=1
        label_vecto = 0
        features_matrix.append(doc_vecto)
        train_labels.append(label_vecto)


        
    return np.asarray(features_matrix),train_labels

dic = make_Dictionary(setting.spam_url,setting.ham_url)
#print(extract_features(setting.url_mail_test,dic,1))
features_matrix,labels = extract_features(setting.spam_url,setting.ham_url,dic)
print(features_matrix.shape)
np.save('feature_matrix.npy',features_matrix)
np.save('labels.npy',labels)
X_train, X_test, y_train, y_test = train_test_split(features_matrix, labels, test_size=0.40)
# try:
#     with open('my_dumped_classifier.pkl', 'rb') as fid:
#         model = cPickle.load(fid)
#     print('Load model success')
# except:
print(X_train[1])
model = MultinomialNB()
model.fit(X_train,y_train)
scores = cross_val_score(model,X_train,y_train,cv=5)
print(scores.mean())
result = model.predict(X_test)
count = 0
for i in range(result.size):
    if result[i] == y_test[i]:
        count+=1
print(count/len(result)*100)
# save the classifier
with open('my_dumped_classifier.pkl', 'wb') as fid:
    cPickle.dump(model, fid)
print('Save model success')
json.dump(dic, open(setting.save_dict, 'w'))
print('Save dict success')


# string_input = input('Nhap file email cua ban vao day : ')
# string_input = os.path.join(setting.url_mail_test,string_input)
# with open(string_input,encoding = 'latin1') as m:
#     all_words = []
#     for i,line in enumerate(m):
#         if i == 1:  #Body of email is only 3rd line of text file
#             words = line.split()
#             check = []
#             for word in words:
#                 if word.isalpha()== False or len(word)== 1 :
#                     check.append(word)
#             for i in check:
#                 words.remove(i)
#     all_words += words



    