#-*- coding: utf-8 -*-
import os
from kombu import Exchange, Queue
from celery.schedules import crontab



CELERY_IMPORTS = ("ProcessingCeleryTask", )
#from kombu import serialization
#serialization.registry._decoders.pop("application/x-python-serialize")
#BROKER_URL = 'redis://'
BROKER_URL = 'redis://192.168.1.3:6379/0'
#BROKER_URL = 'redis://localhost/0'


#CELERY_DEFAULT_QUEUE = 'default'
#Exchange Type can be specified by [providing type keyword while intializing Exchange with the key word type
#The four options for this type can be
#"direct"
#"topic"
#"fanout"
#"header"
#celery -A ProcessingCeleryTask  worker -n mapping_list_worker -Q mapping_list --concurrency=1 --loglevel=info;
#celery -A ProcessingCeleryTask  worker -n result_worker -Q result --concurrency=1 --loglevel=info;
#celery -A ProcessingCeleryTask  worker -n review_id_worker -Q review_ids --concurrency=1 --loglevel=info;
#celery -A ProcessingCeleryTask  worker -n sentence_tokenization_one -Q sentence_tokenization --concurrency=1 --loglevel=info;
#celery -A ProcessingCeleryTask  worker -n word_tokenization_one -Q word_tokenization --concurrency=1 --loglevel=info;
 


CELERY_QUEUES = (
		Queue('ReviewIdToSentTokenizeQueue', Exchange('default', delivery_mode= 2),  routing_key='ReviewIdToSentTokenizeQueue.import'),
		Queue('ProcessEateryIdQueue', Exchange('default', delivery_mode= 2),  routing_key='ProcessEateryIdQueue.import'),
		Queue('SentTokenizeToNPQueue', Exchange('default', delivery_mode= 2),  routing_key='SentTokenizeToNPQueue.import'),
		Queue('MappingListQueue', Exchange('pos_tagger', delivery_mode= 2),  routing_key='MappingListQueue.import'),
                    )


#And your routes that will decide which task goes where:
CELERY_ROUTES = {
		'ProcessingCeleryTask.ReviewIdToSentTokenize': {
				'queue': 'ReviewIdToSentTokenizeQueue',
				'routing_key': 'ReviewIdToSentTokenizeQueue.import',
                        },		
		'ProcessingCeleryTask.ProcessEateryId': {
				'queue': 'ProcessEateryIdQueue',
				'routing_key': 'ProcessEateryIdQueue.import',
                        },		
		
                
                'ProcessingCeleryTask.SentTokenizeToNP': {
				'queue': 'SentTokenizeToNPQueue',
				'routing_key': 'SentTokenizeToNPQueue.import',
                        },		
                
                'ProcessingCeleryTask.MappingList': {
				'queue': 'MappingListQueue',
				'routing_key': 'MappingListQueue.import',
                                   },
                        }
#BROKER_HOST = ''
#BROKER_PORT = ''
#BROKER_USER = ''
#BROKER_PASSWORD = ''
#BROKER_POOL_LIMIT = 20

#Celery result backend settings, We are using monngoodb to store the results after running the tasks through celery
CELERY_RESULT_BACKEND = 'mongodb'

# mongodb://192.168.1.100:30000/ if the mongodb is hosted on another sevrer or for that matter running on different port or on different url on 
#the same server

CELERY_MONGODB_BACKEND_SETTINGS = {
		'host': '192.168.1.3',
#		'host': 'localhost',
		'port': 27017,
		'database': 'celery',
#		'user': '',
#		'password': '',
		'taskmeta_collection': 'celery_taskmeta',
			}


#How many messages to prefetch at a time multiplied by the number of concurrent processes. The default is 4 
#(four messages for each process). The default setting is usually a good choice, however – if you have very 
#long running tasks waiting in the queue and you have to start the workers, note that the first worker to 
#start will receive four times the number of messages initially. Thus the tasks may not be fairly distributed 
#to the workers.
CELERYD_PREFETCH_MULTIPLIER = 1


#CELERY_RESULT_ENGINE_OPTIONS = {'echo': True}
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_ACCEPT_CONTENT=['application/json']
CELERY_ENABLE_UTC = True
#CELERYD_CONCURRENCY = 20
#CELERYD_LOG_FILE="%s/celery.log"%os.path.dirname(os.path.abspath(__file__))
CELERY_DISABLE_RATE_LIMITS = True


#CELERY_ALWAYS_EAGER = True, this is setup for local development and debugging. This setting tells Celery to 
#process all tasks synchronously which is perfect for running our tests and working locally so we don't have 
#to run a separate worker process. You'll obviously want to turn that off in production.
#CELERY_EAGER_PROPAGATES_EXCEPTIONS = True
#CELERY_ALWAYS_EAGER = True

#CELERY_IGNORE_RESULT = True
CELERY_TRACK_STARTED = True

#Added because of the pobable soultion of the problem 
#InconsistencyError: 
#    Cannot route message for exchange 'celery': Table empty or key no longer exists.
#    Probably the key ('_kombu.binding.celery') has been removed from the Redis database.
#While running chunks on Classification task
SEND_TASK_SENT_EVENT = True
