from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import sys
import os

app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

sys.path.append('../')

from models.traffic import Traffic
from lib import domain_classifier

TRAIN = False

nn = domain_classifier()

if TRAIN:
    nn.train()
else:
    nn.load_model()

@app.route('/')
def hello():
    return "Hello World!"

@app.route('/api/v1.0/traffic/list', methods=['GET'])
def get_tasks():
    if request.method == "GET":
        min_prob_bad = request.args.get('min_prob_bad')
        min_created_at = request.args.get('min_created_at')
        if min_created_at == None:
            created_after = datetime.strptime("1990-09-30 12:34:33", "%Y-%m-%d %H:%M:%S")
        else:
            created_after = datetime.strptime(min_created_at, "%Y-%m-%d %H:%M:%S")

        if min_prob_bad == None:
            traffic = Traffic.query.filter(Traffic.created_at > created_after).order_by(Traffic.created_at)
        else:
            traffic = Traffic.query.filter_by(prob_bad >= min_prob_bad).filter(Traffic.created_at > created_after).order_by(Traffic.created_at)

        return jsonify(traffic_objs=[t.serialize for t in traffic.all()])
    else:
        return "You done goofed"

@app.route('/tmp/create')
def tempcreate():
    traffic = Traffic(
            human_id="facebook.com",
            prob_bad=0.5,
            ext_metadata={}
            )
    db.session.add(traffic)
    db.session.commit()

@app.route('/api/v1.0/traffic/classify', methods=['POST'])
def classfify():
    if request.method == "POST":
        domain = str(request.form['domain'])
        evaluated = nn.evaluate_domain(domain)
        traffic = Traffic(
                human_id=domain,
                prob_bad = float(evaluated[0]),
                ext_metadata = {}
                )
        db.session.add(traffic)
        db.session.commit()
        return jsonify(traffic.serialize)
    else:
        return "You done goofed"


if __name__ == '__main__':
    app.run()
