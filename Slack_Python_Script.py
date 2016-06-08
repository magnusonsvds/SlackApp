from datetime import datetime
from slacker import Slacker
from slack_entries_database import db

from slack_entries_database import slack_user, message_channel, message

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:C2rimson@localhost/slacktestdb'
db = SQLAlchemy(app)

slackconnect = Slacker("xoxp-48585661490-48566956614-48985030439-bcbbfeeab3")


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
    for mess in messages:
        userId = mess[0]
        text = mess[1]
        date = datetimeChange(mess[2])
        channel = mess[3]

        new_message = message(userId, channel, date, text)
        db.session.add(new_message)
        

def datetimeChange(timestamp):
    return datetime.fromtimestamp(float(timestamp))

def Query():
    messages = message.query.all()
    #today = message.query.filter_by(text='#today').first()


if __name__ == '__main__':
    channels = getChannelInfo()
    messages = getMessageInfo("C1EGNU95L")
    users = getUserInformation()

    pushData(messages, users, channels)
    print (Query())
