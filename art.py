from flask import Flask
from flask import request
from flask import render_template
from flask import send_file
import json
import time
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError



app = Flask(__name__)
app.config["TEMPLATES_AUTO_RELOAD"] = True
DEVELOPER_KEY = ''
YOUTUBE_API_SERVICE_NAME = 'youtube'
YOUTUBE_API_VERSION = 'v3'

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/search", methods = ["POST", "GET"])
def search():
    if request.method == "POST":
        print(type(request.form))
        req_data = request.form.get("search", "youtube")
        print(req_data)
        youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
                        developerKey=DEVELOPER_KEY)
        search_response = youtube.search().list(q=req_data, part='id,snippet',
                                                maxResults=25).execute()
        videos = []
        count = 0
        #print(json.dumps(search_response))
        # print(i["snippet"]["publishedAt"].split("T")[0])
        for i in search_response["items"]:
            v_data = {}
            if i["id"]["kind"] == "youtube#video" and count < 10 :
                v_data["thumbnails"] = i["snippet"]["thumbnails"]['high']['url']
                v_data["published_at"] = i["snippet"]["publishedAt"].split("T")[0]
                v_data["title"] = i["snippet"]["title"]
                v_data["description"] = i["snippet"]["description"]
                v_data["video_id"] = i["id"]["videoId"]

                videos.append(v_data)
                count += 1
        # print(videos)
        # time.sleep(20)
        return json.dumps(videos)
    elif request.method == "GET":
        return render_template("search.html")

@app.route("/download/<video_id>",methods=["GET"])
def downloadAudio(video_id):
    file_name = '/tmp/taj.mp3'
    print(video_id)
    time.sleep(10)
    return send_file(file_name, mimetype='audio/mpeg3', attachment_filename='video_id.mp3')
