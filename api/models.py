from hashids import Hashids

from api import db
from api.methods import generate_hash
from api.serializers import BaseSerializer


class Url(db.Model, BaseSerializer):
    __tablename__ = 'urls'
    id = db.Column(db.Integer, primary_key=True)
    clicks = db.Column(db.Integer, nullable=False, default=0)
    long_url = db.Column(db.String, nullable=False)
    hash = db.Column(db.String, unique=True)

    def serialize(self):
        data = BaseSerializer.serialize(self)
        del data['id']
        return data

    @staticmethod
    def create_new(long_url):
        new_url = Url(long_url=long_url)
        db.session.add(new_url)
        db.session.commit()

        new_url.hash = generate_hash(new_url.id)
        db.session.add(new_url)
        db.session.commit()

        return new_url

    def generate_hash(self):
        self.hash = generate_hash(self.id)
        db.session.add(self)
        db.session.commit()

        return self.hash

    @staticmethod
    def get_url_by_hash(url_hash):
        url_instance = Url.query.filter_by(hash=url_hash).first()

        return url_instance if url_instance else None
