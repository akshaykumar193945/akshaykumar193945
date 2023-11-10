from flask import Flask, render_template, request, redirect, url_for, jsonify
from models import db, AdmissionRecord, User_Credentials
from flask_login import LoginManager, login_user, login_required, logout_user, current_user

import download_records as dwnld_rcds

app = Flask(__name__)
app.config.from_object('config')

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mydatabase.db'  # Replace with your database URL
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
        return jsonify({'authenticated': True})
    else:
        return jsonify({'authenticated': False})


@app.route('/')
def layout():
    return render_template('layout.html')

@login_manager.user_loader
def load_user(user_id):
    # Implement logic to load a user from your database or user storage
    # For example, if using a database, you can query the user by ID
    user = User_Credentials.query.get(int(user_id))
    return user

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Check if the username is already in use (you may use your database for this check)
        existing_user = User_Credentials.query.filter_by(username=username).first()

        if existing_user:
            return render_template('signup.html', error="Username is already taken.")

        # Create a new user (you need to implement this in your User model)
        new_user = User_Credentials(username=username, password=password)

        # print all records 
        records = User_Credentials.query.all()
        print(records)
        print('rrrrrrrrrrrrrrrrrrrrr ', username, password, new_user)
        # Add and commit the new user to your database
        db.session.add(new_user)
        db.session.commit()

        # Log in the new user after sign-up (optional)
        login_user(new_user)

        return redirect(url_for('login'))  # Redirect to a dashboard or home page

    return render_template('signup.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    # Check user credentials and log in the user
    logout_user()

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = User_Credentials.query.filter(User_Credentials.username == username).first()

        if user and username == user.username and password == user.password:
            login_user(user)
            return redirect(url_for('layout'))
        else:
            return render_template('signup.html')

    return render_template('login.html')

@app.route('/logout')
def logout():
    logout_user()
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

        admission_record = AdmissionRecord(name=name, email=email, dob=dob)

        db.session.add(admission_record)
        db.session.commit()
        admission_record = {
            'name': name,
            'email': email,
            'dob': dob
        }

        return render_template('admission_success.html', admission_record=admission_record)
    return render_template('error.html')

@app.route('/courses')
def courses():
    return render_template('courses.html')

@app.route('/admission_recordscourses')
@login_required
def admission_records():
    records = AdmissionRecord.query.all()
    print(records, "line no 42")
    return render_template('admission_records.html', records=records)

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
        records = AdmissionRecord.query.filter(AdmissionRecord.name == name).all()
        if len(records):
            return render_template('display_record.html', records=records)
        return render_template('error.html', records="Not Found")
    return render_template('error.html')

@app.route('/edit_record_by_id', methods=['POST'])
@login_required
def edit_record_by_id():
    if request.method == 'POST':
        record_id = request.form['record_id']
        record = AdmissionRecord.query.get(record_id)
        print(record)
    return render_template('edit_record.html', record=record)

@app.route('/record_edited/<int:id>', methods=['POST'])
@login_required
def record_edited(id):
    if request.method == 'POST':
        record = AdmissionRecord.query.get(id)
        if request.method == 'POST':
        # Update the record with the data from the form
            record.name = request.form['name']
            record.email = request.form['email']
            record.dob = request.form['dob']
            db.session.commit()  # Commit the changes to the database
            admission_record = {
                'name': request.form['name'],
                'email': request.form['email'],
                'dob': request.form['dob']
                }
            return render_template('admission_success.html', admission_record=admission_record)    

@app.route('/delete_record_by_id', methods=['POST'])
@login_required
def delete_record_by_id():
    if request.method == 'POST':
        record_id = request.form['record_id']
        record = AdmissionRecord.query.get(record_id)
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
    record = AdmissionRecord.query.get(id)
    print(record)
    return render_template('edit_record.html', record=record)

@app.route('/delete_record/<int:id>', methods=['DELETE'])
@login_required
def delete_record(id):
    record = AdmissionRecord.query.get(id)

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


if __name__ == '__main__':
    app.run(debug=True)