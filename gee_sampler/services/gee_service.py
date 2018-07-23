""" GEE service """
import logging
import ee

class GEEService(object):
    @staticmethod
    def gee_point_sample(params):
        logging.debug(f"params: {params}")

        point = ee.Geometry.Point([params.get('lat', None), params.get('lon', None)]);

        gee_entity_type = params.get('type')
        gee_entity = getattr(ee, gee_entity_type)(params.get('id'))
        logging.debug(gee_entity)

        def gee_point_image_sample(point, image):
            return {'result': 'an Image process'}

        def gee_point_ic_sample(point, image_collection):
            res = image_collection.getInfo()
            return {'result': 'an ImageCollection process'}

        def gee_point_fc_sample(point, feature_collection):
            return {'result': 'a FeatureCollection process'}

        incumbent_func = {
            'Image': gee_point_image_sample,
            'ImageCollection': gee_point_ic_sample,
            'FeatureCollection': gee_point_fc_sample,
        }[gee_entity_type]
        try:
            result = incumbent_func(point, gee_entity)
        except Exception as e:
            logging.debug(f'An exception occurred while processing data: {e}')
            raise
        
        return {'status': 'OK', 'type': result}
