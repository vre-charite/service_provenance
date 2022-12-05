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

import enum
from ..models.base_models import APIResponse, EAPIResponseCode
from functools import wraps
from requests import Response


def catch_internal(api_namespace):
    '''
    decorator to catch internal server error.
    '''
    def decorator(func):
        @wraps(func)
        async def inner(*args, **kwargs):
            try:
                return await func(*args, **kwargs)
            except Exception as exce:
                respon = APIResponse()
                respon.code = EAPIResponseCode.internal_error
                respon.result = None
                err = api_namespace + " " + str(exce)
                respon.error_msg = customized_error_template(
                    ECustomizedError.INTERNAL) % err
                return respon.json_response()
        return inner
    return decorator


class ECustomizedError(enum.Enum):
    '''
    Enum of customized errors
    '''
    FILE_NOT_FOUND = "FILE_NOT_FOUND"
    INVALID_FILE_AMOUNT = "INVALID_FILE_AMOUNT"
    JOB_NOT_FOUND = "JOB_NOT_FOUND"
    FORGED_TOKEN = "FORGED_TOKEN"
    TOKEN_EXPIRED = "TOKEN_EXPIRED"
    INVALID_TOKEN = "INVALID_TOKEN"
    INTERNAL = "INTERNAL"


def customized_error_template(customized_error: ECustomizedError):
    '''
    get error template
    '''
    return {
        "FILE_NOT_FOUND": "[File not found] %s.",
        "INVALID_FILE_AMOUNT": "[Invalid file amount] must greater than 0",
        "JOB_NOT_FOUND": "[Invalid Job ID] Not Found",
        "FORGED_TOKEN": "[Invalid Token] System detected forged token, \
                    a report has been submitted.",
        "TOKEN_EXPIRED": "[Invalid Token] Already expired.",
        "INVALID_TOKEN": "[Invalid Token] %s",
        "INTERNAL": "[Internal] %s"
    }.get(
        customized_error.name, "Unknown Error"
    )


def jsonrespon_handler(endpoint: str, response: Response):
    '''
    return json response when code starts with 2 , else riase an error
    '''
    if response.status_code // 200 == 1:
        return response.json()
    else:
        error_msg = "[Post Error %s] %s ------ Text: %s, Json: %s " % \
            str(response.status_code), endpoint, \
            str(response.text), str(response.json())
        raise Exception(error_msg)
