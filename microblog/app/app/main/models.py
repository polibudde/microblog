from app import db
from datetime import datetime

#create a model
class Post(db.Model):   # now we define the colums
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.String(400), nullable=False)
    completed = db.Column(db.Integer, default=0)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('flasklogin-users.id'))

    #create a function that returns a string every time we create a new element
    def __repr__(self):
        return '<Task %r' % self.id

