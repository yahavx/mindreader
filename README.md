![build status](https://travis-ci.org/yahavx/mindreader.svg?branch=master)
![coverage](https://codecov.io/gh/yahavx/mindreader/branch/master/graph/badge.svg)
![docs](https://readthedocs.org/projects/mindreader/badge/?version=latest)

# mindreader

Yahav's final project for Advanced System Design course.

## Table of contents
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
http://127.0.0.1:8080 to see the results. You can also use the [CLI](#cli) or [API](#api) to consume the data.

## Usage

The `mindreader` package provides the following sub-packages:
* [`client`](#client) :mega: - sends cognition snapshots to the server.
* [`server`](#server) :calling: - receives cognition snapshots from the client, and handles them.
* [`parsers`](#parsers) :hammer: - processes snapshots received from the server.
* [`saver`](#saver) :key: - saves processed data to the database.
* [`api`](#api) :book: - an API to receive the data.
* [`cli`](#cli) :memo: - a CLI to receive the data.
* [`gui`](#gui) :computer: - allows to visualize the data comfortably.

Below is a simple description, and usage example, of each of the packages above.
Most of the functions provide an API and a CLI as well. When the usage is identical,
only one of them will be provided for the example.

For a more detailed explanation, as well as necessary information to manage the code, check the [official documentation](https://mindreader.readthedocs.io/en/latest/).

### client
  
The client provides the following API:
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

The server provides the following API:
* `run_server`: starts the server, and handles cognition snapshots received from client. It receives the following arguments:
    * `host`: server host, to listen in
    * `port`: server port
    * `publish`: an handler (function) to the snapshots. Each time a snapshot is received, this function will be called
    with the user (of it) and the snapshot.
    
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
    ...
    ```

### parsers

The parsers sub-package is used to parse snapshots. Each parser can be used directly on a
snapshot, or be deployed to a message queue, where it receives snapshots 
from the queue and pass the results back to it.

The current parsers are color_image, depth_image, feelings, and pose. You can easily 
[add a new parser](#adding-a-new-parser) which will be automatically collected and deployed when you [run the pipeline](#quickstart). 

 provides the following API:
* `run_server`: starts the server, and handles cognition snapshots received from the client. It receives the following arguments:
    * `host`: server host, to listen in
    * `port`: server port
    * `publish`: an handler (function) to snapshots. Each time a snapshot is received, this function will be called
    with the user (of it) and the snapshot.
    
    Example usage:    
    ```pycon
    >>> from mindreader.server import run_server
    >>> def print_message(user, snapshot):
    ...     print(f'User: {user}, Snapshot: {snapshot}')
    >>> run_server(host='127.0.0.1', port=8000, publish=print_snapshot)
    # Listening on 127.0.0.1:8000
    ```
  
    It is also consumable by a CLI, where the host and port are optional (default to the shown here), but instead
    of a handler, it receives a path to a message queue, where it posts the user/snapshot data:
    ```sh
    [mindreader] $ python -m mindreader.server -h/--host '127.0.0.1' -p/--port 8000 \
    'rabbitmq://127.0.0.1:5672/'  # The prefix indicates the message queue type
    ...
    ```

##### Adding a new parser
In order to add a new parser, create a `<parser_name>.py` inside this sub-package.
Inside, add the parser as a function, which is named `parse_<parser_name>`.
It should receive a raw snapshot, and return the parsed data, in JSON format. Finally, add to the function an attribute, named 'field', which is the name of the parser (string).

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