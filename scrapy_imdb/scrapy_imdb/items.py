from scrapy import Item
from scrapy.item import Field


class ImdbItem(Item):
    """
    This class keeps all the information we need to capture for a
    movie.
    """
    # unique identifier assigned by imdb
    movie_id = Field()
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
