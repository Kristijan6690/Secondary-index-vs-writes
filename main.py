from sqlalchemy import Column, Integer, String, Float, create_engine 
from sqlalchemy.orm import declarative_base

db_url= "sqlite:///database.db" # relativ path za db, kreira se u folderu

engine = create_engine(db_url) # engine za kreiranje db

baza = declarative_base() # objekt za kreiranje modula

#Kreiranje baza

class Passanger(baza):
    __tablename__ = "passangers"
    PassengerId = Column(Integer, primary_key = True)
    Survived = Column(Integer)
    Pclass = Column(Integer)
    Name = Column(String)
    Sex = Column(String)
    Age = Column(Float)
    SibSp = Column(Integer)
    Parch = Column(Integer)
    Ticket = Column(String)
    Fare = Column(Float)
    Cabin = Column(String)
    Embarked = Column(String)

class sec_indx_passanger(baza):

    __tablename__ = "sec_indx_passangers"
    PassengerId = Column(Integer, primary_key = True)
    Survived = Column(Integer)
    Pclass = Column(Integer)
    Name = Column(String)
    Sex = Column(String)
    Age = Column(Float)
    SibSp = Column(Integer)
    Parch = Column(Integer)
    Ticket = Column(String)
    Fare = Column(Float)
    Cabin = Column(String)
    Embarked = Column(String)

baza.metadata.create_all(engine) # funkcija za kreiranje baze/tablica odnosno engina
