conn = new Mongo();
db = conn.getDB("imdb");
db.movies.ensureIndex( {"movie_id":1} )
db.movies.ensureIndex( {"rating":1} )
db.movies.ensureIndex( {"genre":1} )
db.movies.ensureIndex( {"produced":1} )
db.movies.ensureIndex( {"name":1} )
