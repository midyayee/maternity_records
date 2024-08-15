from flask import Flask, render_template, request
from sqlalchemy import create_engine
import settings
from models import Base, users
from utils import insert_data
from flask_simple_crypt import SimpleCrypt

def create_app()->Flask:
     app = Flask(__name__)
     app.secret_key = settings.secret_key
     app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://{settings.dbuser}:@{settings.dbhost}/{settings.dbname}'
     engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'], echo=True)
     Base.metadata.create_all(engine, checkfirst=True)
     return app

app = create_app()
cipher = SimpleCrypt()
cipher.init_app(app)


@app.route('/')
def index():
     return render_template('register.html')

@app.route('/register', methods=['POST'])
def register():
     if request.method=='POST':
          result = request.form
          email = result['email']
          role = result['role']
          enc_email = cipher.encrypt(email)
          insert_data(create_engine(app.config['SQLALCHEMY_DATABASE_URI'], echo=True), table=users.User,email=enc_email, password="", role=role)
          return render_template('response.html', result=result)
     
if __name__ == '__main__':
     app.run(port =8080, debug=True)