SELECT title FROM movies
JOIN stars on movies.id = stars.movie_id
JOIN ratings on stars.movie_id = ratings.movie_id
JOIN people on stars.person_id = people.id
WHERE people.name = "Chadwick Boseman" ORDER by rating DESC LIMIT 5;