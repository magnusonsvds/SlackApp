import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String, BigInteger, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
 
Base = declarative_base()

  
class Slackuser(Base):
    __tablename__ = 'slack_user'
    # define columns for the table person
    slack_user_id = Column(BigInteger, primary_key=True)
    username = Column(String(50))
    first_name = Column(String(50))
    last_name = Column(String(50))
 
class Messagechannel(Base):
    __tablename__ = 'message_channel'
    # Here we define columns for the table address.
    channel_id = Column(BigInteger, primary_key=True)
    channel_number = Column(String(50))
    channel_name = Column(String(50))


class Message(Base):
    __tablename__ = 'message'
    message_id = Column(BigInteger, primary_key=True)
    slack_user_id = Column(BigInteger, ForeignKey(Slackuser.slack_user_id))
    channel_id = Column(BigInteger, ForeignKey(Messagechannel.channel_id))
    date_time = Column(DateTime)
    msg = Column(String(2000))
    slack_user = relationship(Slackuser)
    message_channel = relationship(Messagechannel)
 
# Create an engine that stores data in the local directory's
# sqlalchemy_slack_entries.db file.
engine = create_engine('sqlite:///sqlalchemy_slack_entries.db')
 
# Create all tables in the engine. This is equivalent to "Create Table"
# statements in raw SQL.
Base.metadata.create_all(engine)