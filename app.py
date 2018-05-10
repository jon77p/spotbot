from flask import Flask, render_template, redirect, url_for
import spotifyinfo
app = Flask(__name__)
spotifyinfo.tokenreauth()

@app.route('/')
def index():
    try:
        infile = open('../auth_token', 'rw')
    except:
        open('../auth_token', 'w').close()
    try:
        res = spotifyinfo.info(spotifyinfo.tokeneval(infile.readline().strip()))
    except:
        spotifyinfo.tokenreauth()
        res = spotifyinfo.info(spotifyinfo.tokeneval(infile.readline().strip()))
    finally:
        infile.close()
        return render_template('index.html', res=res)

@app.errorhandler(500)
def servererror(error):
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=3000, use_reloader=True)
