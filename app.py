from flask import Flask, request, render_template
import recommenders
import pandas as pd
from collections import Counter


outputList = []
nameList = []
screenNameList = []
name = None
app = Flask(__name__)


@app.route("/")
def main():
    global nameList
    global screenNameList
    
    with open("node_map.txt", "r",  encoding="utf8") as file:
        userMap = file.read().split("\n")
    
    nameList.extend([entry.split(" \t ")[1] for entry in userMap])
    screenNameList.extend([entry.split(" \t ")[0] for entry in userMap])
    return render_template('index.html', userList=nameList)


@app.route('/', methods=["POST"])
def recommender():
    global name
    global outputList
    new = 0
    name = request.form['escreenname']
    
    if name not in nameList:
        screen_name = name
        new = 1
    else:
        idx = nameList.index(name)
        screen_name = screenNameList[idx]
    
    followers_list = recommenders.show(screen_name, 10)
    outputList = []
    
    if new == 0:
        for entry, value in followers_list:
            idx = screenNameList.index(entry)
            outputList.append(nameList[idx])
    else:
        for entry in followers_list:
            idx = screenNameList.index(entry)
            outputList.append(nameList[idx])
        new = 0
    
    return render_template('recommender.html', fl_list = outputList)


@app.route('/result/<fname>',methods=["POST"])
def result(fname):
    global outputList
    
    if request.method == "POST":
        
        if request.form['result_button'] == 'Accept':
            fb = "%s\taccepted\t%s\n" % (name, fname)
        elif request.form['result_button'] == 'Decline':
            fb = "%s\tdeclined\t%s\n" % (name, fname)
        
        fh = open("feedback.txt", "a+")
        fh.write(fb)
        fh.close()
        outputList.remove(fname)
        
        return render_template('recommender.html', fl_list = outputList)


@app.route('/reinforce',methods=["POST"])
def reinforcement():
    declinedAttrList = []
    
    with open("feedback.txt", "r") as file:
        fb = file.read().split("\n")
    
    data = pd.read_csv("input_data_new.csv", index_col=0)
    dataT = data.transpose()
    fb = fb[:-1]
    
    for entry in fb:
        info = entry.split("\t")
        
        if (info[1] == "declined"):
            idx1 = nameList.index(info[0])
            name1 = screenNameList[idx1]
            idx2 = nameList.index(info[2])
            name2 = screenNameList[idx2]
            commonAttr = list(set(list(dataT[name1].nonzero()[0])) & set(list(dataT[name2].nonzero()[0])))
            
            for idx in commonAttr:
                declinedAttrList.append(data.columns[idx])
    
    cnt = Counter(declinedAttrList)
    attrList = [k for k, v in cnt.items()]
    
    return render_template('evaluate.html', attrList = attrList)


if __name__ == "__main__":
    app.run()
