import psycopg2

import os
import random
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier

DATA_DIR = 'local_data/features/'

def setup_db():
    print('Connecting to DB')
    conn = psycopg2.connect(host="localhost",database="inara", user="inara", password="")
    cursor = conn.cursor()

    print('Printing Version')
    cursor.execute('SELECT version()')

    # display the PostgreSQL database server version
    db_version = cursor.fetchone()
    print(db_version)

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
    X = np.load(os.path.join(DATA_DIR, 'features-new.npy'))
    y = np.load(os.path.join(DATA_DIR, 'labels-new.npy'))[0]

    clf = RandomForestClassifier(n_estimators=25, n_jobs=-1)

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25)

    # Fit the model
    clf.fit(X_train, y_train)
    return clf

def classify(clf, data):
    return clf.predict(data)

def iterate(clf, cursor):
    pass


if __name__ == "__main__":
    cursor = setup_db()
    clf = make_model()
    iterate(clf, cursor)

    # close connection
    cursor.close()
