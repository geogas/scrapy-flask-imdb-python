from scrapy.conf import settings
import pymongo, datetime 
from datetime import datetime

"""
Stores the given items into the movies MongoDB collection.
"""
class ImdbPipeline(object):

    """
    This function sets the connection to mongodb up and binds the
    collection variable to the actual db collection.
    """
    def __init__(self):
        conn = pymongo.Connection(settings['MONGODB_HOST'], settings['MONGODB_PORT'])
        db = conn[settings['MONGODB_DB']]
        self.collection = db[settings['MONGODB_COLLECTION']]

    """
    For some movies date information is absent. Dummy values are used
    for missing days and months.
    """
    def get_released(self, released_str):
        released_list = released_str.split()
        
        # in case day info is missing
        if len(released_list) == 2:
            released_str = "1 " + released_str

        # both day and month are absent
        elif len(released_list) == 1:
            released_str = "1 January " + released_str

        return datetime.strptime(released_str, "%d %B %Y")

    """
    This function is responsible for storing the movie items in the
    collection.
    """
    def process_item(self, item, spider):
        item_dict = dict(item)

        # string representation <-> datetime transformation
        item_dict['released'] = self.get_released(item_dict['released'])

        # transform string representation to datetime object
        item_dict['produced'] = datetime.strptime(item_dict['produced']\
                , "%Y")

        # time of insertion
        item_dict['inserted'] = datetime.now()

        self.collection.insert(item_dict)

        return item
