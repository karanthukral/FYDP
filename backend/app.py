from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
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
        only_flagged = request.args.get('only_flagged')
        min_created_at = request.args.get('min_created_at')
        if min_created_at == None:
            created_after = datetime.strptime("1990-09-30 12:34:33", "%Y-%m-%d %H:%M:%S")
        else:
            created_after = datetime.strptime(min_created_at, "%Y-%m-%d %H:%M:%S")

        if only_flagged:
            traffic = Traffic.query.filter_by(flagged=True).filter(Traffic.created_at > created_after).order_by(Traffic.created_at)
        else:
            traffic = Traffic.query.filter(Traffic.created_at > created_after).order_by(Traffic.created_at)

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

@app.route('/api/v1.0/traffic/classify', methods=['POST'])
def classfify():
    if request == "POST":
        domain = str(request.form['domain'])
    else:
        return "You done goofed"


if __name__ == '__main__':
    app.run()
