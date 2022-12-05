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


class FileMetaCreation(BaseModel):
    '''
    Create a File Info
    '''
    global_entity_id: str
    data_type: Optional[str] = 'File'
    operator: str
    zone: str
    file_size: int
    tags: list
    archived: bool
    location: str
    time_lastmodified: int
    time_created: int
    process_pipeline: str
    uploader: str
    file_name: str
    atlas_guid: str
    display_path: str
    dcm_id: Optional[str] = None
    project_code: str
    attributes: Optional[list] = []
    priority: Optional[int] = 20
    version: Optional[str] = None


class FileMetaUpdate(BaseModel):
    '''
    Update a File Info
    '''
    global_entity_id: str
    updated_fields: dict
