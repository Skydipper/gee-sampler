""" GEE service """
import logging
import ee

class GEEService(object):
    @staticmethod
    def gee_point_sample(params):
        logging.debug(f"params: {params}")
        return {'result': 'OK'}
