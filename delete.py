from main import engine, Passanger,sec_indx_passanger
from sqlalchemy.orm import sessionmaker

Session = sessionmaker(bind = engine)
session = Session()

#Brisanje svih podataka u bazi
session.query(Passanger).delete()
session.query(sec_indx_passanger).delete()
session.commit()
print("All data deleted from database")
session.close()