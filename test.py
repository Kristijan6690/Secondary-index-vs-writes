import time
from sqlalchemy.orm import sessionmaker
from main import engine, Passanger, sec_indx_passanger
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

#funkcija za mjenje vremena za jedan insert
def measure_single(db):
    start = time.perf_counter_ns()

    new_user = db(Survived=0, Pclass=2, Name='Kristijan', Sex='Male', Age=25, 
                        SibSp=0, Parch=0, Ticket=11111, Fare=22222, Cabin='B25', Embarked='Q')
    
    session.add(new_user)
    session.commit()

    end = time.perf_counter_ns()
    return print(f"Time taken to write data to {db.__tablename__} table:", end - start, "ns")

#funkcija za mjerenje vremena za više inserta
def measure_multiple(db,data):
    start = time.perf_counter_ns()

    for index, row in data.iterrows(): 
        new_user = db(Survived=row.Survived, Pclass=row.Pclass, Name=row.Name, Sex=row.Sex, Age=row.Age, 
                    SibSp=row.SibSp, Parch=row.Parch, Ticket=row.Ticket, Fare=row.Fare, Cabin=row.Cabin, Embarked=row.Embarked)
        
        session.add(new_user)
        session.commit()

    end = time.perf_counter_ns()
    return print(f"Time taken to write multiple data to {db.__tablename__} table:", end - start, "ns")

#funkcija za kreiranje line chart
def line_chart(without_idx, with_idx,i):
    plt.plot(i, without_idx, marker='o', linestyle='-', label='Without Secondary Index')
    plt.plot(i, with_idx, marker='o', linestyle='-', label='With Secondary Index')
    plt.ylabel('Time taken (ns)')
    plt.xlabel('Iterations')
    plt.title('Comparison of Write Times')
    plt.legend()
    plt.show()

#funkcija za kreiranje bar chart
def bar_chart(without_idx, with_idx,i):
    X_axis = np.arange(len(i)) 
    plt.bar(X_axis - 0.2, without_idx, 0.4, label='Without Secondary Index') 
    plt.bar(X_axis + 0.2, with_idx, 0.4, label='With Secondary Index') 
    plt.xticks(X_axis, i) 
    plt.xlabel("Iterations") 
    plt.ylabel("Time taken (ns)") 
    plt.title("Comparison of Write Times") 
    plt.legend() 
    plt.show() 

Session = sessionmaker(bind = engine) 
session = Session()

#test podaci
df = pd.read_csv('titanic.csv')
df = df.drop(['PassengerId'], axis=1)
test_df = df.head(30) #prvih 30 podataka sa titanic CSV-a

#mjerenje vremena za ubacivanje podataka u bazu
measure_single(sec_indx_passanger)
measure_multiple(sec_indx_passanger,test_df)
session.close()

#podaci od mjerenja za kreiranje grafova
#varijable za rezultate od funkcije measure_single function
without_idx_time = [7871700,8545500,7986100,7591700,7627300]
with_idx_time = [7963900,9106200,8401700,8362500,9219100]

#varijable za rezultate od funkcije measure_multiple function
multi_without_idx_time = [138485500,137707100,139999200,136606200,138111200]
multi_with_idx_time = [144057400,141637700,149293400,149979000,156671300]

#stvaranje grafova
iterations = [1,2,3,4,5]
line_chart(multi_without_idx_time,multi_with_idx_time,iterations)
bar_chart(multi_without_idx_time,multi_with_idx_time,iterations)

