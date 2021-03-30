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
    file_type: str
    operator: str
    zone: str
    file_size: int
    tags: list
    archived: bool
    path: str
    time_lastmodified: int
    time_created: int
    process_pipeline: str
    uploader: str
    file_name: str
    atlas_guid: str
    full_path: str
    generate_id: Optional[str] = None
    project_code: str
    attributes: Optional[list] = []
    priority: Optional[int] = 20

class FileMetaUpdate(BaseModel):
    '''
    Update a File Info
    '''
    global_entity_id: str
    updated_fields: dict