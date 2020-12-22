import sqlalchemy as db


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)

    def __repr__(self):
        return '<User: {}>'.format(self.name)

class Event(db.Model):
    __tablename__ = 'events'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    lon = db.Column(db.Float())
    lat = db.Column(db.Float())
    timestamp = db.Column(db.DateTime)

    def __repr__(self):
        return f'<Event: {id}>'