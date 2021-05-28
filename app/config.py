import os
# os.environ['env'] = 'test'

class ConfigClass(object):
    env = os.environ.get('env')

    version = "0.1.0"

    ATLAS_ADMIN = "admin"
    ATLAS_PASSWD = "admin"

    UTILITY_SERVICE = "http://common.utility:5062/v1/"
    ELASTIC_SEARCH_SERVICE = "http://elasticsearch-master.utility:9200/"
    ATLAS_API = "http://atlas.utility:21000/"
    if env == "test":
        METADATA_API = "http://10.3.7.237:5064"
        UTILITY_SERVICE = "http://10.3.7.222:5062/v1/"
        ELASTIC_SEARCH_SERVICE = "http://10.3.7.219:9200/"
        ATLAS_API = "http://10.3.7.204:21000/"
