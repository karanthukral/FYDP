import psycopg2

print('Connecting to DB')
conn = psycopg2.connect(host="localhost",database="inara", user="inara", password="")
cursor = conn.cursor()

print('Printing Version')
cursor.execute('SELECT version()')

# display the PostgreSQL database server version
db_version = cursor.fetchone()
print(db_version)

# close connection
cursor.close()

def insert(cursor, values):
    # Insert statement
    sql = """INSERT INTO inara(total_src_bytes, total_src_pkts, src_b64_payload,
src_utf_payload, src_tcp_flags, src_ip, src_port, total_dst_bytes,
total_dst_pkts, dst_b64_payload, dst_utf_payload, dst_tcp_flags, dst_ip,
dst_port, app_name, direction, start_time, end_time, tag, classified_tag,
created_at, updated_at) VALUES(%s) RETURNING id;"""
    cursor.execute(sql, values)
