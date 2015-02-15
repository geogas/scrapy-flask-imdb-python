BOT_NAME = 'scrapy_imdb'

SPIDER_MODULES = ['scrapy_imdb.spiders']
NEWSPIDER_MODULE = 'scrapy_imdb.spiders'

# The url we want to crawl: corresponds to a list of movies in imdb
START_URLS = ['http://www.imdb.com/chart/top']

ITEM_PIPELINES = {'scrapy_imdb.pipelines.ImdbPipeline' : 1}

MONGODB_HOST = "localhost"
MONGODB_PORT = 27017
MONGODB_DB = "imdb"
MONGODB_COLLECTION = "movies"
