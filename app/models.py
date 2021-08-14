from app import db

class Class(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    coursenum = db.Column(db.String(3))  

    def __repr__(self):
        return '<Class id: {} - coursenum: {}>'.format(self.id,self.coursenum)
