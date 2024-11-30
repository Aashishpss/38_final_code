from flask import Flask, request, render_template, redirect, session
from flask_socketio import SocketIO, emit
from pymongo import MongoClient
import os

# setting up database
client = MongoClient(
    "mongodb+srv://lakshu1000:lakshay1920@mlprojects.n13dkun.mongodb.net/&ssl=true&ssl_cert_reqs=CERT_NONE"
)
db = client["V2V"]
users = db["users"]
data = db["data"]

# setting up app
app = Flask(__name__)
app.secret_key = os.urandom(24)

# Setup SocketIO
socketio = SocketIO(app)

@app.route('/')
def index():
    page = request.args.get('page')
    if page == "user_login":
        return render_template('cover.html', page=page)
    elif page == "user_register":
        return render_template('cover.html', page=page)
    else:
        return render_template('cover.html', page=page)

# user routes
@app.route('/home')
def home():
    if 'user_id' not in session:
        return redirect('/?page=user_signin')
    
    # Fetch the initial data to render on page load
    cars_data = data.find({'_id': 'cars'})[0]
    weather_data = data.find({'_id': 'weather'})[0]

    return render_template('page.html', cars=cars_data, weather=weather_data)

@app.route('/user_signin', methods=['POST'])
def user_signin():
    email = request.form.get('email')
    password = request.form.get('password')
    details = users.find_one({"email": email, "password": password})
    if details == None:
        return redirect('/?page=user_signin')
    else:
        session['user_id'] = details["email"]
        session['user_name'] = details["name"]
        return redirect('/home')

@app.route('/user_signup', methods=['POST'])
def user_signup():
    name = request.form.get('name')
    email = request.form.get('email')
    password = request.form.get('password')
    details = users.find_one({"email": email})
    if details == None:
        users.insert_one({"name": name, "email": email, "password": password})
        return redirect('/home')
    else:
        return redirect('/?page=user_signup')

@app.route('/logout')
def logout():
    session.pop("user_id")
    return redirect("/")

@app.route('/profile')
def profile():
    if 'user_id' not in session:
        return redirect('/login')
    return render_template('prof.html', email=session['user_id'], name=session['user_name'])

# SocketIO event to send updated data to the client
@socketio.on('request_car_data')
def handle_car_data_request():
    # Fetch updated car and weather data from MongoDB
    cars_data = data.find({'_id': 'cars'})[0]
    weather_data = data.find({'_id': 'weather'})[0]
    # Emit the updated data to the client
    emit('update_car_data', {'cars': cars_data, 'weather': weather_data}, broadcast=True)

# running app
if __name__ == '__main__':
    socketio.run(app, debug=True)
