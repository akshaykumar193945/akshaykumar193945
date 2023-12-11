from flask import Flask, render_template, request, redirect, url_for, jsonify, session
from models import db, Profiles, User_Credentials
from flask_login import LoginManager, login_user, login_required, logout_user, current_user

import download_records as dwnld_rcds

app = Flask(__name__)
app.config.from_object('config')

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mydatabase.db'  # Replace with your database URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

with app.app_context():
    db.create_all()
    print("All database created !!!")

app.secret_key = 'your_secret_key'

login_manager = LoginManager()
login_manager.init_app(app)

app.config['PERMANENT_SESSION_LIFETIME'] = 600  # 30 minutes in seconds


@app.route('/check_login_status')
def check_login_status():
    # Check if the user is authenticated
    if current_user.is_authenticated:
        return jsonify({'authenticated': True, 'username': current_user.username})
    else:
        return jsonify({'authenticated': False})

# Define the 'before_request' hook
@app.before_request
def before_request():
    print("Executing 'before_request' hook")
    print(f"Request URL: {request.url}  Request Method: {request.method} Current_User : {current_user}")
    print("iiiiiiiiiiiiiiiiiiiiiiiiiiiiii")

# Define the 'after_request' hook
@app.after_request
def after_request(response):
    print("Executing 'after_request' hook")
    print(f"Response Status Code: {response.status_code}")
    print("ggggggggggggggggggggggggggggggg")
    return response

@app.route('/')
def layout():
    username = session.get('username', None)
    print(username)
    return render_template('layout.html', username=username)

@login_manager.user_loader
def load_user(user_id):
    # Implement logic to load a user from your database or user storage
    # For example, if using a database, you can query the user by ID
    user = User_Credentials.query.get(int(user_id))
    return user

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    session.clear()
    print('in logged_in in logged_in in logged_in in logged_in')
    if request.method == 'POST':
        data = request.get_json()

        username = data.get('username')
        password = data.get('password')
        first_name = data.get('first_name')
        last_name = data.get('last_name')
        email = data.get('email')
        mobile_number = data.get('mobile_number')

        # Check if the username is already in use (you may use your database for this check)
        existing_user = User_Credentials.query.filter_by(username=username).first()
        print("kkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkk")
        if existing_user:
            return jsonify({'error': 'Username is already taken'})

        # Create a new user
        new_user = User_Credentials(username=username, password=password, first_name=first_name, last_name=last_name, email=email, mobile_number=mobile_number)

        # Add and commit the new user to your database
        db.session.add(new_user)
        db.session.commit()

        # Log in the new user after sign-up (optional)
        login_user(new_user)
        # return redirect(url_for('home_content'))
        return jsonify({'message': 'User registered successfully', 'redirect': '/target_page'})

    return render_template('signup.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    # Check user credentials and log in the user
    logout_user()
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = User_Credentials.query.filter(User_Credentials.username == username).first()
        print("ttttttttttttttttttttttt")
        if user and username == user.username and password == user.password:
            login_user(user)
            session['username'] = current_user.username
            return jsonify({'status': 'success', 'redirect': url_for('layout')})
        else:
            print('ssssssssssssssssssssssssssssss')
            return jsonify({'status': 'failure', 'message': 'Invalid credentials'})
    print("llllllllllllllllllllllllllllll")
    return render_template('login.html')



@app.route('/logout')
def logout():
    logout_user()
    session.clear()
    return redirect(url_for('layout'))


@app.route('/admission_form')
@login_required
def admission_form():
    return render_template('admission_form.html')

@app.route('/admit', methods=['POST'])
@login_required
def admit():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        dob = request.form['dob']

        admission_record = Profiles(name=name, email=email, dob=dob, user_id=current_user.username)

        db.session.add(admission_record)
        db.session.commit()
        admission_record = {
            'name': name,
            'email': email,
            'dob': dob,
            'user_id': current_user.username
        }
        return jsonify({'message': 'Record Added successfully', 'admission_record': admission_record})
    return render_template('error.html')
    


@app.route('/courses')
def courses():
    return render_template('courses.html')

@app.route('/admission_records')
@login_required
def admission_records():
    records = Profiles.query.all()
    print(records, "line no 42")
    return render_template('admission_records.html', records=records)

@app.route('/user_records')
@login_required
def user_records():
    records = User_Credentials.query.all()
    print(records, "line no 42")
    return render_template('User_Credentials.html', records=records)

@app.route('/find')
@login_required
def find():
    print("Line no 48")
    return render_template('find.html')

@app.route('/display_record', methods=['POST'])
@login_required
def display_record():
    if request.method == 'POST':
        name = request.form['name']
        records = Profiles.query.filter(Profiles.name == name).all()
        if len(records):
            return render_template('display_record.html', records=records)
        return render_template('error.html', records="Not Found")
    return render_template('error.html')

@app.route('/edit_record_by_id', methods=['POST'])
@login_required
def edit_record_by_id():
    if request.method == 'POST':
        record_id = request.form['record_id']
        record = Profiles.query.get(record_id)
        print(record)
    return render_template('edit_record.html', record=record)

from flask import request, jsonify
import traceback
@app.route('/record_edited/<int:id>', methods=['POST'])
@login_required
def record_edited(id):
    try:
        if request.method == 'POST':
            print('This is request !!!!', request)
            data = request.get_json(force=True)  # Use request.json to parse JSON data
            print("In record edited :", data)
            # Access data properties as needed
            name = data.get('name')
            email = data.get('email')
            dob = data.get('dob')

            record = Profiles.query.get(id)
            print('This is db recode', record)
            if record:
                # Update the record with the data from the JSON request
                record.name = name
                record.email = email
                record.dob = dob
                db.session.commit()

                admission_record = {
                    'name': record.name,
                    'email': record.email,
                    'dob': record.dob
                }
                print("Updation Done !!!")
                return jsonify({'message': 'Record updated successfully', 'admission_record': admission_record})
            else:
                return jsonify({'error': 'Record not found'}), 404
    except Exception as e:
        print(f"Error: {str(e)}")
        traceback.print_exc()
        return jsonify({'error': ' 1 Internal Server Error'}), 500

@app.route('/record_user_edited/<int:id>', methods=['POST'])
@login_required
def record_user_edited(id):
    try:
        if request.method == 'POST':
            data = request.get_json(force=True)  # Use request.json to parse JSON data
            print("In record user edited :", data)

            first_name = data.get('first_name')
            last_name = data.get('last_name')
            email = data.get('email')
            password = data.get('password')
            mobile_number = data.get('mobile_number')

            record = User_Credentials.query.get(id)
            if record:
                record.first_name = first_name
                record.last_name = last_name
                record.email = email
                record.password = password
                record.mobile_number = mobile_number

                db.session.commit()

                user_record = {
                    'first_name': record.first_name,
                    'last_name': record.last_name,
                    'password': record.password,
                    'email': record.email,
                    'mobile_number': record.mobile_number
                }

                print("Updation Done !!!")
                return jsonify({'message': 'Record updated successfully', 'user_record': user_record})
            else:
                return jsonify({'error': 'Record not found'}), 404
    except Exception as e:
        print(f"Error: {str(e)}")
        traceback.print_exc()
        return jsonify({'error': 'Internal Server Error'}), 500

@app.route('/user_profile', methods=['GET'])
@login_required
def user_profile():
    existing_user = User_Credentials.query.filter_by(username=current_user.username).first()
    return render_template('user_profiles.html', existing_user=existing_user)


@app.route('/delete_record_by_id', methods=['POST'])
@login_required
def delete_record_by_id():
    if request.method == 'POST':
        record_id = request.form['record_id']
        record = Profiles.query.get(record_id)
        if record:
            db.session.delete(record)
            db.session.commit()
            print("Record is ", record)
            return render_template('delete_record.html', record=record)
        else: 
            return render_template('error.html')
    print('Error')
    return render_template('error.html')


@app.route('/process_form', methods=['POST'])
@login_required
def process_form():
    dwnld_rcds.download_records()        
    return redirect(url_for('admission_records'))

@app.route('/service')
def service():
    return render_template('service.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/update_record/<int:id>', methods=['GET', 'POST'])
@login_required
def update_record(id):
    # Perform Operation
    record = Profiles.query.get(id)
    print(" in edit records", record)
    return render_template('edit_record.html', record=record)

@app.route('/update_user_record/<int:id>', methods=['GET', 'POST'])
@login_required
def update_user_record(id):
    # Perform Operation
    record = User_Credentials.query.get(id)
    print(" in edit user records ",record)
    return render_template('edit_user_record.html', record=record)

@app.route('/delete_record/<int:id>', methods=['DELETE'])
@login_required
def delete_record(id):
    record = Profiles.query.get(id)

    if record:
        model_dict = {}
        for column in record.__table__.columns:
            attribute_name = column.key
            attribute_value = getattr(record, attribute_name)
            model_dict[attribute_name] = attribute_value

        db.session.delete(record)
        db.session.commit()

        # Optionally, return a JSON response to indicate success
        return jsonify({'message': 'Record deleted successfully', 'deleted_record': model_dict})
    else:
        # Return a JSON response for error
        return jsonify({'error': 'Record not found'}), 404
    
    
@app.route('/delete_user_record/<int:id>', methods=['DELETE'])
@login_required
def delete_user_record(id):
    record = User_Credentials.query.get(id)

    if record:
        model_dict = {}
        for column in record.__table__.columns:
            attribute_name = column.key
            attribute_value = getattr(record, attribute_name)
            model_dict[attribute_name] = attribute_value

        db.session.delete(record)
        db.session.commit()

        # Optionally, return a JSON response to indicate success
        return jsonify({'message': 'Record deleted successfully', 'deleted_record': model_dict})
    else:
        # Return a JSON response for error
        return jsonify({'error': 'Record not found'}), 404
        
@app.route('/home_content')
def home_content():
    return render_template("home_content.html")