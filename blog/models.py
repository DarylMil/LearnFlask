from flask import current_app
from datetime import datetime
from blog import db, login_manager
from flask_login import UserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

now = datetime.utcnow()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
 
class User(db.Model, UserMixin):
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(length=20), unique=True, nullable=False)
    email = db.Column(db.String(length=120), unique=True, nullable=False)
    image_file = db.Column(db.String(length=20), nullable=False, default='default.jpg')
    password = db.Column(db.String(length=60), nullable=False)
    posts = db.relationship('Post', backref='author', lazy='select') # this isn't an actual column but its making queries to the post table

    def get_reset_token(self, expires_sec=1800):
        s = Serializer(current_app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id':self.id}).decode('utf-8') # creates the Token and pass in the payload as args. Then change it from bytes to utf

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id'] # s.loads() returns a dict, and we want the 'user_id'
        except:
            return None
        return User.query.get(user_id)

    def __repr__(self):
        return f"User({self.username}, {self.email}, {self.image_file}"

# It will automatically create a table in our db named 'post' *note it is lower case
class Post(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    title = db.Column(db.String(length=100), nullable=False)
    date_posted = db.Column(db.DateTime(), nullable=False, default = now)
    content = db.Column(db.Text(), nullable=False)
    user_id = db.Column(db.Integer(), db.ForeignKey('user.id'), nullable=False) # user.id is lower case unlike relationship Upper case 'Post', is because ForeignKey we are referencing the table while relationship is the class


    def __repr__(self):
        return f"Post({self.title}, {self.date_posted})"
