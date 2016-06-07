import datetime
from slacker import Slacker
from slack_entries_database import db

from slack_entries_database import slack_user, message_channel, message

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/db'
db = SQLAlchemy(app)

slackconnect = Slacker("xoxp-48585661490-48566956614-48957258242-7cc1bd3785")


def getUserInformation():
    userInfo = []
    responseObject = slackconnect.users.list()
    responseMemberList = responseObject.body["members"]
    for member in responseMemberList:
        idCode = member["id"]
        profile = member["profile"]
        firstName = profile["first_name"]
        LastName = profile["last_name"]
        memberInfo = [idCode, firstName, LastName]
        userInfo.append(memberInfo)
    return userInfo

def getChannelInfo():
    channelInfo = []
    responseObject = slackconnect.channels.list()
    responseChannelList = responseObject.body["channels"]
    for channel in responseChannelList:
        channelId = channel["id"]
        channelName = channel["name"]
        chanInfo = [channelId, channelName]
        channelInfo.append(chanInfo)
    return channelInfo

def getMessageInfo(channel):
    messageLogInfo = []
    responseObject = slackconnect.channels.history(channel)
    responseDict = responseObject.body["messages"]
    #print (responseDict)

    for i in responseDict:
        message = i
        text = message["text"]
        user = message["user"]
        timestamp = message["ts"]
        messageInfo = [user,text,timestamp,channel]
        messageLogInfo.append(messageInfo)
    return messageLogInfo

def pushData(messages, users, channels):
    db.create_all()

    # Insert messages in the message table
    sendMessagesToDatabase(messages)
    # Insert channels in the channel table
    sendChannelsToDatabase(channels) 
    #Inser users in the the user table
    sendUsersToDatabase(users)   
    
    db.session.commit()     

def sendChannelsToDatabase(channels):
    for channel in channels:
        channelId = channel[0]
        channelName = channel[1]

        new_channel = message_channel(channelId, channelName)
        db.session.add(new_channel)


def sendUsersToDatabase(users):
    for user in users:
        userId = user[0]
        userFirst = user[1]
        userLast = user[2]

        new_user = slack_user(userId, userFirst, userLast)
        db.session.add(new_user)


def sendMessagesToDatabase(messages):
    for message in messages:
        userId = message[0]
        text = message[1]
        datetime = datetime(message[2])
        channel = message[3]
        counter +=1
        new_message = message(userId, channel, datetime,  text)
        db.session.add(new_message)
        

def datetime(timestamp):
    datetime.datetime.fromtimestamp(int(timestamp)).strftime('%Y-%m-%d %H:%M:%S')

def Query():
    messages = message.query.all()
    #today = message.query.filter_by(text='#today').first()


if __name__ == '__main__':
    channels = getChannelInfo()
    messages = getMessageInfo("C1EGNU95L")
    users = getUserInformation()

    print (Query())
