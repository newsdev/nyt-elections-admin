import logging
import os

from django.core.management.base import BaseCommand, CommandError
from pymongo import MongoClient


class Command(BaseCommand):

    logger = logging.getLogger(__name__)


    def handle(self, *args, **options):
        MONGODB_CLIENT = MongoClient(os.environ.get('ELEX_RECORDING_MONGO_URL', 'mongodb://localhost:27017/'))
        MONGODB_DATABASE = MONGODB_CLIENT[os.environ.get('ELEX_RECORDING_MONGO_DB', 'ap_elections_loader')]
        collection = MONGODB_DATABASE.elex_recording

        self.logger.info('clear_mongo deleting %s recordings from archives.' % collection.find().count())

        collection.drop()
