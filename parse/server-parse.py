from flask import Flask, request, json, jsonify
import mongodb as mongo
import config
from ParseVideo import *
from threading import Thread


playListLink = ""
app = Flask(__name__)


@app.route('/setPlayList', methods=['POST'])
def setLink():
    t = Thread(target=getVideosGivenPlayList,args=("PLD6cpMQHuQEQ-005myefm5J9oiXeBXRjJ",request.json["topic"].upper(), request.json["subtopic"]))
    t.start()
    return jsonify({"staus":200})
    #if not request.json:
    #    abort(400)
    #separate = request.json["playListLink"].split("&list=")
    #if len(separate) != 2:
    #    abort(400)
    #playListLink = separate[1]

@app.route('/searchSubtopic', methods=['POST'])
def searchSub():

    if not request.json["topic"] or not request.json["subtopic"]:
        return jsonify({"status":400})
    topic = request.json["topic"].upper().replace(" ","_")
    suggestions = mongo.find(topic, request.json["subtopic"])
    print(suggestions)
    videoLinks = []
    timeStamps = []
    for videoSuggestion in suggestions:
        if videoSuggestion[1][1] == []:
            continue
        timeStamps.append(videoSuggestion[1][1][0]["timeStamp"])
        videoLinks.append(videoSuggestion[1][0])
    

    ret = {
        "videoLink":videoLinks,
        "timeStamps":timeStamps
    }
    print(ret)
    return jsonify(ret)



if __name__ == "__main__":
    app.run(port=6969,host="0.0.0.0",debug=True)
