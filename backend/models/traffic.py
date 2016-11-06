from app import db
from sqlalchemy.dialects.postgresql import JSON
import datetime

def dump_datetime(value):
    if value is None:
        return None
    return [value.strftime("%Y-%m-%d"), value.strftime("%H:%M:%S")]

class Traffic(db.Model):
    __tablename__ = 'traffic'

    id = db.Column(db.Integer, primary_key=True)
    human_id = db.Column(db.String)
    created_at = db.Column(db.DateTime)
    updated_at = db.Column(db.DateTime)
    prob_bad = db.Column(db.Float)
    ext_metadata = db.Column(JSON)

    def __init__(self, human_id, prob_bad, ext_metadata):
        self.human_id = human_id
        self.prob_bad = prob_bad
        self.ext_metadata = ext_metadata if ext_metadata else {}
        self.created_at = datetime.datetime.now()
        self.updated_at = datetime.datetime.now()

    def __repr__(self):
        return '<id {}>'.format(self.id)

    @property
    def serialize(self):
        return {
                'id': self.id,
                'human_id': self.human_id,
                'prob_bad': self.prob_bad,
                'created_at': dump_datetime(self.created_at),
                'updated_at': dump_datetime(self.updated_at),
                'ext_metadata': self.ext_metadata
        }


