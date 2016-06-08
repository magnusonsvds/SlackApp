import os
import sys
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
# Update password for sql at ADDPASSWORDHERE in the line below
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:1Svds@123@localhost/slacktestdb'
db = SQLAlchemy(app)
  
class slack_user(db.Model):
    #include the line: __tablename__ = 'slack_user'  ????
    # define columns for the table person
    ID = db.Column(db.Integer, primary_key=True)
    slack_number = db.Column(db.String(50), unique=True)
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))

    def __init__(self, slack_number, first_name, last_name):
        self.slack_number = slack_number
        self.first_name = first_name
        self.last_name = last_name

    def __repr__(self):
        return '<slack_user %r>' % self.ID  


class message_channel(db.Model):
    # Here we define columns for the table address.
    ID = db.Column(db.Integer, db.Sequence('user_id_seq'), primary_key=True)
    channel_number = db.Column(db.String(50), unique=True)
    channel_name = db.Column(db.String(50))

    def __init__(self, channel_number, channel_name):
        self.channel_number = channel_number
        self.channel_name = channel_name

    def __repr__(self):
        return '<message_channel %r>' % self.ID


class message(db.Model):
    ID = db.Column(db.Integer, db.Sequence('user_id_seq'), primary_key=True)
    date_time = db.Column(db.DateTime)
    msg = db.Column(db.String(2000))
    slack_number = db.Column(db.String(50))
    channel_number = db.Column(db.String(50))

    def __init__(self, date_time, msg, slack_number, channel_number):
        if date_time is None:
            date_time = datetime.utcnow()
        self.date_time = date_time
        self.msg = msg
        self.slack_number = slack_number
        self.channel_number =  channel_number

    def __repr__(self):
        return '<message %r>' % self.ID
db.create_all()

# notes
#TRUE was changed from NONE in /Users/james/anaconda/lib/python3.5/site-packages/flask_sqlalchemy/__init__.py
