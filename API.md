API overview
============

## Contents

- [Movies](#movies)
  - [Create](#creating-a-movie)
  - [Get](#getting-list-of-all-movies)
- [Comments](#comments)
  - [Create](#creating-a-comment)
  - [Get](#getting-list-of-comments)
- [Top](#top)

### Movies

#### Creating a movie:

    POST /movies
   
Request:

| Attribute                | Description                                                                        | Optional |
| ------------------------ | ---------------------------------------------------------------------------------- | -------- |
| `title`                  | The title of the movie - max 255 chars.                                            | no       |

Responses:
* 201 - movie created
  
  | Attribute                | Description                                                                        | Nullable |
  | ------------------------ | ---------------------------------------------------------------------------------- | -------- |
  | `id`                     | The ID of the movie.                                                               | no       |
  | `title`                  | The title of the movie received from OMDB API.                                     | no       |
  | `details`                | Dynamic object containing movie's details retrieved from OMDB API.                 | no       |
* 400 - bad request (no title specified/empty title/title too long)

  | Attribute                | Description                                                                        | Nullable |
  | ------------------------ | ---------------------------------------------------------------------------------- | -------- |
  | `title`                  | Array with errors details.                                                         | no       |
* 409 - movie with given title exists

  | Attribute                | Description                                                                        | Nullable |
  | ------------------------ | ---------------------------------------------------------------------------------- | -------- |
  | `title`                  | Array with errors details.                                                         | no       |
* 415 - POST sent with inproper content type
* 503 - OMDB API unavailable or returns an error. Movie cannot be created

  | Attribute                | Description                                                                        | Nullable |
  | ------------------------ | ---------------------------------------------------------------------------------- | -------- |
  | `OMDB API`               | Array with errors details.                                                         | no       |

#### Getting list of all movies:

    GET /movies

Response:
* 200 - ok

  List of movies:
  
  | Attribute                | Description                                                                        | Nullable |
  | ------------------------ | ---------------------------------------------------------------------------------- | -------- |
  | `id`                     | The ID of the movie.                                                               | no       |
  | `title`                  | The title of the movie received from OMDB API.                                     | no       |
  | `details`                | Dynamic object containing movie's details retrieved from OMDB API.                 | no       |

### Comments

#### Creating a comment:

    POST /comments

Request:

| Attribute                | Description                                                                        | Optional |
| ------------------------ | ---------------------------------------------------------------------------------- | -------- |
| `movie_id`               | The ID of the [movie](#movies).                                                    | no       |
| `comment`                | Comment to the movie.                                                              | no       |

Responses:
* 201 - comment created
  
  | Attribute                | Description                                                                        | Nullable |
  | ------------------------ | ---------------------------------------------------------------------------------- | -------- |
  | `id`                     | The ID of the comment.                                                             | no       |
  | `movie_id`               | The ID of the movie.                                                               | no       |
  | `comment`                | Comment to the movie.                                                              | no       |
* 400 - bad request (no title specified/empty title/title too long)

  | Attribute                | Description                                                                        | Nullable |
  | ------------------------ | ---------------------------------------------------------------------------------- | -------- |
  | `comment`                | Array with `comment` related errors details.                                       | yes*     |
  | `movie_id`               | Array with `movie_id` related errors details.                                      | yes*     |
  
  \* at least one of the attributes must not be null
* 415 - POST sent with inproper content type

#### Getting list of comments:

    GET /comments

Query params:

| Param                    | Description                                                                        | Optional |
| ------------------------ | ---------------------------------------------------------------------------------- | -------- |
| `movie_id`               | The ID of the movie.                                                               | yes      |

Responses:
* 200 - ok

  List of comments:
  
  | Attribute                | Description                                                                        | Nullable |
  | ------------------------ | ---------------------------------------------------------------------------------- | -------- |
  | `id`                     | The ID of the comment.                                                             | no       |
  | `movie_id`               | The ID of the movie.                                                               | no       |
  | `comment`                | Comment to the movie.                                                              | no       |
* 404 - movie with given `movie_id` not found

### Top

#### Getting list of ranked and sorted movies by number of comments created in specified date range

    GET /top

Query params:

| Param                    | Description                                                                        | Optional |
| ------------------------ | ---------------------------------------------------------------------------------- | -------- |
| `start`                  | Start date in format `YYYY-MM-DD`.                                                 | no       |
| `end`                    | End date in format `YYYY-MM-DD`.                                                   | no       |

Responses:
* 200 - ok

  List of movies sorted by rank, in case of draw movies are sorted by id:
  
  | Attribute                | Description                                                                        | Nullable |
  | ------------------------ | ---------------------------------------------------------------------------------- | -------- |
  | `movie_id`               | The ID of the movie.                                                               | no       |
  | `total_comments`         | Number of comments created in specified date range.                                | no       |
  | `rank`                   | Place in the ranking (most commented movie's rank is 1, draws are possible)        | no       |
 
* 400 - bad request - `start` or `end` params are given in wrong format

  | Attribute                | Description                                                                        | Nullable |
  | ------------------------ | ---------------------------------------------------------------------------------- | -------- |
  | `start`                  | Array with `start` related errors details.                                         | yes*     |
  | `end`                    | Array with `end` related errors details.                                           | yes*     |
 
  \* at least one of the attributes must not be null
  
* 404 - missing `start` or `end` param

  | Attribute                | Description                                                                        | Nullable |
  | ------------------------ | ---------------------------------------------------------------------------------- | -------- |
  | `start`                  | Array with `start` related errors details.                                         | yes*     |
  | `end`                    | Array with `end` related errors details.                                           | yes*     |
 
  \* at least one of the attributes must not be null
