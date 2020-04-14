## API

The API allows to consume the data from the database.

It provide the `run-api-server` function, which runs the RESTful API server. it receives the following arguments:
* `host`: server host, to serve in 
* `port`: server port
* `database_url`: a url do a database

Example usage:
```pycon
>>> from mindreader.api import run_api_server
>>> run_api_server('127.0.0.1', 5000, 'mongodb://127.0.0.1:27017')
# serves on 127.0.0.1:5000
```

It can be also run via a CLI (with the name `run-server`):
```sh
[mindreader] $ python -m mindreader.api run-server -h/--host '127.0.0.1' -p/--port 5000 \
-d/--database 'mongodb://127.0.0.1:27017'
...
```

After running the server (in either way), it provides the following API endpoints: 
* `GET /users` - returns the list of all the supported users, including their IDs and names.
* `GET /users/user-id` - returns the specified user's details: ID, name, birthday and gender.
* `GET /users/user-id/snapshots` - returns the list of the specified user's snapshot IDs and datetimes.
* `GET /users/user-id/snapshots/snapshot-id` - returns the specified snapshot's details:
ID, datetime, and the available results' names.
* `GET /users/user-id/snapshots/snapshot-id/result-name` - returns the specified snapshot's result. If the result is
is very large (e.g image), it will contain only metadata, with the data itself available in:
    * `GET /users/user-id/snapshots/snapshot-id/color-image/data`
    
All the results are returned in pretty JSON format (except the last one),
 and can be consumed also via the [CLI](../cli/README.md).