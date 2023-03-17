

import os
from flask import Flask, render_template, request, url_for, redirect, request
from flask_sqlalchemy import SQLAlchemy


from sqlalchemy.sql import func


basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] =\
        'sqlite:///' + os.path.join(basedir, 'database.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)



class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    university = db.Column(db.String(80), nullable=False)
    gender = db.Column(db.String(80), nullable=False )
    age = db.Column(db.Integer, nullable=False)
    education = db.Column(db.String(80), nullable=False)
    city = db.Column(db.String(80),nullable=False)
    created_at = db.Column(db.DateTime(timezone=True),
                           server_default=func.now())
    vaccine = db.Column(db.String(30))
    status = db.Column(db.String(30))
    vaccines = db.relationship('Vaccines', backref='student', lazy=True,uselist=False)
    illness = db.relationship('Illness',backref = 'student', lazy=True,uselist=False)
    knowledge = db.relationship('Knowledge', backref = 'student', lazy= True,uselist=False)

    def __repr__(self):
        return f'<Student {self.id}>'

class Vaccines(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    vaccine_type = db.Column(db.String(30), nullable=True)
    vaccine_number = db.Column(db.Integer, nullable=True)
    nop = db.Column(db.String(120), nullable=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'),
        nullable=False)

    def __repr__(self):
        return f'<Vaccines {self.vaccine}>'


class Illness (db.Model):
    id = db.Column(db.Integer, primary_key=True)
    disease = db.Column(db.String(20))
    time = db.Column(db.String(20), nullable=True)
    mileage = db.Column(db.String(20), nullable=True)
    mileage2 = db.Column(db.String(20), nullable=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'),
        nullable=False)

    def __repr__(self):
        return f'<Illness {self.disease}>'




class Knowledge(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    knowledge1 = db.Column(db.String(40))
    knowledge2 = db.Column(db.String(40))
    knowledge3 = db.Column(db.String(40))
    knowledge4 = db.Column(db.String(40))
    knowledge5 = db.Column(db.String(40))
    knowledge6 = db.Column(db.String(40))
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'),
        nullable=False)

    def __repr__(self):
        return f'<Knowledge {self.knowledge1}>'



@app.route('/', methods=('GET', 'POST'))
def create():
    if request.method == 'POST':
        university = request.form['university']
        gender = request.form['gender']
        age = request.form['age']
        education = request.form['education']
        city = request.form['city']
        vaccine = request.form['vaccine']
        status = request.form['status']
        student = Student(vaccine = vaccine,
                          university=university,
                          gender=gender,
                          age=age,
                          education=education,
                          city=city,
                          status=status
                          )
        db.session.add(student)
        db.session.commit()
        if vaccine == "yes":
            return redirect(url_for('vaccines',liczba = student.id, **request.args))
        else:
            return redirect(url_for('illnes1',liczba = student.id, **request.args))
    return render_template('create.html')

@app.route('/results/')
def index():
    students = Student.query.all()
    vaccine = Vaccines.query.all()
    return render_template('index.html', students=students, vaccine=vaccine)

@app.route('/about/')
def about():
    return render_template('about.html')

@app.route('/vaccines/', methods=('GET', 'POST'))
def vaccines():
    recommend_this_to_string = ''
    liczba = request.args['liczba']
    if request.method == 'POST':
        vaccine_type = request.form['vaccine2']
        vaccine_number = int(request.form['number'])
        nop = request.form.getlist('NOP')
        for val in nop:
                recommend_this_to_string += val + ','
        vaccines = Vaccines(
                            vaccine_type = vaccine_type,
                            vaccine_number = vaccine_number,
                            nop = recommend_this_to_string,
                            student_id = liczba)
        db.session.add(vaccines)
        db.session.commit()
        return redirect(url_for('illnes', **request.args ))
    return render_template('Szczepienia.html')


@app.route('/illnes1/', methods=('GET', 'POST'))
def illnes1():
    liczba = request.args['liczba']
    if request.method == 'POST':
        disease = request.form['disease']
        mileage = request.form['mileage']
        illness = Illness(
                            disease = disease,
                            mileage = mileage,
                            student_id = liczba)
        db.session.add(illness)
        db.session.commit()
        return redirect(url_for('knowledge', **request.args))
    return render_template('Zachorowanie.html')

@app.route('/illnes/', methods=('GET', 'POST'))
def illnes():
    liczba = request.args['liczba']
    if request.method == 'POST':
        disease = request.form['disease']
        time = request.form['time']
        mileage = request.form['mileage']
        mileage2 = request.form['mileage2']
        illness = Illness(
                            disease = disease,
                            time = time,
                            mileage = mileage,
                            mileage2 =mileage2,
                            student_id = liczba)
        db.session.add(illness)
        db.session.commit()
        return redirect(url_for('knowledge', **request.args))
    return render_template('Zachorowanie1.html')


@app.route('/knowledge/', methods=('GET', 'POST'))
def knowledge():
    liczba = request.args['liczba']
    if request.method == 'POST':
        knowledge1 = request.form['type']
        knowledge2 = request.form['modify']
        knowledge3 = request.form['auto']
        knowledge4 = request.form['allergy']
        knowledge5 = request.form['safe']
        knowledge6 = request.form['safe1']
        knowledge = Knowledge(
                            knowledge1=knowledge1,
                          knowledge2=knowledge2,
                          knowledge3=knowledge3,
                          knowledge4=knowledge4,
                          knowledge5=knowledge5,
                          knowledge6=knowledge6,
                          student_id = liczba)
        db.session.add(knowledge)
        db.session.commit()
        return redirect(url_for('end'  ))
    return render_template('Wiedza.html')

@app.route('/end/')
def end():
    return render_template('Koniec.html')
