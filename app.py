from flask import Flask,request,Response
from sklearn import linear_model
import os
import json
import pickle

port = int(os.getenv("PORT", 3000))
# API server
app = Flask(__name__)
logReg = linear_model.LogisticRegression()
@app.route('/trains', methods=['POST'])
def train():
    try:
        pass_list = []
        y_list = []
        json_= request.get_json(force=True)
        print(">>>>>>>>>> json object",type(json_),'get object',json_[0])
        for i in json_:
            #  json_ = json.loads(json)
            object_list=[]
            param1 = i['Age']
            object_list.append(param1)
            param2 = i['Sex']
            object_list.append(param2)
            param3 = i['Embarked']
            object_list.append(param3)
            param4 = i['y']
            y_list.append(param4)
            #object_list.append(param4)
            print (param1,param2,param3)
            pass_list.append(object_list)
        logReg.fit(pass_list,y_list)
        print("here")
        pickle.dump(logReg, open('logReg.pkl', 'wb'))
        return 'Model Trainedsd'
    except Exception as e:
        print(e)
@app.route('/predict', methods=['POST'])
def predict():
    try:
        pass_list_predict = []
        json_predict = request.get_json(force=True)
        print(">>>>>>>>>> json object", type(json_predict), 'get object', json_predict[0])
        for i in json_predict:
            object_list_predict = []
            param1 = i['Age']
            object_list_predict.append(param1)
            param2 = i['Sex']
            object_list_predict.append(param2)
            param3 = i['Embarked']
            object_list_predict.append(param3)
            print(param1, param2, param3)
            pass_list_predict.append(object_list_predict)
            logReg = pickle.load(open('logReg.pkl', 'rb'))
            print("pickle")
        prediction = (logReg.predict(pass_list_predict))
        print("prediction",predict)
        if (prediction[0] == 0):
            result = "spam"
        else:
            result = "valid"

        msg = {
            "message": "Email is %s" % (result)
        }
        resp = Response(response=json.dumps(msg),
                        status=200, \
                        mimetype="application/json")
        return resp
    except Exception as e:
        print(e)
if __name__ == '__main__':
    app.run(host='0.0.0.0',port=port)