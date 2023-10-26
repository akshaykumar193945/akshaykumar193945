from flask import Flask, render_template, request, redirect, url_for, flash
from models import db, AdmissionRecord

import download_records as dwnld_rcds

app = Flask(__name__)
app.config.from_object('config')

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mydatabase.db'  # Replace with your database URL
db.init_app(app)
with app.app_context():
    db.create_all()

@app.route('/')
def layout():
    return render_template('layout.html')

@app.route('/admission_form')
def admission_form():
    return render_template('admission_form.html')

@app.route('/admit', methods=['POST'])
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

@app.route('/admission_records')
def admission_records():
    records = AdmissionRecord.query.all()
    print(records, "line no 42")
    return render_template('admission_records.html', records=records)

@app.route('/find')
def find():
    print("Line no 48")
    return render_template('find.html')

@app.route('/display_record', methods=['POST'])
def display_record():
    if request.method == 'POST':
        name = request.form['name']
        records = AdmissionRecord.query.filter(AdmissionRecord.name == name).all()
        if len(records):
            return render_template('display_record.html', records=records)
        return render_template('error.html', records="Not Found")
    return render_template('error.html')

@app.route('/edit_record_by_id', methods=['POST'])
def edit_record_by_id():
    if request.method == 'POST':
        record_id = request.form['record_id']
        print("2222222222222222222222", record_id)
        record = AdmissionRecord.query.get(record_id)
        print(record)
    return render_template('edit_record.html', record=record)

@app.route('/record_edited/<int:id>', methods=['POST'])
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

if __name__ == '__main__':
    app.run(debug=True)