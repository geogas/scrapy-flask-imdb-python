from scrapy import Spider
from scrapy.conf import settings
from scrapy.selector import Selector
from scrapy.http.request import Request
from scrapy_imdb.items import ImdbItem


class ImdbSpider(Spider):
    """
    This class defines the rules according to which we extract information
    from the urls we scrape. We firstly collect all the urls of the given
    list and then we issue a request per url. This request results in a
    page corresponding to a movie existing in the given list. For this
    movie we extract relevant information such as title, duration, etc.
    """
    name = "imdb"
    allowed_domains = ["imdb.com"]
    start_urls = settings['START_URLS']

    # data members
    protocol = "http"
    base_url = "www.imdb.com"

    def parse(self, response):
        """
        For every url existing in start_urls (each one corresponds to a
        movie list) we extract the urls of the movies in the list.
        """
        sel = Selector(response)

        # xpath rule for extracting movies' urls
        url_list = sel.xpath('//tbody[@class="lister-list"]/tr\
                /td[@class="titleColumn"]/a/@href').extract()

        movies_urls = []
        # build the actual link to the movie
        for url in url_list:
            movies_urls.append(self.protocol + "://" + self.base_url + url)
        """
        for every url we issue an http request, the response will
        be handled by the parse_movie function
        """
        for movie_url in movies_urls:
            yield Request(movie_url, callback=self.parse_movies)

    def parse_movies(self, response):
        """
        This function parses the responses of the requests being issued
        by the parse function. Each request results in a webpage
        illustrating information regarding a movie.
        """
        sel = Selector(response)
        item = ImdbItem()

        item['movie_id'] = response.request.url.split('/')[4]
        item['img_src'] = self.get_img_src(sel)
        item['name'] = self.get_movie_name(sel)
        item['produced'] = self.get_production_year(sel)
        item['duration'] = self.get_duration(sel)
        item['genre'] = self.get_genre(sel)
        item['released'] = self.get_release_date(sel)
        item['rating'] = self.get_rating(sel)
        item['rating_cnt'] = self.get_rating_count(sel)
        item['description'] = self.get_description(sel)
        item['director'] = self.get_director(sel)
        item['writer'] = self.get_writer(sel)
        item['cast'] = self.get_cast(sel)
        return item

    def trim(self, raw_str):
        """
        Removes unicode strings from given string. Utility function
        being invoked by multiple functions. Returned value has also
        been stripped.
        """
        return raw_str.encode('ascii', errors='ignore').strip()

    def trim_list(self, raw_list):
        """
        Given a list containing strings that have unicode parts, it
        returns a list having no unicode strings. List items have
        also been stripped.
        """
        return [self.trim(raw_str) for raw_str in raw_list]

    def get_img_src(self, selector):
        """
        Extracts the source of the movie poster.
        """
        img_src = selector.xpath('//div[@class="image"]/a/img[@itemprop="image"]/@src').extract()[0]

        return self.trim(img_src)

    def get_movie_name(self, selector):
        """
        Extracts the name of the movie.
        """
        movie_name = selector.xpath('//h1[@class="header"]/span[@itemprop ="name"]/text()').extract()[0]

        return self.trim(movie_name)

    def get_production_year(self, selector):
        """
        Extracts the year the movie was filmed.
        """
        production_year = selector.xpath('//h1[@class="header"]/span/a/text()').extract()[0]

        return self.trim(production_year)

    def get_duration(self, selector):
        """
        Retrieves the duration of the film as an integer.
        """
        duration = selector.xpath('//time[@itemprop="duration"]/text()').extract()[0]

        return int(self.trim(duration).split()[0])

    def get_genre(self, selector):
        """
        Extracts movie genre.
        """
        genre = selector.xpath('//span[@itemprop="genre"]/text()').extract()

        return self.trim_list(genre)

    def get_release_date(self, selector):
        """
        Retrieves release date.
        """
        release_date = selector.xpath('//div[@class="infobar"]/span[@class="nobr"]/a/text()').extract()[0]

        return self.trim(release_date)

    def get_rating(self, selector):
        """
        Gets the rating of the movie as a float number.
        """
        rating = selector.xpath('//span[@itemprop="ratingValue"]/text()').extract()[0]

        return float(self.trim(rating))

    def get_rating_count(self, selector):
        """
        Retrieves the number of votes for the film (rating count).
        """
        rating_count = selector.xpath('//span[@itemprop="ratingCount"]/text()').extract()[0]

        return int(self.trim(rating_count).replace(',', ''))

    def get_description(self, selector):
        """
        Extracts the movie description (short excerpt).
        """
        description = selector.xpath('//td[@id="overview-top"]/p[@itemprop="description"]/text()').extract()[0]

        return self.trim(description)

    def get_director(self, selector):
        """
        Name(s) of the director(s).
        """
        director = selector.xpath('//div[@itemprop="director"]/a/span[@itemprop="name"]/text()').extract()

        return self.trim_list(director)

    def get_writer(self, selector):
        """
        Name(s) of the movie writer(s).
        """
        writer = selector.xpath('//div[@itemprop="creator"]/a/span[@itemprop="name"]/text()').extract()

        return self.trim_list(writer)

    def get_cast(self, selector):
        """
        Firstnames, lastnames of actors participating in the movie.
        """
        cast = selector.xpath('//table[@class="cast_list"]/tr/td[@itemprop="actor"]//text()').extract()

        return filter(None, self.trim_list(cast))

