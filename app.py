#!/usr/bin/env python
import random
import string
import hashlib
import settings
from utils import register_user, update_password, user_login, get_role, register_clients
from flask import Flask, render_template, request, session
from sqlalchemy import create_engine
from models import Base
from flask_mail import Mail


def create_app()->Flask:
     app = Flask(__name__)
     app.secret_key = settings.secret_key
     app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://{settings.dbuser}:{settings.dbpassword}@{settings.dbhost}/{settings.dbname}'
     app.config['MAIL_SERVER'] = 'mail.privateemail.com'
     app.config['MAIL_PORT'] = 465
     app.config['MAIL_USE_TLS'] = False
     app.config['MAIL_USE_SSL'] = True
     app.config['MAIL_USERNAME'] = 'accounts@schoolofprogramming.online'
     app.config['MAIL_PASSWORD'] = '!!!Newaccount24_Hack$'
     engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'], echo=True)
     Base.metadata.create_all(engine, checkfirst=True)
     return app

app = create_app()

mail = Mail(app)


@app.route('/')
def index():
     return render_template('register.html')

@app.route('/register', methods=['POST'])
def register():
     if request.method=='POST':
          result = request.form
          email = result['email']
          role = result['role']
          code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
          email = email.strip()
          if not email or not role:
               response = "Email and role are required"
               return render_template('response.html', response=response)
          register_user(create_engine(app.config['SQLALCHEMY_DATABASE_URI'], echo=True), email, role, code)
          response = "Registration successful! Check your email to activate your account"
          return render_template('response.html', response=response)


@app.route('/activate', methods=['GET'])
def activate():
     if request.method=='GET':
          code = request.args.get('code')
          return render_template('verify.html', code=code)
             

@app.route('/confirmed', methods=['POST'])
def confirmed():
     if request.method == 'POST':
          result = request.form
          password = result['password']
          cpassword = result['cpassword']
          code = result['code']
          if password != cpassword:
               response = "Passwords do not match"
               return render_template('response.html', response=response)
          update_password(create_engine(app.config['SQLALCHEMY_DATABASE_URI'], echo=True), code, password)
          response = "Activation Successful"
          return render_template('response.html', response=response)
     

@app.route('/login', methods=['POST', 'GET'])
def login():
     if request.method == 'POST':
          result = request.form
          email = result['email']
          password = result['password']
          if not email or not password:
               response = "Email and password are required"
               return render_template('response.html', response=response)
          email= email.strip()
          password = password.strip()
          if user_login(create_engine(app.config['SQLALCHEMY_DATABASE_URI'], echo=True), email, password):
               session['email'] = email
               if get_role(create_engine(app.config['SQLALCHEMY_DATABASE_URI'], echo=True), email) == 'ADMIN':
                    session['role'] = 'admin'
                    return render_template('admin/home.html', email=email, session=session)
               if get_role(create_engine(app.config['SQLALCHEMY_DATABASE_URI'], echo=True), email) == 'CLIENT':
                    session['role'] = 'client'
                    return render_template('client/home.html', email=email, session=session)
               if get_role(create_engine(app.config['SQLALCHEMY_DATABASE_URI'], echo=True), email) == 'CLINICAL':
                    session['role'] = 'clinical'
                    return render_template('clinical/home.html', email=email, session=session)
          else:
               response = "Unsuccessful Login"
               return render_template('response.html', response=response)
     return render_template('login.html')

@app.route('/logout', methods=['GET'])
def logout():
     session.pop('email', None)
     session.pop('role', None)
     return render_template('response.html', response="Logged out successfully")
     
@app.route('/clients', methods=['POST', 'GET'])
def clients():
     if request.method == 'GET':
          patient_num = 'abc123'
          first_name = 'John'
          middle_name = 'Doe'
          family_name = 'Smith'
          date_of_birth = '1990-01-01'
          street_address = '123 Main St'
          city = 'Anytown'
          state = 'CA'
          zip_code = '12345'
          phone_number = '123-456-7890'
          email = 'j.smith@test.com'
          emergency_contact_name = 'Jane Smith'
          emergency_contact_phone = '098-765-4321'
          emergency_contact_relation = 'Sister'
          emergency_contact_address = '456 Elm St'
          if register_clients(create_engine(app.config['SQLALCHEMY_DATABASE_URI'], echo=True), patient_num, first_name, middle_name, family_name,
                               date_of_birth, street_address, city, state, zip_code, phone_number, email,
                                 emergency_contact_name, emergency_contact_phone, emergency_contact_relation, 
                                 emergency_contact_address):
               response = "Client registered successfully"
               return render_template('response.html', response=response)
          else:
               response = "Client already exists"
               return render_template('response.html', response=response)

          #form_data = request.form
          #patient_num = form_data.get('patient_num')