import os
import numpy as np 
import setting
from sklearn.naive_bayes import MultinomialNB
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import cross_val_score 
import pickle as cPickle
import json
from nltk.stem.porter import *

np.set_printoptions(threshold=np.nan)

stemmer = PorterStemmer()
def extract_features(mail_dir_test,new_voc): 
    files = [os.path.join(mail_dir_test,fi) for fi in os.listdir(mail_dir_test)]
    #features_matrix = np.zeros((len(files)+len(files2),len(dictionary)),dtype=int)
    features_matrix = []
    #train_labels = np.zeros((len(files)+len(files2)))
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
        features_matrix.append(doc_vecto)
    return np.asarray(features_matrix)
# load it again
with open('my_dumped_classifier.pkl', 'rb') as fid:
    model = cPickle.load(fid)
print('Load model success')
dic = json.load(open(setting.save_dict))
print(dic)
print('Load dict success')
feature = extract_features(setting.url_mail_test,dic)
print(feature)
count = 0 
print(len(dic))
prediction  = model.predict_proba(feature)
print(prediction)

# print(model.predict(feature))