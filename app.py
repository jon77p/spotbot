from flask import Flask, render_template
import spotifyinfo
app = Flask(__name__)

@app.route('/')
def index():
    res = spotifyinfo.info()
    #printed = res[0] + res[1] + res[2]
    #return printed
    #return render_template('index.html', res=res)
    test = render_template('index.html', res=res)
    return test

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=3000, use_reloader=True)
