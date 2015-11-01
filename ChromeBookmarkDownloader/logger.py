# -*- coding: utf-8 -*-

def get_logger_dict():
    logger_dict = { 
        'version': 1,              
        'disable_existing_loggers': False,
        'formatters': {
            'complex': {
                'format': '%(asctime)s - %(threadName)s - %(name)s - line %(lineno)d - %(levelname)s - %(message)s'
            }
        },
        'handlers': {
            'file': {  
                'class':'logging.handlers.RotatingFileHandler',
                'maxBytes': 2000000,
                'backupCount': 2,
                'formatter': 'complex',
                'level': 'INFO',
                'filename': '/tmp/chromebookmarkdownloader.log'
            },  
            'screen': {
                'level':'INFO',    
                'class':'logging.StreamHandler',
                'formatter': 'complex'
            }
        },
        "root": {
                 'level': 'INFO',
                 'handlers': ['file', 'screen']
        }
    }

    return logger_dict