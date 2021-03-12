import os

class ConfigClass(object):
    env = os.environ.get('env')

    version = "0.1.0"
    VRE_ROOT_PATH = "/vre-data"
    METADATA_API = "http://cataloguing.utility:5064"
    UTILITY_SERVICE = "http://common.utility:5062/"
    ELASTIC_SEARCH_SERVICE = "http://elasticsearch-master.utility:9200/"
    ATLAS_API = "http://atlas.utility:21000/"
    ATLAS_ADMIN = "admin"
    ATLAS_PASSWD = "admin"

    # disk mounts
    NFS_ROOT_PATH = "./"
    VRE_ROOT_PATH = "/vre-data"

    # download secret
    DOWNLOAD_KEY = "indoc101"
    DOWNLOAD_TOKEN_EXPIRE_AT = 5

    # Redis Service
    # REDIS_HOST = "10.3.7.233"
    REDIS_HOST = "redis-master.utility"
    REDIS_PORT = 6379
    REDIS_DB = 0
    REDIS_PASSWORD = {
        'staging': '8EH6QmEYJN',
        'charite': 'o2x7vGQx6m'
    }.get(env, "5wCCMMC1Lk")
