import requests
import time
from ..config import ConfigClass

def exact_search(es_type, es_index, page, page_size, params, sort_by=None, sort_type=None):
    url = ConfigClass.ELASTIC_SEARCH_SERVICE + '{}/{}/_search'.format(es_index, es_type)

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


def insert_one(es_type, es_index, data):
    url = ConfigClass.ELASTIC_SEARCH_SERVICE + '{}/{}'.format(es_index, es_type)

    res = requests.post(url, json=data)

    return res.json()

def insert_one_by_id(es_type, es_index, data, id):
    url = ConfigClass.ELASTIC_SEARCH_SERVICE + '{}/{}/{}'.format(es_index, es_type, id)

    res = requests.put(url, json=data)

    return res.json()


def get_mappings(es_index):
    url = ConfigClass.ELASTIC_SEARCH_SERVICE + '{}/_mappings'.format(es_index)
    res = requests.get(url)

    return res.json()

def update_one_by_id(es_index, id, fields):
    url = ConfigClass.ELASTIC_SEARCH_SERVICE + '{}/_update/{}'.format(es_index, id)

    request_body = {
        "doc": fields
    }
    res = requests.post(url, json=request_body)

    return res.json()


def file_search(es_index, page, page_size, data, sort_by=None, sort_type=None):
    url = ConfigClass.ELASTIC_SEARCH_SERVICE + '{}/_search'.format(es_index)

    search_fields = []

    for item in data:
        if item['nested']:
            field_values = [
                { "match": { "attributes.name": item['name'] }},
                { "match": { "attributes.attribute_name": item['attribute_name'] }}
            ]

            if item['search_type'] == 'wildcard':
                field_values.append({ "wildcard": { "attributes.value": item['value'] }})
            elif item['search_type'] == 'match':
                field_values.append({ "match": { "attributes.value": item['value'] }})
            elif item['search_type'] == 'should':
                options = []
                for option in item['value']:
                    options.append({ "term": { "attributes.value": option }})
                field_values.append({
                    "bool": {
                        "should": options
                    }
                })
            elif item['search_type'] == 'must':
                options = []
                for option in item['value']:
                    options.append({ "term": { "attributes.value": option }})
                field_values.append({
                    "bool": {
                        "must": options
                    }
                })

            search_fields.append({
                "nested": {
                    "path": item['field'],
                    "query": {
                        "bool": {
                            "must": field_values,
                        }
                    }
                }
            })
        elif item['range']:
            if len(item['range']) == 1:
                if item['search_type'] == 'lte':
                    search_fields.append({
                        "range": {
                            item['field']: {"lte": int(item['range'][0])}
                        }
                    })
                else:
                    search_fields.append({
                        "range": {
                            item['field']: {"gte": int(item['range'][0])}
                        }
                    })
            else:
                search_fields.append({
                    "range": {
                        item['field']: {"gte": int(item['range'][0]), "lte": int(item['range'][1])}
                    }
                })
        elif item['multi_values']:
            options = []
            for option in item['value']:
                options.append({ "term": { item['field']: option }})
            
            if item['search_type'] == 'should':
                search_fields.append({
                    "bool": {
                        "should": options
                    }
                })
            else:
                search_fields.append({
                    "bool": {
                        "must": options
                    }
                })
        else:
            if item['search_type'] == 'contain':
                search_fields.append({
                    "wildcard": {
                        item['field']: '*{}*'.format(item['value'])
                    }
                })
            else:
                search_fields.append({
                    "term": {
                        item['field']: item['value']
                    }
                })

    search_params = {
        "query": {
            "bool": {
                "must": search_fields
            }
        },
        "size": page_size,
        "from": page * page_size,
        "sort": [
            {sort_by: sort_type}
        ]
    }

    print(url)
    print(search_params)

    res = requests.get(url, json=search_params)
    return res.json()