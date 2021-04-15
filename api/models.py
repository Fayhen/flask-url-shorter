# from sqlalchemy import Column, Integer, String
from api import db
from api.serializers import BaseSerializer


class Url(db.Model, BaseSerializer):
    __tablename__ = 'urls'
    id = db.Column(db.Integer, primary_key=True)
    clicks = db.Column(db.Integer, nullable=False, default=0)
    long_url = db.Column(db.String, nullable=False)
    hash = db.Column(db.String, unique=True)

    def serialize(self):
        data = BaseSerializer.serialize(self)
        # del data['id']
        return data

    # def get_short_url(self):
