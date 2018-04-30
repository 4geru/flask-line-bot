from sqlalchemy import create_engine
from setting import Base, Restaurant, MenuItem
engine = create_engine('sqlite:///restaurantMenu.db')
Base.metadata.bind=engine

from sqlalchemy.orm import sessionmaker
Session = sessionmaker(bind=engine)
session = Session()

#create
new_restaurant = Restaurant(name='Pizza Palace')
session.add(new_restaurant)
session.commit()

#read
restrants = session.query(Restaurant).all()
print('before')
for restrant in restrants:
    print(restrant.id)
delete_restrants = restrants[0]
session.delete(delete_restrants)
session.commit()
print('after')
restrants = session.query(Restaurant).all()
for restrant in restrants:
    print(restrant.id)