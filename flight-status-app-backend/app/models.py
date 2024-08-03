from app import db
from sqlalchemy.dialects.postgresql import JSONB

class Flight(db.Model):
    __tablename__ = 'flights'

    id = db.Column(db.Integer, primary_key=True)
    flight_number = db.Column(db.String(10), unique=True, nullable=False)
    status = db.Column(db.String(20), nullable=False)
    gate = db.Column(db.String(5))
    arrival_time = db.Column(db.DateTime)
    boarding_time = db.Column(db.DateTime)

    def __repr__(self):
        return f'<Flight {self.flight_number}>'

    @staticmethod
    def create_flight(flight_number, status, gate, arrival_time, boarding_time):
        flight = Flight(flight_number=flight_number, status=status, gate=gate, arrival_time=arrival_time, boarding_time=boarding_time)
        db.session.add(flight)
        db.session.commit()
        return flight

    @staticmethod
    def get_flight_by_id(flight_id):
        return Flight.query.get(flight_id)

    @staticmethod
    def update_flight(flight_id, **kwargs):
        flight = Flight.query.get(flight_id)
        for key, value in kwargs.items():
            setattr(flight, key, value)
        db.session.commit()
        return flight

    @staticmethod
    def delete_flight(flight_id):
        flight = Flight.query.get(flight_id)
        db.session.delete(flight)
        db.session.commit()

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    phone_number = db.Column(db.String(15))
    notification_preferences = db.Column(JSONB, nullable=False)

    def __repr__(self):
        return f'<User {self.name}>'

    @staticmethod
    def create_user(name, email, phone_number, notification_preferences):
        user = User(name=name, email=email, phone_number=phone_number, notification_preferences=notification_preferences)
        db.session.add(user)
        db.session.commit()
        return user

    @staticmethod
    def get_user_by_id(user_id):
        return User.query.get(user_id)

    @staticmethod
    def update_user(user_id, **kwargs):
        user = User.query.get(user_id)
        for key, value in kwargs.items():
            setattr(user, key, value)
        db.session.commit()
        return user

    @staticmethod
    def delete_user(user_id):
        user = User.query.get(user_id)
        db.session.delete(user)
        db.session.commit()

class Notification(db.Model):
    __tablename__ = 'notifications'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'))
    flight_id = db.Column(db.Integer, db.ForeignKey('flights.id', ondelete='CASCADE'))
    message = db.Column(db.Text, nullable=False)
    sent_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    notification_type = db.Column(db.String(20), nullable=False)

    user = db.relationship('User', backref=db.backref('notifications', lazy=True))
    flight = db.relationship('Flight', backref=db.backref('notifications', lazy=True))

    def __repr__(self):
        return f'<Notification {self.id} for User {self.user_id}>'

    @staticmethod
    def create_notification(user_id, flight_id, message, notification_type):
        notification = Notification(user_id=user_id, flight_id=flight_id, message=message, notification_type=notification_type)
        db.session.add(notification)
        db.session.commit()
        return notification

    @staticmethod
    def get_notification_by_id(notification_id):
        return Notification.query.get(notification_id)

    @staticmethod
    def delete_notification(notification_id):
        notification = Notification.query.get(notification_id)
        db.session.delete(notification)
        db.session.commit()
