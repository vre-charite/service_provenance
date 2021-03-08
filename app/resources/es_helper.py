import requests
import time
from ..config import ConfigClass

def exact_search(es_type, resource, page, page_size, params, sort_by=None, sort_type=None):
    url = ConfigClass.ELASTIC_SEARCH_SERVICE + '{}/{}/_search'.format(resource, es_type)

    search_params = []

    for key, value in params.items():
        if key != 'createdTime':
            search_params.append({
                "constant_score" : {
                    "filter" : {
                        "term" : {
                            key : value
                        }
                    }
                }
            })
        else:
            search_params.append({
                "constant_score" : {
                    "filter": {
                        "range": {
                            "createdTime": {"gte": value[0], "lte": value[1]}
                        }
                    }
                }
            })
    search_data = {
        "query" : {
            "bool": {
                "must": search_params
            }
        },
        "size": page_size,
        "from": page * page_size,
        "sort": [
            {sort_by: sort_type}
        ]
    }

    res = requests.get(url, json=search_data)
    return res.json()


def insert_one(es_type, resource, data):
    url = ConfigClass.ELASTIC_SEARCH_SERVICE + '{}/{}'.format(resource, es_type)

    res = requests.post(url, json=data)

    return res.json()
