import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from scipy import sparse

data_items = pd.read_csv('input_data_new.csv', index_col=0)
df = data_items.transpose()
similarity = df.corr()

friends = pd.read_csv("node_pair.txt", header =None, delimiter = "\t")

a = friends[0].value_counts().tolist()
a.sort(reverse = True)

b = friends[0].value_counts().keys().tolist()

def getFriends(similarityMatrix, user, k):
    corr =  similarityMatrix[user].sort_values(ascending=False)
    for val in list(corr[1:k+1].index):
        print(str(user) + ' ' + str(val))
        f = open("appu_output2.txt","a")
        f.write(str(user) + ' ' + str(val) + '\n')
        f.close()

for i in range (0,1348):
    getFriends(similarity, b[i].strip(),a[i])
