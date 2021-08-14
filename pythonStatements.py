

from app import db
#create the database file, if it doesn't exist. 
db.create_all()

# import db models
from app.models import Class

#create class objects and write them to the database
newClass = Class(coursenum='322')
db.session.add(newClass)
newClass = Class(coursenum='355')
db.session.add(newClass)
db.session.commit()

# query and print classes
Class.query.all()
Class.query.filter_by(coursenum='322').all()
Class.query.filter_by(coursenum='322').first()
myclasses = Class.query.order_by(Class.coursenum.desc()).all()
for c in myclasses:
    print(c.coursenum)
