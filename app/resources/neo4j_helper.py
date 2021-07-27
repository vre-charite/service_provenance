import requests
from ..config import ConfigClass

def http_query_node(primary_label, query_params={}):
    '''
    primary_label i.e. Folder, File, Container
    '''
    payload = {
        **query_params
    }
    node_query_url = ConfigClass.NEO4J_SERVICE + "nodes/{}/query".format(primary_label)
    response = requests.post(node_query_url, json=payload)
    return response