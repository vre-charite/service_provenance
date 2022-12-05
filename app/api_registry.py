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

from fastapi import FastAPI
from .routers import api_root
from .routers.v1 import api_audit_log
from .routers.v1.api_lineage import lineage 
from .routers.v1 import api_file_meta

def api_registry(app: FastAPI):
    app.include_router(api_root.router)
    app.include_router(api_audit_log.router, prefix="/v1")
    app.include_router(lineage.router, prefix="/v1/lineage", tags=["lineage"])
    app.include_router(api_file_meta.router, prefix="/v1")
