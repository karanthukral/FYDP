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
    created_at = db.Column(db.DateTime)
    updated_at = db.Column(db.DateTime)

    # Source Details
    total_src_bytes = db.Column(db.String)
    total_src_pkts = db.Column(db.String)
    src_b64_payload = db.Column(db.String)
    src_utf_payload = db.Column(db.String)
    src_tcp_flags = db.Column(db.String)
    src_ip = db.Column(db.String)
    src_port = db.Column(db.String)

    # Destination Details
    total_dst_bytes = db.Column(db.String)
    total_dst_pkts = db.Column(db.String)
    dst_b64_payload = db.Column(db.String)
    dst_utf_payload = db.Column(db.String)
    dst_tcp_flags = db.Column(db.String)
    dst_ip = db.Column(db.String)
    dst_port = db.Column(db.String)

    # Common Details
    app_name = db.Column(db.String)
    direction = db.Column(db.String)
    start_time = db.Column(db.String)
    end_time = db.Column(db.String)
    tag = db.Column(db.String)

    # ML Tag
    classified_tag = db.Column(db.String)

    # ext_metadata = db.Column(JSON)

    def __init__(self):
        self.created_at = datetime.datetime.now()
        self.updated_at = datetime.datetime.now()

    def __repr__(self):
        return '<id {}>'.format(self.id)

    @property
    def serialize(self):
        return {
                'id': self.id,
                'created_at': dump_datetime(self.created_at),
                'updated_at': dump_datetime(self.updated_at),
                'total_src_bytes': self.total_src_bytes,
                'total_src_pkts': self.total_src_pkts,
                'src_b64_payload': self.src_b64_payload,
                'src_utf_payload': self.src_utf_payload,
                'src_tcp_flags': self.src_tcp_flags,
                'src_ip': self.src_ip,
                'src_port': self.src_port,
                'total_dst_bytes': self.total_dst_bytes,
                'total_dst_pkts': self.total_dst_pkts,
                'dst_b64_payload': self.dst_b64_payload,
                'dst_utf_payload': self.dst_utf_payload,
                'dst_tcp_flags': self.dst_tcp_flags,
                'dst_ip': self.dst_ip,
                'dst_port': self.dst_port,
                'app_name': self.app_name,
                'direction': self.direction,
                'start_time': dump_datetime(self.start_time),
                'end_time': dump_datetime(self.end_time),
                'tag': self.tag,
                'classified_tag': self.classified_tag,
        }


