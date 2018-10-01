"""-"""
from gee_sampler.utils.files import BASE_DIR
import os


SETTINGS = {
    'logging': {
        'level': 'DEBUG'
    },
    'service': {
        'port': os.getenv('PORT')
    },
    'gee': {
        'service_account': 'api-highways@gpsdd-198018.iam.gserviceaccount.com',
        'privatekey_file': BASE_DIR + '/privatekey.pem'
    }
}
