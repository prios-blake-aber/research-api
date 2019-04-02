
import requests
from elasticsearch import Elasticsearch


def query(index='person_v0', input_string='Blake'):
    return es.search(
        index=index, body={
            "query": {
                "multi_match": {
                    "query": input_string
                }
            }
        }
    )


# PULL DIRECTLY FROM ES
es = Elasticsearch(hosts='localhost:9200')


# PULL ES METADATA
r = requests.get('http://localhost:9200/_cluster/state?pretty')
data = r.json()
data['metadata']['indices'].keys()
