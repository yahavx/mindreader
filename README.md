![build status](https://travis-ci.org/yahavx/mindreader.svg?branch=master)
![coverage](https://codecov.io/gh/yahavx/mindreader/branch/master/graph/badge.svg)
![docs](https://readthedocs.org/projects/mindreader/badge/?version=latest)

# mindreader

Yahav's final project for Advanced System Design course.

## Table of Contents

* [Installation](#installation)
* [Quickstart](#quickstart)
* [Usage](#usage)
* [Credits](#credits)

## Installation

1. Clone the repository and enter it:

    ```sh
    $ git clone git@github.com:yahavx/mindreader.git
    ...
    $ cd mindreader/
    ```

2. Run the installation script and activate the virtual environment:

    ```sh
    $ ./scripts/install.sh
    ...
    $ source .env/bin/activate
    [mindreader] $ # you're good to go!
    ```

3. To check that everything is working as expected, run the tests:

    ```sh
    [mindreader] $ pytest tests/
    ...
    ```

## Quickstart
After finishing the [installation](#installation) step, run the ```run-pipeline``` script:

```sh
[mindreader] $ ./scripts/run-pipeline.sh
...
Everything is ready!
[mindreader] $
```

Now upload some samples using the [upload_sample](#client), and than you can visit
http://127.0.0.1:8080/ to see the results. You can also use the [CLI](#cli) or [API](#api) to consume the data.

## Usage

The project contains one package, `mindreader`, which provides the following sub-packages:
* [`client`](#client) :mega: - sends cognition snapshots to the server.
* [`server`](#server) :calling: - receives cognition snapshots from the client, and handles them.
* [`parsers`](#parsers) :hammer: - processes snapshots received from the server.
* [`saver`](#saver) :key: - saves processed data to the database.
* [`api`](#api) :book: - an API to consume the data.
* [`cli`](#cli) :memo: - a CLI that consumes the API.
* [`gui`](#gui) :computer: - allows to visualize the data comfortably.

Below is a simple description, and usage example, of each of the packages above.
Most of the functions can be used via an API and a CLI as well.

For a more detailed explanation, as well as necessary information to manage the code, check the
[official documentation](https://mindreader.readthedocs.io/en/latest/).

### client
The client sends snapshots to the server. It provides the following functions:
* `upload_sample`: reads a sample and uploads it to the server. Use CTRL+C to exit gracefully in the middle. It receives the following arguments:
    * `host`: server host
    * `port`: server port
    * `path`: relative or absolute path to the sample
    * `format`: the format of the sample supplied. Optional parameter, defaults to 'pb' (protobuf)

    Example usage:    
    ```pycon
    >>> from mindreader.client import upload_sample
    >>> upload_sample(host='127.0.0.1', port=8000, path='sample.mind.gz', format='pb')
    ...
    ^CSome of the snapshots were not sent due to a keyboard interrupt. Total sent: 27
    ```
  
    It is also consumable by a CLI, where the host and port are optional (and default to the shown here):
    ```sh
    [mindreader] $ python -m mindreader.client -h/--host '127.0.0.1' -p/--port 8000 \
    -f/--format 'pb' snapshot.mind.gz'
    ...
    All the 1024 snapshots were sent successfully!  # We were patient this time
    [mindreader] $ 
    ```

### server
The server receives snapshots from the client, and is responsible to handle them. 

It provides the following functions:
* `run_server`: starts the server, and handles cognition snapshots received from client. It receives the following arguments:
    * `host`: server host, to listen in
    * `port`: server port
    * `publish`: an handler (function) to the snapshots. Each time a snapshot is received, this function will be called
    with the user (of it) and the snapshot
    
    Example usage:    
    ```pycon
    >>> from mindreader.server import run_server
    >>> def print_snapshot(user, snapshot):
    ...     print(f'User: {user}, Snapshot: {snapshot}')
    >>> run_server(host='127.0.0.1', port=8000, publish=print_snapshot)
    # Listening on 127.0.0.1:8000
    ```
  
    It is also consumable by a CLI, where the host and port are optional (default to the shown here), but instead
    of a handler, it receives a path to a message queue, where it posts the user/snapshot data:
    ```sh
    [mindreader] $ python -m mindreader.server -h/--host '127.0.0.1' -p/--port 8000 \
    'rabbitmq://127.0.0.1:5672/'  # The prefix indicates the message queue type
    ... # Listening on 127.0.0.1:8000, passing messages to rabbit mq at 127.0.0.1:5672 
    ```

### parsers

The parsers sub-package is used to parse snapshots. Each parser can be used directly on a
snapshot, or be deployed to a message queue, where it receives snapshots 
from the queue and pass the results back to it.

The current parsers are color_image, depth_image, feelings, and pose. You can easily 
[add a new parser](#adding-a-new-parser) which will be automatically collected, and deployed when you
[run the pipeline](#quickstart). 

The parsers (package) provides the following functions:
* `parse`: parses a snapshot, and returns the result in JSON format. It receives the following arguments:
    * `parser_name`: the name of the parser
    *  `raw_data`: a snapshot, in JSON format
    
    Example usage:    
    ```pycon
    >>> from mindreader.parsers import parse
    >>> data = ...  # a snapshot, in JSON format
    >>> result = parse('feelings' , data)
    ```
  
    It is also consumable by a CLI, that receives the data through a file (in JSON format), and prints it
    the result to the screen (or to a file):
    ```sh
    [mindreader] $ python -m mindreader.parsers parse 'feelings' 'snapshot.raw' > 'feelings.result'  # saved to a file
    [mindreader] $ python -m mindreader.parsers parse 'feelings' 'snapshot.raw'
    {'hunger': 1.2, 'thirst': 3.5, ...}
    ```

* `run_parser`: runs a parser as a service, so it listens on a message queue, receive raw snapshots, parse them,
    and pass the parsed results back to the message queue. This is only available via the CLI.
    This command receives a parser name, and a url to a message queue. 
    
    Example usage:
    ```sh
    [mindreader] $ python -m mindreader.parsers run-parser 'feeling' 'rabbitmq://127.0.0.1:5672/'
    ...  # Listening on the message queue
    ```

* `run_parsers`: collects all available parsers, and runs each one as a service, as in `run_parser`.
    This is also only available via the CLI.
    This command receives a parser name, and a url to a message queue. Example usage:
    ```sh
    [mindreader] $ python -m mindreader.parsers run-parsers 'rabbitmq://127.0.0.1:5672/'
    ...  # Listening on the message queue, with eash parser separately
    ```
  
#### Adding a new parser
In order to add a new parser, create a `<parser_name>.py` inside this `parsers` sub-package.
Inside, add the parser as a function, which is named `parse_<parser_name>`.
It should receive a raw snapshot (in JSON format), and return the parsed data, in JSON format.
Finally, add to the function an attribute, named `field`, which is the name of the parser (a string).

You can also add a parser as an instance of a class (instead of a function), which 
implements `__call__(self, snapshot)`. The rules from above will follow to this instance, in exactly the same way. 

The parser will be automatically collected, to be used through the parsing functions (with the name
assigned under `field`), and also deployed when [running the pipeline](#quickstart).

Example:
```python
# parsers/example.py

def parse_example(snapshot):
    result = ...  # parse the snapshot
    return {'example': result}

parse_example.field = 'example'
```

Although few parsers can work from the same `.py` file, it is recommended to put each one in
a different file.

### saver

The saver is responsible to save parsed data, supplied by parsers, to a database.

It provides a `Saver` class, which is instantiated via a database url:
```pycon
>>> from mindreader.saver import Saver
>>> saver = Saver(database_url)
```

After that, the `saver` provide the following functions:
* `save`: saves data to the database. It receives the following arguments:
    * `topic`: the type of parsed data, usually the name of the parser which produces it
    * `data`: the data, in JSON format
    
    Example usage:    
    ```pycon
    >>> from mindreader.parsers import parse
    >>> data = ...  # some parsed data, in JSON
    >>> result = parse('feelings', data)
    ```
  
    This function can be also used directly via a CLI, that receives optionally a database url (defaulted to the below),
    a topic name, and a path to a file which contains parsed data of a parser:
    ```sh
    [mindreader] $ python -m cortex.saver save -d/--database 'mongodb://127.0.0.1:27017' \
    'feelings' 'data_folder/feelings.result'
    ```

The following functions are exposed via the CLI:
* `run_saver`: runs the saver as a service, so it listens on a message queue to every relevant topic (parser),
    consume the results, and saves them to the database. This command receives the url of the
    message queue to listen to, and a url to the database, to save the data in.
    
    Example usage:
    ```sh
    [mindreader] $ python -m cortex.saver run-saver 'mongodb://127.0.0.1:27017' \
    'rabbitmq://127.0.0.1:5672/'
    ...
    ```

### API

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
is very large (e.g image), it will contain only metadata, and the data itself will be available in:
    * `GET /users/user-id/snapshots/snapshot-id/color-image/data`
    
All the results are returned in pretty JSON format (except the last one), and can be consumed also via the [CLI](#cli).

### CLI

The CLI consumes the [API](#api). It provides a command for each API endpoint (except the last one - data).
Each command can receive the `-h` (`--host`) and `-p` (`--port`) flags which indicates the host and port to question,
respectively. If not supplied, it defaults to '127.0.0.1', 5000.

The following commands are provided:
* `get-users`: returns the list of all the supported users, including their IDs and names.
```sh
[mindreader] $ python -m mindreader.cli get-users -h '127.0.0.1' -p 5000
[
    {
        "user_id": 42,
        "username": "Dan Gittik"
    }
]
```

* `get-user`: receives a user ID, and returns the specified user's details: ID, name, birthday and gender.
```sh
[mindreader] $ python -m mindreader.cli get-user 42
{
    "birthday": "05/03/1992",
    "gender": "male",
    "user_id": 42,
    "username": "Dan Gittik"
}
```

* `get-snapshots`: receives a user ID, and returns his snapshot IDs and timestamps.
```sh
[mindreader] $ python -m mindreader.cli get-snapshots 42
[
    {
        "date": "04/12/2019, 10:08:07:339000",
        "snapshot_id": "c5f8f545"
    },
    {
        "date": "04/12/2019, 10:08:07:412000",
        "snapshot_id": "9cd2f9d0"
    }
] 
``` 

* `get-snapshot`: receives a user ID and a snapshot ID, and returns the specified snapshot's details:
    ID, datetime, and the available results.
```sh
[mindreader] $ python -m mindreader.cli get-snapshot 42 'c5f8f545'
{
    "date": "04/12/2019, 10:08:07:339000",
    "results": [
        "pose",
        "feelings",
        "depth_image",
        "color_image"
    ],
    "snapshot_id": "c5f8f545"
}
``` 

* `get-result`: receives a user ID, a snapshot ID, and a result name, and returns the snapshot's result
    (if the result is too big, it will return metadata only, the data will be available via
     the [CLI](#cli)).

```sh
[mindreader] $ python -m mindreader.cli get-result 42 'c5f8f545' 'pose'
{
    {
    "rotation": {
        "w": 0.9571326384559261,
        "x": -0.10888676356214629,
        "y": -0.26755994585035286,
        "z": -0.021271118915446748
    },
    "translation": {
        "x": 0.4873843491077423,
        "y": 0.007090016733855009,
        "z": -1.1306129693984985
    }
}
```

### GUI

The GUI consumes and API and visualizes all of the above. It provides the following functions:
* `run-server` function, which recives: 
    * `host`: server host, to serve in
    * `port`: server port
    * `api_host`: host to consume the API from
    * `api_port`: API port
    
    And runs the server at host:port, consuming the data needed from api_host:api_port.
    
    Example usage:    
    ```pycon
    >>> from mindreader.gui import run_server
    >>> run_server(host='127.0.0.1', port=8080, api_host = '127.0.0.1', api_port = 5000)
    # Serving on http://127.0.0.1:8080/ 
    ```
    
    Similarly, it can be run via the CLI:
    ```sh
    [mindreader] $ python -m mindreader.gui run-server -h/--host '127.0.0.1' -p/--port 8080 \
    -H/--api-host '127.0.0.1' -P/--api-port 5000
    # Serving on http://127.0.0.1:8080/ 
    ```

