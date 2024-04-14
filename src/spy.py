from src import app, db, bcrypt, login_manager, domain_name
from src.models import User, Role, SpyPixel, Log
from flask import send_file, request, render_template, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
import datetime
import urllib.request
import json
import os

# ----------------- User Authentication -----------------

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

@app.route('/')
def index():
    if current_user.is_authenticated and current_user.role.name == 'admin':
        return render_template('index.html', current_user=current_user)
    else:
        return render_template('login.html')
    




# ----------------- SPY PIXEL -----------------



@app.route('/create_pixel', methods=['GET', 'POST'])
@login_required
def create_pixel():
    if request.method == 'POST':
        pixel_tag = request.form['pixel_tag']
        user_id = current_user.id
        pixel = SpyPixel.query.filter_by(pixel_tag=pixel_tag).first()
        if pixel:
            flash('Pixel already exists!', 'danger')
        else:
            new_pixel = SpyPixel(user_id=user_id, pixel_tag=pixel_tag)
            db.session.add(new_pixel)
            db.session.commit()
            flash('Pixel created!', 'success')

            # Copy the pixel.png image to the media folder with the pixel_tag_pixel.png name
            with open('/app/src/static/pixel.png', 'rb') as f:
                with open(f'/app/src/media/{pixel_tag}_pixel.png', 'wb') as f2:
                    f2.write(f.read())
    return render_template('create_pixel.html', current_user=current_user)

@app.route('/view_pixels')
@login_required
def view_pixels():
    dn = domain_name
    pixels = SpyPixel.query.filter_by(user_id=current_user.id).all()
    return render_template('view_pixels.html', pixels=pixels, current_user=current_user, url=dn)


@app.route('/pixel/<pixel_tag>')
def pixel(pixel_tag):
    pixel = SpyPixel.query.filter_by(pixel_tag=pixel_tag).first()
    if not pixel:
        return 'Pixel tag not found', 404
    # check if the file exists
    try:
        with open(f'/app/src/media/{pixel_tag}_pixel.png', 'rb') as f:
            pass
    except FileNotFoundError:
        return 'Pixel image not found', 404

    time = datetime.datetime.now()
    time_str = datetime.datetime.strftime(time, '%Y-%m-%d %H:%M:%S')
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
    log_message = f'T:{time_str} - IP:{ip} - Geolocation:{geolocation_data} - User-Agent:{ua}\n'
    print(log_message)

    with open(f'/app/log_{pixel_tag}.txt', 'a') as f:
        f.write(log_message)

    # Create a new log entry
    log = Log(spy_pixel_id=pixel.id, time=time, ip=ip, user_agent=ua, data=geolocation_data)
    db.session.add(log)
    db.session.commit()
    
    # Serve the pixel.png image
    return send_file(f'/app/src/media/{pixel_tag}_pixel.png', mimetype='image/png')

# delete pixel.id
@app.route('/delete_pixel/<int:pixel_id>')
@login_required
def delete_pixel(pixel_id):
    pixel = SpyPixel.query.get(pixel_id)
    if pixel:
        # Delete the logs associated with the spypixel
        logs = Log.query.filter_by(spy_pixel_id=pixel_id).all()
        for log in logs:
            db.session.delete(log)

        # Delete the pixel.png image
        try:
            with open(f'/app/src/media/{pixel.pixel_tag}_pixel.png', 'rb') as f:
                pass
        except FileNotFoundError:
            return 'Pixel image not found', 404
        else:
            os.remove(f'/app/src/media/{pixel.pixel_tag}_pixel.png')
    
        # Delete the spypixel
        db.session.delete(pixel)
        db.session.commit()

        flash('Pixel deleted!', 'success')
    return redirect(url_for('view_pixels'))

if __name__ == '__main__':
    app.run()
