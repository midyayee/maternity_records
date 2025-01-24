#!/usr/bin/env python
import hashlib
import settings
from flask_mail import Mail, Message
from sqlalchemy import insert
from models import tables

mail = Mail()


def insert_data(engine, table, **kwargs):
    with engine.connect() as connection:
        connection.execute(insert(table.__table__).values(**kwargs).prefix_with('IGNORE'))
        connection.commit()

def send_mail(email:str, sender:str, subject:str, body:str)->bool:
    msg = Message(subject = subject,
                  sender = sender,
                  recipients = [email])
    msg.body = body      
    mail.send(msg)
    return True

def register_user(engine, email:str, role:str, code:str)->bool:
    hash = email + settings.secret_key
    hash = hashlib.sha256(hash.encode())
    enc_email = hash.hexdigest()
    with engine.connect() as conn:
        result  = conn.execute(tables.User.__table__.select().where(tables.User.__table__.c.email == enc_email))
        conn.commit()
        if result.rowcount > 0:
            return False
        else:
            insert_data(engine, table=tables.User, email=enc_email, role=role, code=code)
            send_mail(email=email, sender ="accounts@schoolofprogramming.online",
                    subject="Activate your account",
                    body=f"Click on this link to activate your account: http://{settings.dbhost}/activate?email={email}&code={code}")
            return True

def update_password(engine, code, user_password):
    passwordhash = user_password + settings.secret_key
    passwordhash = hashlib.sha256(passwordhash.encode())
    password = passwordhash.hexdigest()
    with engine.connect() as conn:
        conn.execute(tables.User.__table__.update().where(tables.User.__table__.c.code == code).values(password=password, activated=True))
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
        result = conn.execute(tables.User.__table__.select().where(tables.User.__table__.c.email == enc_email).where(tables.User.__table__.c.password == enc_password))
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
        result = conn.execute(tables.User.__table__.select().where(tables.User.__table__.c.email == enc_email))
        #commit the transaction
        conn.commit()
        if result.rowcount > 0:
            for row in result:
                return row[3]
        return False

def register_clients(engine, patient_num:str, first_name :str, middle_name:str, 
                     family_name:str, date_of_birth:str, street_address:str, city:str,
                     state:str, zip_code:str, phone_number:str, email:str, emergency_contact_name:str,
                     emergency_contact_phone:str, emergency_contact_relation:str, emergency_contact_address:str
                     ):
    with engine.connect() as conn:
        result = conn.execute(tables.Clients.__table__.select().where(tables.Clients.__table__.c.patient_num == patient_num))
        conn.commit()
        if result.rowcount > 0:
            return False
        else:
            insert_data(engine, table=tables.Clients, patient_num=patient_num, first_name=first_name,
                         middle_name=middle_name, family_name=family_name, date_of_birth=date_of_birth,
                         street_address=street_address, city=city, state=state, zip_code=zip_code,
                         phone_number=phone_number, email=email, emergency_contact_name=emergency_contact_name,
                         emergency_contact_phone=emergency_contact_phone, emergency_contact_relation=emergency_contact_relation,
                         emergency_contact_address=emergency_contact_address)
            return True
