from datetime import datetime
from slacker import Slacker
from slack_entries_database import db

from slack_entries_database import slack_user, message_channel, message

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:1Svds@123@localhost/slacktestdb'
db = SQLAlchemy(app)

slackconnect = Slacker("xoxp-48585661490-48566956614-49183403814-0bd90fc171")


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

def insertData(messages, users, channels):
    sendMessagesToDatabase(messages)
    sendChannelsToDatabase(channels) 
    sendUsersToDatabase(users)
    db.session.commit()  


def pushData(messages, users, channels):

    userQuery = slack_user.query.all()
    if (len(userQuery) > len(users)):
        # Insert messages in the message table
        sendMessagesToDatabase(messages)

    channelQuery = message_channel.query.all()
    if (len(channelQuery) > len(channels)):
        # Insert channels in the channel table
        sendChannelsToDatabase(channels) 

    #Inser users in the the user table
    sendUsersToDatabase(users)   
    
    db.session.commit()     

def sendChannelsToDatabase(channels):
    for channel in channels:
        channelNum = channel[0]
        channelName = channel[1]

        new_channel = message_channel(channelNum, channelName)
        db.session.add(new_channel)


def sendUsersToDatabase(users):
    for user in users:
        userNum = user[0]
        userFirst = user[1]
        userLast = user[2]

        new_user = slack_user(userNum, userFirst, userLast)
        db.session.add(new_user)


def sendMessagesToDatabase(messages):
    for mess in messages:
        userNum = mess[0]
        text = mess[1]
        date = datetimeChange(mess[2])
        channelNum = mess[3]

        new_message = message(date, text, userNum, channelNum)
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
    insertData(messages, users, channels)
    pushData(messages, users, channels)