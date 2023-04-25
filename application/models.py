from .database import db 

class user(db.Model):
    __tablename__="user"
    user_id=db.Column(db.Integer,primary_key=True)
    username=db.Column(db.String)
    password=db.Column(db.String)
    dob=db.Column(db.String)
    email=db.Column(db.String)
    date_joined=db.Column(db.String)
    todos=db.relationship('todo',backref='user')


class todo(db.Model):
    __tablename__="todo"
    todo_id=db.Column(db.Integer,primary_key=True)
    creator_id=db.Column(db.Integer,  db.ForeignKey("user.user_id"))
    title=db.Column(db.String)
    description=db.Column(db.String)
    status=db.Column(db.Integer)
    date_created=db.Column(db.String)
    deadline=db.Column(db.String)
    last_updated=db.Column(db.String)
