import datetime
from slacker import Slacker
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from slack_entries_database import Slackuser, Messagechannel, Message, Base

#from sqlalchemy_declarative import Address, Base, Person

slackconnect = Slacker("")

#def getAllChannels():
    #channels = slackconnect.
   # return users
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
    engine = create_engine('sqlite:///sqlalchemy_example.db')
    Base.metadata.bind = engine
    DBSession = sessionmaker(bind=engine)
    session = DBSession()

    # Insert messages in the message table
    sendMessagesToDatabase(messages, session)
    # Insert channels in the channel table
    sendChannelsToDatabase(channels, session) 
    #Inser users in the the user table
    sendUsersToDatabase(users, session)   
     

def sendChannelsToDatabase(channels, session):
    counter =0
    for channel in channels:
        channelId = channel[0]
        channelName = channel[1]
        counter += 1

        new_channel = Messagechannel(channel_id = counter, channel_number = channelId, channel_name = channelName)
        session.add(new_channel)
        session.commit()


def sendUsersToDatabase(users, session):
    counter = 0
    for user in users:
        userId = user[0]
        userFirst = user[1]
        userLast = user[2]
        counter +=1

        new_user = Slackuser(slack_user_id = counter, username = userId, first_name = userFirst, last_name = userLast)
        session.add(new_user)
        session.commit()


def sendMessagesToDatabase(messages, session):
    counter = 0
    for message in messages:
        userId = message[0]
        text = message[1]
        datetime = datetime(message[2])
        channel = message[3]
        counter +=1
        oneMessage = Message(message_id = counter, slack_user_id = userId, channel_id = channel, date_time = datetime, message = text)
        session.add(oneMessage)
        session.commit()

def datetime(timestamp):
    datetime.datetime.fromtimestamp(int(timestamp)).strftime('%Y-%m-%d %H:%M:%S')


if __name__ == '__main__':
    channels = getChannelInfo()
    messages = getMessageInfo("C1EGNU95L")
    users = getUserInformation()
