# Copyright 2022 Indoc Research
# 
# Licensed under the EUPL, Version 1.2 or – as soon they
# will be approved by the European Commission - subsequent
# versions of the EUPL (the "Licence");
# You may not use this work except in compliance with the
# Licence.
# You may obtain a copy of the Licence at:
# 
# https://joinup.ec.europa.eu/collection/eupl/eupl-text-eupl-12
# 
# Unless required by applicable law or agreed to in
# writing, software distributed under the Licence is
# distributed on an "AS IS" basis,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either
# express or implied.
# See the Licence for the specific language governing
# permissions and limitations under the Licence.
# 


import time
from fastapi.testclient import TestClient
from app.main import create_app

app = create_app()
client = TestClient(app)

TESTER = 'harry'
RESOURCE = 'unittest'
PROJECT_CODE = 'testproject'
ACTION = 'testaction'

def test_01_create_audit_log():
    # no action in payload
    payload = {
        "operator": TESTER,
        "target": "string1" + str(time.time()),
        "outcome": "string2" + str(time.time()),
        "resource": RESOURCE,
        "display_name": "string2" + str(time.time()),
        "project_code": PROJECT_CODE
    }

    response = client.post('/v1/audit-logs', json=payload)
    assert response.status_code == 422

    # no operator in palyload
    payload = {
        "action": ACTION,
        "target": "string1" + str(time.time()),
        "outcome": "string2" + str(time.time()),
        "resource": RESOURCE,
        "display_name": "string2" + str(time.time()),
        "project_code": PROJECT_CODE
    }
    response = client.post('/v1/audit-logs', json=payload)
    assert response.status_code == 422

    # no target in palyload
    payload = {
        "operator": TESTER,
        "action": ACTION,
        "outcome": "string2" + str(time.time()),
        "resource": RESOURCE,
        "display_name": "string2" + str(time.time()),
        "project_code": PROJECT_CODE
    }
    response = client.post('/v1/audit-logs', json=payload)
    assert response.status_code == 422

    # no outcome in palyload
    payload = {
        "operator": TESTER,
        "action": ACTION,
        "target": "string1" + str(time.time()),
        "resource": RESOURCE,
        "display_name": "string2" + str(time.time()),
        "project_code": PROJECT_CODE
    }
    response = client.post('/v1/audit-logs', json=payload)
    assert response.status_code == 422

    # no resource in palyload
    payload = {
        "operator": TESTER,
        "action": ACTION,
        "target": "string1" + str(time.time()),
        "outcome": "string2" + str(time.time()),
        "display_name": "string2" + str(time.time()),
        "project_code": PROJECT_CODE
    }
    response = client.post('/v1/audit-logs', json=payload)
    assert response.status_code == 422


    # no display_name in palyload
    payload = {
        "operator": TESTER,
        "action": ACTION,
        "target": "string1" + str(time.time()),
        "outcome": "string2" + str(time.time()),
        "resource": RESOURCE,
        "project_code": PROJECT_CODE
    }
    response = client.post('/v1/audit-logs', json=payload)
    assert response.status_code == 422

    # no project_code in palyload
    payload = {
        "operator": TESTER,
        "action": ACTION,
        "target": "string1" + str(time.time()),
        "outcome": "string2" + str(time.time()),
        "resource": RESOURCE,
        "display_name": "string2" + str(time.time())
    }
    response = client.post('/v1/audit-logs', json=payload)
    assert response.status_code == 422

def test_02_create_audit_log():
    # correct payload
    payload = {
        "operator": TESTER,
        "action": ACTION,
        "target": "string1" + str(time.time()),
        "outcome": "string2" + str(time.time()),
        "resource": RESOURCE,
        "display_name": "string2" + str(time.time()),
        "project_code": PROJECT_CODE,
        "extra": {}
    }
    response = client.post('/v1/audit-logs', json=payload)
    assert response.status_code == 200


def test_01_query_audit_log():
    # no project_code in params
    params = {
        "page": 0,
        "page_size": 10,
        "sort_by": 'createdTime',
        "sort_type": 'desc',
        "action": 'upload',
        "resource": 'file'
    }

    response = client.get('/v1/audit-logs', params=params)
    assert response.status_code == 422


# def test_02_query_audit_log():
#     # no action in params
#     params = {
#         "page": 0,
#         "page_size": 10,
#         "sort_by": 'createdTime',
#         "sort_type": 'desc',
#         "project_code": 'test',
#         "resource": 'file'
#     }

#     response = client.get('/v1/audit-logs', params=params)
#     assert response.status_code == 422

def test_03_query_audit_log():
    # no resource in params
    params = {
        "page": 0,
        "page_size": 10,
        "sort_by": 'createdTime',
        "sort_type": 'desc',
        "project_code": 'test',
        "action": 'upload'
    }

    response = client.get('/v1/audit-logs', params=params)
    assert response.status_code == 422


def test_04_query_audit_log():
    # correct query
    params = {
        "page": 0,
        "page_size": 10,
        "sort_by": 'createdTime',
        "sort_type": 'desc',
        "project_code": PROJECT_CODE,
        "action": ACTION,
        "resource": RESOURCE,
        "operator": TESTER
    }

    response = client.get('/v1/audit-logs', params=params)
    
    res = response.json()
    result = res['result']

    filter_by_resource = []
    filter_by_project_code = []
    filter_by_operator = []
    filter_by_action = []

    for log in result:
        item = log['_source']
        if item['resource'] == RESOURCE:
            filter_by_resource.append(item)
        if item['projectCode'] == PROJECT_CODE:
            filter_by_project_code.append(item)
        if item['operator'] == TESTER:
            filter_by_operator.append(item)
        if item['action'] == ACTION:
            filter_by_action.append(item)
        

    assert response.status_code == 200
    # assert len(result) > 0
    # assert len(result) == len(filter_by_resource)
    # assert len(result) == len(filter_by_project_code)
    # assert len(result) == len(filter_by_operator)
    # assert len(result) == len(filter_by_action)