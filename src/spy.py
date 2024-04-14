from src import app, db, bcrypt, login_manager
from src.models import User, Role
from flask import send_file, request, render_template, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
import datetime
import urllib.request
import json

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and bcrypt.check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('index'))
        else:
            error = "Invalid username or password. Please try again."
            return render_template('login.html', error=error)
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

'''
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Check if username already exists
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash('Username already exists. Please choose a different one.', 'error')
            return redirect(url_for('register'))

        # Create a new user
        new_user = User(username=username, password=password)  # Note: You should hash the password before saving to the database
        db.session.add(new_user)
        db.session.commit()

        flash('Registration successful! You can now log in.', 'success')
        return redirect(url_for('login'))

    return render_template('register.html')
'''

@app.route('/')
def index():
    if current_user.is_authenticated and current_user.role.name == 'admin':
        return render_template('index.html', current_user=current_user)
    else:
        return render_template('index.html')

@app.route('/pixel')
def pixel():
    time = datetime.datetime.now()
    time = datetime.datetime.strftime(time, '%Y-%m-%d %H:%M:%S')
    ua = request.headers.get('User-Agent')

    if request.headers.get('CF-Connecting-IP') is not None:
        ip = request.headers.get('CF-Connecting-IP')
    elif request.environ.get('HTTP_X_FORWARDED_FOR') is None:
        ip = request.environ['REMOTE_ADDR']
    else:
        ip = request.environ['HTTP_X_FORWARDED_FOR']
    
    # Fetch geolocation data
    with urllib.request.urlopen(f"https://geolocation-db.com/jsonp/{ip}") as url:
        data = url.read().decode()
        data = data.split("(")[1].strip(")")
        geolocation_data = json.loads(data)
    
    # Log geolocation data
    print(f'T:{time} - IP:{ip} - Geolocation:{geolocation_data} - User-Agent:{ua}\n')

    with open('/app/log.txt', 'a') as f:
        f.write(f'T:{time} - IP:{ip} - Geolocation:{geolocation_data} - User-Agent:{ua}\n')
    return send_file('media/pixel.png', mimetype='image/png')

if __name__ == '__main__':
    app.run()
