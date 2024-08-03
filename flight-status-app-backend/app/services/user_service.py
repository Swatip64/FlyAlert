# app/services/user_service.py

from ..models import User
from .. import db

def get_user(user_id):
    return User.query.get(user_id)

def update_user_preferences(user_id, preferences):
    user = get_user(user_id)
    if user:
        user.preferences = ','.join(preferences)
        db.session.commit()
