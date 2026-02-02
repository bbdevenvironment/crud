from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)


raw_db_url = os.getenv('DATABASE_URL')

if not raw_db_url:
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///contacts.db'
else:
    if raw_db_url.startswith("postgres://"):
        raw_db_url = raw_db_url.replace("postgres://", "postgresql://", 1)
    app.config['SQLALCHEMY_DATABASE_URI'] = raw_db_url

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Person(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    email = db.Column(db.String(50))
    phone = db.Column(db.String(20))

with app.app_context():
    db.create_all()

@app.route('/')
def home():
    all_people = Person.query.all()
    return render_template('index.html', people=all_people)


@app.route('/add', methods=['POST'])
def add_contact():
    u_name = request.form.get('u_name')
    u_email = request.form.get('u_email')
    u_phone = request.form.get('u_phone')

 
    if u_name and u_email:
        new_person = Person(name=u_name, email=u_email, phone=u_phone)
        db.session.add(new_person)
        db.session.commit()
    
    return redirect('/')


@app.route('/update/<int:id>', methods=['POST'])
def update_contact(id):
    person_to_update = Person.query.get(id)
    
    if person_to_update:
        person_to_update.name = request.form.get('u_name')
        person_to_update.email = request.form.get('u_email')
        person_to_update.phone = request.form.get('u_phone')
        
        db.session.commit()
        
    return redirect('/')


@app.route('/clear', methods=['POST'])
def clear_data():
    db.session.query(Person).delete()
    db.session.commit()
    return redirect('/')


if __name__ == "__main__":
    app.run(debug=True)