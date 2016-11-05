from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

from models.traffic import Traffic

@app.route('/')
def hello():
    return "Hello World!"

@app.route('/api/v1.0/traffic/list', methods=['GET'])
def get_tasks():
    if request.method == "GET":
        traffic = Traffic.query.order_by(Traffic.created_at)
        return jsonify(traffic_objs=[t.serialize for t in traffic.all()])
    else:
        return "You done goofed"

@app.route('/tmp/create')
def tempcreate():
    traffic = Traffic(
            human_id="facebook.com",
            flagged=False,
            ext_metadata={}
            )
    db.session.add(traffic)
    db.session.commit()

if __name__ == '__main__':
    app.run()
