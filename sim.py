import pickle, os, random, time
from datetime import datetime

import psycopg2
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier

DATA_DIR = 'local_data/features/'

def setup_db():
    print('Connecting to DB...')
    conn = psycopg2.connect(host="localhost",database="inara", user="inara", password="")
    cursor = conn.cursor()

    print('Printing Version')
    cursor.execute('SELECT version()')

    # display the PostgreSQL database server version
    db_version = cursor.fetchone()
    print(db_version)
    print('DB Ready')
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

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25)

    # Fit the model
    clf.fit(X_train, y_train)
    print('Model training done, took ' + str(time.time()-start) + ' seconds')
    return [clf, X]

def classify(clf, data):
    return clf.predict(data)

def iterate(clf, X, cursor):
    full_db_data = pickle.load(open(os.path.join(DATA_DIR,'flow-for-db.pkl'),'rb'))
    for idx, data in enumerate(X):
        tag = classify(clf, [data])
        db_datum = full_db_data[idx]
        db_datum.append(tag)
        db_datum.append([datetime.now().strftime("%Y-%m-%d"), datetime.now().strftime("%H:%M:%S")])
        db_datum.append([datetime.now().strftime("%Y-%m-%d"), datetime.now().strftime("%H:%M:%S")])
        print("Inserting " + str(db_datum))
        insert(cursor, db_datum)
        time.sleep(random.random())

if __name__ == "__main__":
    cursor = setup_db()
    clf, X = make_model()
    iterate(clf, X, cursor)

    # close connection
    cursor.close()
