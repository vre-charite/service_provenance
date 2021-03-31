import unittest
from fastapi.testclient import TestClient
from app.main import create_app    
from app.config import ConfigClass
from .logger import Logger
import requests
import pprint
import time
import json

pp = pprint.PrettyPrinter(indent=4)

app = create_app()

class TestFileMeta(unittest.TestCase):
    client = TestClient(app)
    log = Logger(name='test_file_meta.log')

    project_code = 'unit_test'
    uploader1 = 'unit_test_admin1'
    uploader2 = 'unit_test_admin2'
    uploader3 = 'unit_test_admin3'

    url = '/v1/file-meta'

    @classmethod
    def create_file(self):
        current_timestamp = time.time()
        payload1 = {
            "global_entity_id": "string_{}".format(current_timestamp),
            "data_type": "File",
            "file_type": "string",
            "operator": self.uploader1,
            "zone": "string",
            "file_size": 10,
            "tags": [
                "tag1",
                "tag2"
            ],
            "archived": False,
            "path": "string",
            "time_lastmodified": int(current_timestamp),
            "time_created": int(current_timestamp),
            "process_pipeline": "string",
            "uploader": self.uploader1,
            "file_name": "string",
            "atlas_guid": "string",
            "full_path": "string",
            "generate_id": "string",
            "project_code": self.project_code,
            "attributes": [{
                "name": "Attribute1",
                "attribute_name": "attr1",
                "value": ["a1"]
            },
            {
                "name": "Attribute1",
                "attribute_name": "attr2",
                "value": "lalala2"
            }],
            "priority": 20
        }

        res = self.client.post(self.url, json=payload1)
        self.log.info(f"RESPONSE DATA: {res.json()}")
        self.log.info(f"RESPONSE STATUS: {res.status_code}")
        self.log.info(f"COMPARING: {res.status_code} VS 200")
    
        payload2 = payload1
        payload2["global_entity_id"] = "string2_{}".format(current_timestamp)
        payload2["operator"] = self.uploader2
        payload2["uploader"] = self.uploader2
        payload2["tags"] = ["tag1", "tag3"]
        payload2["file_size"] = 100
        payload2["attributes"] = [{
            "name": "Attribute1",
            "attribute_name": "attr1",
            "value": ["a1", "a2"]
        },{
            "name": "Attribute1",
            "attribute_name": "attr2",
            "value": "lalala3"
        }]

        res = self.client.post(self.url, json=payload2)
        self.log.info(f"RESPONSE DATA: {res.json()}")
        self.log.info(f"RESPONSE STATUS: {res.status_code}")
        self.log.info(f"COMPARING: {res.status_code} VS 200")

    @classmethod
    def setUpClass(cls):
        try:
            cls.entity_raw = cls.create_file()
        except Exception as e:
            print(f"Filed to setup test: {e}")
            cls.log.error(f"Failed to setup test {e}")
            raise unittest.SkipTest(f"Failed to setup test {e}")

    def test_01_create_file(self):
        current_timestamp = time.time()
        payload1 = {
            "global_entity_id": "string_{}".format(current_timestamp),
            "data_type": "File",
            "file_type": "string",
            "operator": self.uploader3,
            "zone": "string",
            "file_size": 10,
            "tags": [
                "tag1"
            ],
            "archived": False,
            "path": "string",
            "time_lastmodified": int(current_timestamp),
            "time_created": int(current_timestamp),
            "process_pipeline": "string",
            "uploader": self.uploader3,
            "file_name": "string",
            "atlas_guid": "string",
            "full_path": "string",
            "generate_id": "string",
            "project_code": self.project_code,
            "attributes": [{
                "name": "Attribute1",
                "attribute_name": "attr1",
                "value": ["a1", "a3"]
            },
            {
                "name": "Attribute1",
                "attribute_name": "attr2",
                "value": "lalala2"
            }],
            "priority": 20
        }

        res = self.client.post(self.url, json=payload1)
        self.log.info(f"RESPONSE DATA: {res.json()}")
        self.log.info(f"RESPONSE STATUS: {res.status_code}")
        self.log.info(f"COMPARING: {res.status_code} VS 200")

    def test_02_query_files(self):
        # search by project
        query = {
            "project_code": {
                "value": self.project_code,
                "condition": "equal"
            }
        }
        query = json.dumps(query)

        res = self.client.get(self.url, params={"query": query })
        result = res.json()
        self.log.info(f"RESPONSE DATA: {result}")

        data = result["result"]
        self.assertGreater(len(data), 0)

        is_all_equal_project = True
        for record in data:
            attribute = record['_source']
            if attribute['project_code'] != self.project_code:
                is_all_equal_project = False
                break
        self.assertEqual(is_all_equal_project, True)


        query2 = {
            "project_code": {
                "value": self.project_code,
                "condition": "contain"
            }
        }
        query2 = json.dumps(query2)
        res = self.client.get(self.url, params={"query": query2 })
        result = res.json()
        data = result["result"]

        is_all_contain_project = True
        for record in data:
            attribute = record['_source']
            if not self.project_code in attribute['project_code']:
                is_all_contain_project = False
                break
        self.assertEqual(is_all_contain_project, True)

    def test_03_query_files(self):
        # search by file size
        query = {
            "project_code": {
                "value": self.project_code,
                "condition": "equal"
            },
            "file_size": {
                "value": [10],
                "condition": "lte"
            }
        }
        query = json.dumps(query)

        res = self.client.get(self.url, params={"query": query })
        result = res.json()
        data = result["result"]

        is_all_small_file = True
        for record in data:
            attribute = record['_source']
            file_size = attribute['file_size']

            if file_size > 10:
                is_all_small_file = False
                break
        
        self.assertEqual(is_all_small_file, True)


    def test_04_query_files(self):
        # search with page size
        query = {
            "project_code": {
                "value": self.project_code,
                "condition": "equal"
            }
        }
        query = json.dumps(query)

        res = self.client.get(self.url, params={"query": query, "page_size": 10 })
        result = res.json()
        data = result["result"]

        self.assertLessEqual(len(data), 10)

    def test_05_query_files(self):
        # search with sorting field
        query = {
            "project_code": {
                "value": self.project_code,
                "condition": "equal"
            }
        }
        query = json.dumps(query)

        res = self.client.get(self.url, params={"query": query, "page_size": 10,  "sort_by": "time_created", "sort_type": "asc" })
        result = res.json()
        data = result["result"]

        created_times = []

        for record in data:
            attribute = record['_source']

            created_times.append(attribute['time_created'])
        
        sorted_times = created_times
        sorted_times.sort()

        self.assertEqual(sorted_times, created_times)

    def test_06_query_files(self):
        # search with tags
        query = {
            "project_code": {
                "value": self.project_code,
                "condition": "equal"
            },
            "tags": {
                "value": ["tag1", "tag2"],
                "condition": "contain"
            }
        }
        query = json.dumps(query)

        res = self.client.get(self.url, params={"query": query, "page_size": 10,  "sort_by": "time_created", "sort_type": "asc" })
        result = res.json()
        data = result["result"]

        containe_result = []

        for record in data:
            attribute = record['_source']
            tags = attribute['tags']

            if 'tag1' in tags or 'tag2' in tags:
                containe_result.append(record)
        
        self.assertEqual(len(containe_result), len(data))

        query = {
            "project_code": {
                "value": self.project_code,
                "condition": "equal"
            },
            "tags": {
                "value": ["tag1", "tag2"],
                "condition": "equal"
            }
        }
        query = json.dumps(query)

        res = self.client.get(self.url, params={"query": query, "page_size": 10,  "sort_by": "time_created", "sort_type": "asc" })
        result = res.json()
        data = result["result"]

        equal_result = []

        for record in data:
            attribute = record['_source']
            tags = attribute['tags']

            if tags == ["tag1", "tag2"]:
                equal_result.append(record)
        
        self.assertEqual(len(equal_result), len(data))

    
    def test_06_query_files(self):
        # search with attributes
        query = {
            "project_code": {
                "value": self.project_code,
                "condition": "equal"
            },
            "attributes": {
                "name": "Attribute1",
                "attribute_name": "attr1",
                "value": ["a1"], 
                "type": "multiple choice",
                "condition": "contain"
            }
        }

        query = json.dumps(query)

        res = self.client.get(self.url, params={"query": query, "page_size": 10,  "sort_by": "time_created", "sort_type": "asc" })
        result = res.json()
        data = result["result"]

        containe_result = []
        for record in data:
            attribute = record['_source']
            attributes = attribute['attributes']

            for item in attributes:
                if item['name'] == "Attribute1" and item["attribute_name"] == "attr1":
                    value = item["value"]

                    if "a1" in value:
                        containe_result.append(record)
        self.assertEqual(len(containe_result), len(data))

        
        query = {
            "project_code": {
                "value": self.project_code,
                "condition": "equal"
            },
            "attributes": {
                "name": "Attribute1",
                "attribute_name": "attr1",
                "value": ["a1"], 
                "type": "multiple choice",
                "condition": "equal"
            }
        }

        query = json.dumps(query)

        res = self.client.get(self.url, params={"query": query, "page_size": 10,  "sort_by": "time_created", "sort_type": "asc" })
        result = res.json()
        data = result["result"]

        equal_result = []
        for record in data:
            attribute = record['_source']
            attributes = attribute['attributes']

            for item in attributes:
                if item['name'] == "Attribute1" and item["attribute_name"] == "attr1":
                    value = item["value"]

                    if value == ["a1"]:
                        equal_result.append(record)
        # self.assertEqual(len(equal_result), len(data))