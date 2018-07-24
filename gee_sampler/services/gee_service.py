""" GEE service """
import logging
import ee
from gee_sampler.helpers.date_helper import DateHelper

class GEEService(object):
    @staticmethod
    def gee_point_sample(params):
        logging.debug(f"params: {params}")

        point = ee.Geometry.Point([params.get('lat', None), params.get('lon', None)]);

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
                logging.debug(f"min_date: {min_date}")

            # Filter the ImageCollection by the point bounds
            image_collection = image_collection.filterBounds(point)

            # Check the length of the IC
            logging.debug(f"Number of elements: {len(image_collection.toList(5000).getInfo())}")
            
            point_fc = ee.FeatureCollection([
                ee.Feature(point)
            ])

            logging.debug(f"point_fc: {point_fc}")


            first_image = ee.Image(image_collection.first())
            logging.debug(f"first: {first_image.getInfo()}")
            fc_image_red = first_image.reduceRegions(collection=point_fc,
                                               reducer=ee.Reducer.mean(),
                                               scale=30)
            
            return {'result': 'an ImageCollection process', 'data': fc_image_red.getInfo()}

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
