from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship
from database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String) 
    username = Column(String, unique=True, index=True)
    pin = Column(String)
    balance = Column(Float, default=0.0)

class Merchant(Base):
    __tablename__ = "merchants"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String)  
    handle = Column(String, unique=True, index=True)
    balance = Column(Float, default=0.0)

class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)
    sender_id = Column(Integer, ForeignKey("users.id"))
    receiver_id = Column(Integer, ForeignKey("merchants.id"))
    amount = Column(Float)
    status = Column(String)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())

    sender = relationship("User")
    receiver = relationship("Merchant")