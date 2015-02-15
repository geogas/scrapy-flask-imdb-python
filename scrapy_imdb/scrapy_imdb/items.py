import scrapy
from scrapy.item import Item, Field

"""
This class keeps all the information we need to capture for a
movie.
"""
class ImdbItem(scrapy.Item):
    img_src = Field()
    name = Field()
    produced = Field()
    duration = Field()
    genre = Field()
    released = Field()
    rating = Field()
    rating_cnt = Field()
    description = Field()
    director = Field()
    writer = Field()
    cast = Field()
