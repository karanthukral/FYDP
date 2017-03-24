from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import sys
import os

sys.path.append('../')

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://inara@localhost:5432/inara'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

from models.traffic import Traffic

ITEMS_PER_PAGE = 20

@app.route('/')
def hello():
    return "Hello World!"

@app.route('/api/v1.0/traffic/list/<int:page>', methods=['GET'])
def get_tasks(page=1):
    if request.method == "GET":
        print(request.args.get('min_created_at'))
        min_created_at = request.args.get('min_created_at')
        max_created_at = request.args.get('max_created_at')
        if min_created_at == None:
            created_after = datetime.strptime("1990-09-30 12:34:33", "%Y-%m-%d %H:%M:%S")
        else:
            created_after = datetime.strptime(min_created_at, "%Y-%m-%d %H:%M:%S")

        if max_created_at == None:
            created_before = datetime.strptime("2020-09-30 12:34:33", "%Y-%m-%d %H:%M:%S")
        else:
            created_before = datetime.strptime(max_created_at, "%Y-%m-%d %H:%M:%S")

        traffic = Traffic.query.filter(Traffic.created_at >
                created_after).filter(Traffic.created_at < created_before).order_by(Traffic.created_at).paginate(page,
                        ITEMS_PER_PAGE, False)


        return jsonify(traffic_objs=[t.serialize for t in traffic.items])
    else:
        return "You done goofed"

# @app.route('/tmp/create')
# def tempcreate():
    # traffic = Traffic(
            # human_id="facebook.com",
            # prob_bad=0.5,
            # ext_metadata={}
            # )
    # db.session.add(traffic)
    # db.session.commit()

if __name__ == '__main__':
    app.run()
