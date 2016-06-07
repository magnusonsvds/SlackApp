import os
import sys
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
# add password to server at ADDPASSWORDHERE in line below (line 8)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:ADDPASSWORDHERE@localhost/mydatabase'
db = SQLAlchemy(app)
  
class slack_user(db.Model):
	#include the line: __tablename__ = 'slack_user'  ????
    # define columns for the table person
    slack_user_id = db.Column(db.BigInteger, primary_key=True)
    username = db.Column(db.String(50))
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))

    def __init__(self, slack_user_id, username, first_name, last_name):
    	self.slack_user_id = slack_user_id
    	self.username = username
    	self.first_name = first_name
    	self.last_name = last_name

    def __repr__(self):
    	return '<slack_user %r>' % self.slack_user_id	


class message_channel(db.Model):
    # Here we define columns for the table address.
    channel_id = db.Column(db.BigInteger, primary_key=True)
    channel_number = db.Column(db.String(50))
    channel_name = db.Column(db.String(50))

    def __init__(self, channel_id, channel_number, channel_name):
    	self.channel_id = channel_id
    	self.channel_number = channel_number
    	self.channel_name = channel_name

    def __repr__(self):
    	return '<message_channel %r>' % self.channel_id


class message(db.Model):
    message_id = db.Column(db.BigInteger, primary_key=True)
    slack_user_id = db.Column(db.BigInteger, db.ForeignKey(slack_user.slack_user_id))
    channel_id = db.Column(db.BigInteger, db.ForeignKey(message_channel.channel_id))
    date_time = db.Column(db.DateTime)
    msg = db.Column(db.String(2000))
    slack_user = db.relationship(slack_user)
    message_channel = db.relationship(message_channel)

    def __init__(self, message_id, slack_user_id, channel_id, date_time, msg):
    	self.message_id = message_id
    	self.slack_user_id = slack_user_id
    	self.channel_id = channel_id
    	if date_time is None:
    			date_time = datetime.utcnow()
    	self.date_time = date_time
    	self.msg = msg

    def __repr__(self):
    	return '<message %r>' % self.message_id


''' notes
True was changed from None in /Users/james/anaconda/lib/python3.5/site-packages/flask_sqlalchemy/__init__.py
'''
