import pickle
import os
import random
import time

from datetime import datetime
import psycopg2
import numpy as np
from sklearn.ensemble import RandomForestClassifier

DATA_DIR = 'local_data/features/'


def setup_db():
    print('Connecting to DB...')
    conn = psycopg2.connect(host="localhost",
                            database="inara",
                            user="inara",
                            password="")
    cursor = conn.cursor()

    print('Printing Version')
    cursor.execute('SELECT version()')

    # display the PostgreSQL database server version
    db_version = cursor.fetchone()
    print('DB Ready, v{}'.format(db_version))
    return cursor


def insert(cursor, values):
    # Insert statement
    sql = """INSERT INTO inara(total_src_bytes, total_src_pkts, src_b64_payload,
src_utf_payload, src_tcp_flags, src_ip, src_port, total_dst_bytes,
total_dst_pkts, dst_b64_payload, dst_utf_payload, dst_tcp_flags, dst_ip,
dst_port, app_name, direction, start_time, end_time, tag, classified_tag,
created_at, updated_at) VALUES(%s) RETURNING id;"""
    cursor.execute(sql, values)


def make_model():

    print('Beginning model training...')
    start = time.time()
    X = np.load(os.path.join(DATA_DIR, 'features-new.npy'))
    y = np.load(os.path.join(DATA_DIR, 'labels-new.npy'))[0]

    clf = RandomForestClassifier(n_estimators=25, n_jobs=-1)
    clf.fit(X, y)
    print('Model training done, took {} seconds'.format(time.time()-start))
    return [clf, X]


def classify(clf, data):
    return clf.predict(data)


def iterate(clf, X, cursor):
    full_db_data = pickle.load(
        open(os.path.join(DATA_DIR, 'flow-for-db.pkl'), 'rb'))
    for idx, data in enumerate(X):
        tag = classify(clf, [data])
        db_datum = full_db_data[idx]
        db_datum.append(tag)
        dtn = datetime.now()
        db_datum.append([dtn.strftime("%Y-%m-%d"), dtn.strftime("%H:%M:%S")])
        db_datum.append([dtn.strftime("%Y-%m-%d"), dtn.strftime("%H:%M:%S")])
        print("Inserting {}".format(db_datum))
        insert(cursor, db_datum)
        time.sleep(random.random())  # wait a random amount of time t: 0<t<1s


if __name__ == "__main__":
    cursor = setup_db()
    clf, X = make_model()
    iterate(clf, X, cursor)
    # close connection
    cursor.close()
