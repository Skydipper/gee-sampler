from gee_sampler.routes.api import error
from gee_sampler.errors import DatasetNotFound, ProviderNotFound
from CTRegisterMicroserviceFlask import request_to_microservice
import logging

def getKeys(mylist: list, mydict: dict):
        return {k: v for k, v in mydict.items() if k in mylist}

class GetDatasetService(object):
    """

    """
    @staticmethod
    def execute(config):
        
        try:
            
            response = request_to_microservice(config)
            if not response or response.get('errors'):
                logging.debug(f"[DATASETSERVICE]: {response}")
                raise DatasetNotFound(message=str(e))
            
            dataset = response.get('data', None).get('attributes', None)
            
            myKeys = getKeys(['tableName', 'provider'], dataset)
            
            if myKeys['provider'] not in ['cog','gee']:
                logging.debug(f"[DATASETSERVICE]: {myKeys['provider']}")
                raise ProviderNotFound(message=str(e))

        except Exception as e:
            raise DatasetNotFound(message=str(e))
        
        return myKeys

    @staticmethod
    def get(datasetId):
        config = {
            'uri': f'/dataset/{datasetId}',
            'method': 'GET'
        }
        return GetDatasetService.execute(config)
    
