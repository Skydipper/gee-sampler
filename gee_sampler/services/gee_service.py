""" GEE service """
import logging
import ee
from gee_sampler.helpers.date_helper import DateHelper

class GEEService(object):
    """
    params accepted:
        
    """
    @staticmethod
    def gee_point_sample(params):
        logging.debug(f"params: {params}")

        point = ee.Geometry.Point([params.get('lat', None), params.get('lon', None)]);
        scale = params.get('scale', None)

        gee_entity_type = params.get('type')
        gee_entity = getattr(ee, gee_entity_type)(params.get('id'))

        def gee_point_image_sample(point, image):
            return {'result': 'an Image process'}

        def gee_point_ic_sample(point, image_collection):
            # Filtering the ImageCollection by date, if dates are provided
            if params.get('date'):
                min_date = DateHelper.parse_date(params.get('date').get('min'))
                max_date = DateHelper.parse_date(params.get('date').get('max'))
                image_collection = image_collection.filterDate(min_date, max_date)
                
            reducer = params.get('reducer', None)
            reducer_funct = {
                'mean': ee.Reducer.mean(),
                'minMax': ee.Reducer.minMax()
            }[reducer]
            
            
            # Filter the ImageCollection by the point bounds
            image_collection = image_collection.filterBounds(point)

            # And last, limit the results by the provided limit or 5000 (set in the validator)
            limit = params.get('limit')
            image_collection = image_collection.limit(limit)

            ic_ids = image_collection.getInfo()
            logging.debug(f"ic_ids: {ic_ids}")
            
            fc_image_red = image_collection.reduceRegions(
                collection = point_fc,
                reducer = reducer_funct,
                scale = scale
            )
            try:
                result = fc_image_red.getInfo().get('features', {})[0].get('properties', {})
            except IndexError:
                result = {}
                
            return result
        
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
        
        return result
