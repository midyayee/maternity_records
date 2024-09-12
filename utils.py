import hashlib
import settings
from flask_mail import Mail, Message
from sqlalchemy import insert
from models import users

mail = Mail()


def insert_data(engine, table, **kwargs):
    with engine.connect() as connection:
        connection.execute(insert(table.__table__).values(**kwargs).prefix_with('IGNORE'))
        connection.commit()

def send_mail(email, sender, subject, body):
    msg = Message(subject = subject,
                  sender = sender,
                  recipients = [email])
    msg.body = body      
    mail.send(msg)
    return True

def register_user(engine, email, role, code):
    hash = email + settings.secret_key
    hash = hashlib.sha256(hash.encode())
    enc_email = hash.hexdigest()
    with engine.connect() as conn:
        result  = conn.execute(users.User.__table__.select().where(users.User.__table__.c.email == enc_email))
        conn.commit()
        if result.rowcount > 0:
            return False
        else:
            insert_data(engine, table=users.User, email=enc_email, role=role, code=code)
            send_mail(email=email, sender ="accounts@schoolofprogramming.online",
                    subject="Activate your account",
                    body=f"Click on this link to activate your account: http://{settings.dbhost}:8080/activate?email={email}&code={code}")
            return True

def update_password(engine, code, user_password):
    passwordhash = user_password + settings.secret_key
    passwordhash = hashlib.sha256(passwordhash.encode())
    password = passwordhash.hexdigest()
    with engine.connect() as conn:
        conn.execute(users.User.__table__.update().where(users.User.__table__.c.code == code).values(password=password, activated=True))
        conn.commit()
        return True

def user_login(engine, email, password):
    hash = email + settings.secret_key
    hash = hashlib.sha256(hash.encode())
    enc_email = hash.hexdigest()
    passwordhash = password + settings.secret_key
    passwordhash = hashlib.sha256(passwordhash.encode())
    enc_password = passwordhash.hexdigest()
    with engine.connect() as conn:
        #return row where email and password match
        result = conn.execute(users.User.__table__.select().where(users.User.__table__.c.email == enc_email).where(users.User.__table__.c.password == enc_password))
        if result.rowcount > 0:
            for row in result:
                if row[5] == 1:
                    return True
                else:
                    return "Account is not Activated"
        return False
    

def get_role(engine, email):
    hash = email + settings.secret_key
    hash = hashlib.sha256(hash.encode())
    enc_email = hash.hexdigest()
    with engine.connect() as conn:
        result = conn.execute(users.User.__table__.select().where(users.User.__table__.c.email == enc_email))
        #commit the transaction
        conn.commit()
        if result.rowcount > 0:
            for row in result:
                return row[3]
        return False

