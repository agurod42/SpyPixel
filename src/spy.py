from flask import Flask, send_file, request
import datetime
import urllib.request

app = Flask(__name__)

@app.route('/')
def index():
    return send_file('index.html', mimetype='text/html')

@app.route('/pixel')
def pixel():
    time = datetime.datetime.now()
    time = datetime.datetime.strftime(time, '%Y-%m-%d %H:%M:%S')
    ua = request.headers.get('User-Agent')
    ip = request.remote_addr
    with urllib.request.urlopen("https://geolocation-db.com/jsonp/"+ ip) as url:
        data = url.read().decode()
        data = data.split("(")[1].strip(")")

    print(f'T:{time} - IP:{data} - User Agent:{ua}\n')

    with open('/app/log.txt', 'a') as f:
        f.write(f'T:{time} - IP:{data} - User Agent:{ua}\n')
    return send_file('pixel.png', mimetype='image/png')

if __name__ == '__main__':
    app.run()
