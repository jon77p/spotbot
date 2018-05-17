from flask import Flask, render_template, redirect, url_for
import spotifyinfo
app = Flask(__name__)
spotifyinfo.tokenreauth()

@app.route('/')
def index():
    res = "N/A", "N/A", "static/img/spotify_connect.png" 
    try:
        infile = open('../auth_token', 'rw')
    except:
        infile2 = open('../auth_token', 'w')
        infile2.close()
        spotifyinfo.tokenreauth()
        infile = open('../auth_token', 'rw')
    try:
        res = spotifyinfo.info(spotifyinfo.tokeneval(infile.readline().strip()))
    except:
        infile.close()
        spotifyinfo.tokenreauth()
        infile = open('../auth_token', 'rw')
        res = spotifyinfo.info(spotifyinfo.tokeneval(infile.readline().strip()))
    finally:
        infile.close()
        return render_template('index.html', res=res)

@app.errorhandler(500)
def servererror(error):
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=3000, use_reloader=True)
