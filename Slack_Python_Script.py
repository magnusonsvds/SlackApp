from slacker import Slacker
import datetime
import json
import mysql.connector

slackconnect = Slacker("xoxp-48585661490-48566956614-48609736293-3d77cbda11")

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

def getMessageInfo():
    messageLogInfo = []
    responseObject = slackconnect.channels.history("C1EGNU95L")
    responseDict = responseObject.body["messages"]
    #print (responseDict)

    for i in responseDict:
        message = i
        text = message["text"]
        user = message["user"]
        timestamp = message["ts"]
        messageInfo = [user,text,timestamp]
        messageLogInfo.append(messageInfo)
    return messageLogInfo

def pushData(messages):
    connection = mysql.connector.connect(user='scott', password='tiger', host='localhost', database='employees')



    

if __name__ == '__main__':
	#print (getUserInfo())
	#mes = getMessageInfo()
	#print (mes)
    #print (getUserInformation())

    print(getChannelInfo())
