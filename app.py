from flask import Flask, render_template, redirect, url_for, Response, jsonify, request
from flask_restful import Resource, Api
from flask_socketio import SocketIO, emit, send
import subprocess
import spotifyinfo
import re
app = Flask(__name__)
spotifyinfo.tokenreauth()


api = Api(app)
socketio = SocketIO(app)

###### Flask ######

@app.route('/')
def index():
    res = getspotify_np()
    return render_template('index.html', res=res)

###### WebSockets ######

@socketio.on('connect')
def connect():
    print('Client connect!')

@socketio.on('connect', namespace='/devices')
def connectDevices():
    print('Client connected to /devices')
    emit('message', {'data': "Hello from server to device!"}, namespace='/devices')
    emit('connected')

@socketio.on('test', namespace='/devices')
def test(msg):
    emit('message', {'data': msg}, namespace='/devices', broadcast=True)

@socketio.on('disconnect', namespace='/devices')
def device_disconnect():
    print('Client disconnected from devices')

@socketio.on('disconnect')
def disconnect():
    print('Client disconnected')

@socketio.on('get_nowplaying', namespace='/devices')
def get_nowplaying():
    np_data = getspotify_np()
    emit('nowplaying', {'data': np_data}, namespace='/devices')

###### API ######

class Refresh(Resource):
    def get(self):
        return {'message': 'refreshing devices!'}
    def put(self):
        data = request.form['data']
        if (data == "test"):
            try:
                socketio.emit('refresh', namespace='/devices', broadcast=True)
                socketio.disconnect()
                return {'message': 'success!'}
            except:
                return {'message': 'failure!'}
        else:
            return {'message': 'invalid'}

api.add_resource(Refresh, '/api/refresh')

class Info(Resource):
    def get(self):
        return getspotify_np()

api.add_resource(Info, '/api/info')

###### Functions ######

def getspotify_np():
    res = {"artist": "N/A", "track": "N/A", "img": "static/img/spotify_connect.png", "uri": "https://open.spotify.com"}
    try:
        infile = open('../auth_token', 'r')
    except:
        infile2 = open('../auth_token', 'w')
        infile2.close()
        spotifyinfo.tokenreauth()
        infile = open('../auth_token', 'r')
    try:
        res = spotifyinfo.info(spotifyinfo.tokeneval(infile.readline().strip()), '/home/pi/raspotify.log')
    except:
        infile.close()
        spotifyinfo.tokenreauth()
        infile = open('../auth_token', 'r')
        res = spotifyinfo.info(spotifyinfo.tokeneval(infile.readline().strip()), '/home/pi/raspotify.log')
    finally:
        infile.close()
        return res

###### Error Handling ######

@app.errorhandler(500)
def servererror(error):
    return redirect(url_for('index'))

if __name__ == '__main__':
    socketio.run(app, debug=False, host='0.0.0.0', port=3000)
