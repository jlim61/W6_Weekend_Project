from app import db

from werkzeug.security import generate_password_hash, check_password_hash

friends = db.Table('Friends List',
    db.Column('friending_id', db.Integer, db.ForeignKey('users.id')),
    db.Column('friended_id', db.Integer, db.ForeignKey('users.id'))
)

class UserModel(db.Model):

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)
    password_hash = db.Column(db.String, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    ign = db.Column(db.String, unique=True, nullable=False)
    items = db.relationship('ItemModel', backref='author', lazy='dynamic', cascade='all, delete')
    friend_list = db.relationship('UserModel', secondary=friends,
        primaryjoin = friends.c.friending_id == id,
        secondaryjoin = friends.c.friended_id == id,
        backref = db.backref('friends', lazy='dynamic'),
        lazy='dynamic'
    )

    def __repr__(self):
        return f'<User: {self.ign}>'
    
    def hash_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def from_dict(self, dict):
        password = dict.pop('password')
        self.hash_password(password)
        for k,v in dict.items():
            setattr(self, k, v)

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def is_friended(self, user):
        return self.friend_list.filter(user.id == friends.c.friended_id).count() > 0

    def add_friend(self, user):
        if not self.is_friended(user):
            self.friend_list.append(user)
            self.save()

    def unfriend(self, user):
        if self.is_friended(user):
            self.friend_list.remove(user)
            self.save()