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

class MetaService(type):
    def __new__(cls, name: str, bases, namespace, **kwargs):
        if not name.startswith('Srv'):
            raise TypeError('[Fatal] Invalid Service Statement: class name should start with "Srv"', name)
        return super().__new__(cls, name, bases, namespace, **kwargs)

class MetaAPI(type):
    def __new__(cls, name: str, bases, namespace, **kwargs):
        if not name.startswith('API'):
            raise TypeError('[Fatal] Invalid API Statement: class name should start with "API"', name)
        if 'api_registry' not in namespace:
            raise TypeError('[Fatal] Invalid API Statement: Function api_registry Not Found ', name)
        return super().__new__(cls, name, bases, namespace, **kwargs)
