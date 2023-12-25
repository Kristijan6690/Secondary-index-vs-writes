from sqlalchemy.orm import sessionmaker
from sqlalchemy import Index, inspect
from main import engine, Passanger, sec_indx_passanger
from faker import Faker
import pandas as pd

#Funkcija za ubacivanje podataka u bazu
def insert_data(db,data):
    for index, row in data.iterrows(): 
        person = db(Survived=row.Survived, Pclass=row.Pclass, Name=row.Name, Sex=row.Sex, Age=row.Age, 
                    SibSp=row.SibSp, Parch=row.Parch, Ticket=row.Ticket, Fare=row.Fare, Cabin=row.Cabin, Embarked=row.Embarked)
        session.add(person)

    print("Data inserted into Database")

Session = sessionmaker(bind = engine) #kreiranje sesije koja govori gdje da se sve naredbe odrađuju
session = Session() # varijabla koja vraća sesijski objekt za odrađivanje naredba 

fake = Faker() # objekt za generiranje radnom podataka

#Block za pripremu i generiranje podataka
df = pd.read_csv('titanic.csv')
df = df.drop(['PassengerId'], axis=1)
for _ in range(5000):
    passanger = {
        'Survived': fake.random_element(elements = (0, 1)),
        'Pclass': fake.random_element(elements = (0, 1, 3)),
        'Name': fake.name(),
        'Sex': fake.random_element(elements = ('male', 'female')),
        'Age': fake.random_element(elements = (20,30,40,50,60,70)),
        'SibSp': fake.random_element(elements = (0, 1, 3)),
        'Parch': fake.random_element(elements = (0, 1)),
        'Ticket': fake.random_element(elements = (347742, 243456, 123058, 389291)),
        'Fare': fake.random_element(elements = (8.0291, 7.0293, 5,502, 9,502)),
        'Cabin': fake.random_element(elements = ('C86', 'D35', 'A55')),
        'Embarked': fake.random_element(elements = ('C', 'S', 'Q'))
    }

    df = df._append(passanger, ignore_index=True)
    
try:
    #Ubacivanje podataka u bazu
    insert_data(Passanger, df)
    insert_data(sec_indx_passanger, df)
    
    #Provjera ako već postoje i stvaranje secondary indexa na column Sex i Pclass
    inspector = inspect(engine)

    if inspector.has_index('sec_indx_passangers','idx_Sex') or inspector.has_index('sec_indx_passangers','idx_Pclass'):
        session.commit()
    else:
        sex_index = Index('idx_Sex', sec_indx_passanger.Sex)
        pclass_index = Index('idx_Pclass', sec_indx_passanger.Pclass)
        sex_index.create(engine)
        pclass_index.create(engine)
        print("Secondary Indexes created")
        session.commit()
    
except:
    session.rollback()
    print("Error")
    
finally:
    session.close()
    print("Session closed")