from flask import Flask, send_file, request
# from werkzeug.middleware.proxy_fix import ProxyFix
import datetime
import urllib.request
import json

app = Flask(__name__)

# Ensure Flask is configured to handle proxy headers correctly
# app.wsgi_app = ProxyFix(app.wsgi_app)

@app.route('/')
def index():
    return send_file('index.html', mimetype='text/html')

@app.route('/pixel')
def pixel():
    time = datetime.datetime.now()
    time = datetime.datetime.strftime(time, '%Y-%m-%d %H:%M:%S')
    ua = request.headers.get('User-Agent')
    ip = request.environ['REMOTE_ADDR']
     
    # Fetch geolocation data
    with urllib.request.urlopen(f"https://geolocation-db.com/jsonp/{ip}") as url:
        data = url.read().decode()
        data = data.split("(")[1].strip(")")
        geolocation_data = json.loads(data)
    
    # Log geolocation data
    print(f'T:{time} - IP:{ip} - Geolocation:{geolocation_data} - User-Agent:{ua}\n')

    with open('/app/log.txt', 'a') as f:
        f.write(f'T:{time} - IP:{ip} - Geolocation:{geolocation_data} - User-Agent:{ua}\n')
    return send_file('pixel.png', mimetype='image/png')

if __name__ == '__main__':
    app.run()
