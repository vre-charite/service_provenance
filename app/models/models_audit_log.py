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

from enum import Enum
from pydantic import BaseModel, Field
from typing import Optional
from .base_models import APIResponse

class AuditLogCreation(BaseModel):
    '''
    Create an Audit Log
    '''
    action: str
    operator: str
    target: str
    outcome: str
    resource: str
    display_name: str
    project_code: str
    extra: dict

class AuditLogQuery(BaseModel):
    '''
    Query Audit Logs
    '''
    project_code: str
    action: Optional[str] = None
    resource: str
    operator: Optional[str] = None
    start_date: Optional[int] = None
    end_date: Optional[int] = None