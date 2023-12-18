from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, jsonify, session
from models import db, User_Credentials, Course_DB
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from flask_migrate import Migrate
from flask import request, jsonify
import traceback
import download_records as dwnld_rcds

app = Flask(__name__)
app.config.from_object('config')

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mydatabase.db'  # Replace with your database URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
migrate = Migrate(app, db)

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
            return jsonify({'status': False, 'message': 'Username is already taken'})

        # Create a new user
        new_user = User_Credentials(username=username, password=password, first_name=first_name, last_name=last_name, email=email, mobile_number=mobile_number)

        # Add and commit the new user to your database
        db.session.add(new_user)
        db.session.commit()

        # Log in the new user after sign-up (optional)
        login_user(new_user)
        # return redirect(url_for('home_content'))
        return jsonify({'status' : True, 'message': 'User registered successfully', 'redirect': '/target_page'})

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

@app.route('/forgot_password')
def forgot_password():
    return render_template('forgot_password.html')

@app.route('/update_user_record/<int:id>', methods=['GET', 'POST'])
@login_required
def update_user_record(id):
    record = User_Credentials.query.get(id)
    print(" in edit user records ",record)
    return render_template('edit_user_record.html', record=record)

@app.route('/update_password_1/<string:username>', methods=['GET', 'POST'])
def update_password_1(username):
    record = User_Credentials.query.filter_by(username=username).first()
    print(" in edit user records update 2 ", record)
    return render_template('update_password_1.html', record=record)

@app.route('/password_updated/<string:username>', methods=['POST', 'GET'])
def password_updated(username):
    print("ininininininininininin")
    try:
        if request.method == 'POST':
            print("In password updator user edited ::::: ", request.data)

            data = request.get_json()  # Use request.json to parse JSON data
            print("In password updator user edited :", data)

            new_password = data.get('new_password')
            print("new passwaord : ", new_password)
            record = User_Credentials.query.filter_by(username=username).first()
            if record:
                record.password = new_password
                db.session.commit()

                user_password = {
                    'password': record.password
                }

                print("Password Updation Done !!!")
                return jsonify({'status':'success', 'message': 'Password updated successfully', 'user_password': user_password})
            else:
                return jsonify({'error': 'Record not found'}), 404
    except Exception as e:
        print(f"Error: {str(e)}")
        traceback.print_exc()
        return jsonify({'error': 'Internal Server Error'}), 500

@app.route('/')
def layout():
    username = session.get('username', None)
    print(username)
    return render_template('layout.html', username=username)

@app.route('/user_records')
@login_required
def user_records():
    records = User_Credentials.query.all()
    print(records, "line no 42")
    return render_template('User_Credentials.html', records=records)

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
        # delete_user_order

@app.route('/courses')
def courses():
    return render_template('courses.html')

@app.route('/show_enrolled_course', methods=['GET'])
def show_enrolled_course():
    records = Course_DB.query.all()
    print(records, "line no 186")
    return render_template('Course_Enrolled.html', records=records)

@app.route('/enroll_Course', methods=['POST'])
@login_required
def enroll_Course():
    # username = current_user.username
    # existing_user = User_Credentials.query.filter_by(username=current_user.username).first()
    # username = Course_DB.query.filter_by(username=current_user.user_id).first()
    print("vbvbvbvbvbvbvbvbvbvb")
    if request.method == 'POST':
        data = request.get_json()
       
        course = data.get('course_name')
        course_id = data.get('course_id')
        
        existing_enroll = Course_DB.query.filter_by(course=course, user_id=current_user.username).first()
        
        if existing_enroll:
            return jsonify({'status' : False, 'message': 'Already Enrolled', 'redirect': '/target_page'})
        
        current_datetime = datetime.now()
        formatted_date = current_datetime.strftime("%Y-%m-%d %H:%M:%S")
        enroll_datetime = datetime.strptime(formatted_date, "%Y-%m-%d %H:%M:%S")

        new_enroll = Course_DB(course_id=course_id, course=course, user_id=current_user.username, enroll_date=enroll_datetime)

        # Add and commit the new user to your database
        db.session.add(new_enroll)
        db.session.commit()
        return jsonify({'status' : True, 'message': 'User enrolled successfully', 'redirect': '/target_page'})
        
    return render_template('courses.html')

@app.route('/submit_edit_order/<int:id>', methods=['POST'])
@login_required
def submit_edit_order(id):
    try:
        print("zzzzzzzzzzzzzzzzzzzzzzzz")
        if request.method == 'POST':
            data = request.get_json(force=True)  # Use request.json to parse JSON data
            print("In order edit :", data)

            course = data.get('course')
            course_id = data.get('course_id')

            record = Course_DB.query.get(id)
            if record:
                record.course_id = course_id
                record.course = course 

                db.session.commit()

                user_order = {
                    'course_id': record.course_id,
                    'course': record.course,
                }

                print("Order Updation Done !!!")
                return jsonify({'message': 'Record updated successfully', 'user_order': user_order})
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
    # user_orders = Course_DB.query.filter_by(user_id=current_user.username).first()
    user_orders = Course_DB.query.filter_by(user_id=current_user.username).all()
    # enrolled_cources = Course_DB.query.filter_by(user_id=current_user.username)
    return render_template('user_profiles.html', existing_user=existing_user, user_orders=user_orders)

@app.route('/process_form', methods=['POST'])
@login_required
def process_form():
    dwnld_rcds.download_records()        
    return redirect(url_for('user_records'))

@app.route('/edit_user_order/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_user_order(id):
    record = Course_DB.query.get(id)
    print(" in edit user records ",record)
    return render_template('edit_user_order.html', record=record)

@app.route('/delete_user_order/<int:id>', methods=['DELETE'])
@login_required
def delete_user_order(id):
    record = Course_DB.query.get(id)

    if record:
        model_dict = {}
        for column in record.__table__.columns:
            attribute_name = column.key
            attribute_value = getattr(record, attribute_name)
            model_dict[attribute_name] = attribute_value

        db.session.delete(record)
        db.session.commit()

        # Optionally, return a JSON response to indicate success
        return jsonify({'message': 'Order deleted successfully', 'deleted_record': model_dict})
    else:
        # Return a JSON response for error
        return jsonify({'error': 'Record not found'}), 404

@app.route('/home_content')
def home_content():
    return render_template("home_content.html")

@app.route('/service')
def service():
    return render_template('service.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')