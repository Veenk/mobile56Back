from flask import Flask, request, jsonify
import operator
from vtbReq import vtbReq
import json

app = Flask(__name__)
BASE = "https://gw.hackathon.vtb.ru"

@app.route('/v1/cars/<brand>', methods=['GET'])
def getCars(brand):
    bm = askFromMP(brand)
    print(bm)
    return json.dumps(bm)


@app.route('/v1/cars/<brand>/<model>', methods=['GET'])
def getCars1(brand, model):
    bm = askFromMP(brand + " " + model)
    print(bm)
    return json.dumps(bm)


@app.route('/v1/cars/recognition', methods=['POST'])
def sapnuPuas():
    image_64 = request.get_json()
    image_64 = "{\"content\":\"" + image_64['content'] + "\"}"
    headers = {
        'x-ibm-client-id': '06cd3ba02dcc18ad47c27a25d2a41c4e',
        'content-type': "application/json",
        'accept': "application/json"
    }
    req = vtbReq(headers, image_64, BASE + "/vtb/hackathon/car-recognize")
    vtbRes = req.postResponse()
    if vtbRes.status_code == 200:
        prob_this_car = max(vtbRes.json()["probabilities"].items(), key=operator.itemgetter(1))[0]
        model = askFromMP(prob_this_car)
        return json.dumps(model) if vtbRes.json()["probabilities"][prob_this_car] > 0.1 else json.dumps([])
    else:
        return json.dumps({"status": vtbRes.status_code})


def askFromMP(value):
    carjson = []
    brand_model = value.split(" ")

    headers = {
        'x-ibm-client-id': '06cd3ba02dcc18ad47c27a25d2a41c4e',
        'accept': "application/json"
    }
    link = "/vtb/hackathon/marketplace"
    askVtb = vtbReq(headers=headers, payload=None, link=BASE+link)

    response = askVtb.getResponse()

    for dict in response.json()["list"]:
        if dict['title'] == brand_model[0]:
            if len(brand_model) == 1:
                carjson.append(dict)
            else:
                for model in dict['models']:
                    if model['title'] == brand_model[1]:
                        carjson.append(model)
    return carjson

if __name__ == '__main__':
    app.run(debug=True, port=5000)
