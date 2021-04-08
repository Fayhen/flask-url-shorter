from sqlalchemy import Column, Integer, String
from api.database import Base
from api.serializers import BaseSerializer


class Url(Base, BaseSerializer):
    __tablename__ = 'urls'
    id = Column(Integer, primary_key=True)
    clicks = Column(Integer, nullable=False, default=0)
    short_url = Column(String, unique=True, nullable=False)
    long_url = Column(String, nullable=False)

    def serialize(self):
        data = BaseSerializer.serialize(self)
        del data['id']
        return data
