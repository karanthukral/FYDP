from elasticsearch import Elasticsearch
import json

size = 10
from_index = 1000
doc_type = 'syslog' # possibilities = syslog, wineventlog

es = Elasticsearch()
response = es.search(index='homequitybank-2016.09.01', _source='', size=size,
        from_=from_index, doc_type=doc_type)
print(json.dumps(response, indent=2))
# res = es.get(index="homequitybank-2016.09.01", doc_type="_all", id="AVbjgUD8h76HlwhVdggy")
