from fastapi import APIRouter, Depends
from fastapi_utils.cbv import cbv
from app.models.base_models import APIResponse, EAPIResponseCode
from app.models.models_lineage import GETLineage, GETLineageResponse, POSTLineage, POSTLineageResponse, creation_form_factory 
from app.config import ConfigClass
from app.commons.atlas.lineage_manager import SrvLineageMgr
from app.commons.logger_services.logger_factory_service import SrvLoggerFactory
import requests

router = APIRouter()

@cbv(router)
class Lineage:
    lineage_mgr = SrvLineageMgr()
    _logger = SrvLoggerFactory('api_lineage_action').get_logger()

    @router.get('/', response_model=GETLineageResponse, summary="Get Lineage")
    def get(self, params: GETLineage = Depends(GETLineage)):
        '''
        get lineage, query params: geid, direction defult(INPUT)
        '''
        api_response = GETLineageResponse()
        geid = params.geid
        type_name = 'file_data'

        response = self.lineage_mgr.get(geid, type_name, params.direction)
        if response.status_code == 200:
            response_json = response.json()
            if response_json['guidEntityMap']:
                pass
            else:
                res_default_entity = self.lineage_mgr.search_entity(geid, type_name=type_name)
                if res_default_entity.status_code == 200 and len(res_default_entity.json()['entities']) > 0:
                    default_entity = res_default_entity.json()['entities'][0]
                    response_json['guidEntityMap'] = {
                        '{}'.format(default_entity['guid']): default_entity
                    }
                else:
                    api_response.error_msg = "Invalid Entity"
                    api_response.code = EAPIResponseCode.bad_request
                    return api_response.json()
            api_response.result = response_json
            return api_response.json_response()
        else:
            self._logger.error('Error: %s', response.text)
            api_response.error_msg = response.text
            api_response.code = EAPIResponseCode.internal_error
            return api_response.json_response()
        return api_response.json_response()


    @router.post('/', response_model=POSTLineageResponse, summary="POST Lineage")
    def post(self, data: POSTLineage):
        '''
        add new lineage to the metadata service by payload
            {
                'input_geid': '',
                'output_geid': '',
                'project_code': '',
                'pipeline_name': '',
                'description': '',
            }
        '''
        api_response = POSTLineageResponse()
        creation_form = {}

        if data.input_geid == data.output_geid:
            api_response.error_msg = "Input and Output geid are the same"
            api_response.code = EAPIResponseCode.bad_request
            return api_response.json_response()

        try:
            creation_form = creation_form_factory(data)
        except Exception as e:
            self._logger.error('Error in create lineage: %s', str(e))
            api_response.error_msg = str(e)
            api_response.code = EAPIResponseCode.bad_request
            return api_response.json_response()

        try:
            ## create atlas lineage
            res = self.lineage_mgr.create(creation_form, version='v2')
            # log it if not 200 level response
            if res.status_code >= 300:
                self._logger.error('Error in response: %s', res.text)
                api_response.error_msg = res.text
                api_response.code = EAPIResponseCode.internal_error
                return api_response.json_response()
        except Exception as e:
            self._logger.error('Error in create lineage: %s', str(e))
            api_response.error_msg = str(e)
            api_response.code = EAPIResponseCode.forbidden
            return api_response.json_response()
        api_response.result = res.json()
        return api_response.json_response()
