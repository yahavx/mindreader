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

Now upload some samples using the [upload_sample](#client), and than you can see the results
at http://127.0.0.1: 
use the [CLI](#cli)
or [API](#api) to consume the data, and the [GUI](#gui) to visual 

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
* ```upload_sample```: reads a sample and uploads it to the server. Use CTRL+C to exit gracefully in the middle. This function receives the following arguments:
    * ```host```: server host
    * ``port``: server port
    * `path`: relative or absolute path to the sample


Format is an optional parameter, which defaults to 'pb' (protobuf), and indicates the format of the file supplied.    
```pycon
>>> from mindreader.client import upload_sample
>>> upload_sample(host='127.0.0.1', port=8000, path='sample.mind.gz', format='pb')
...
^CServer terminated by user (KeyboardInterrupt)
```
    
This function starts a server that is going to receive thoughts.
It receives the following arguments:
- address: a tuple of consist of ip and port, i.e (ip, port), to run the server on
- data: a directory to save received data
    
    Sending SIGINT ends the connection. 
    Usage example:



- `upload_thought`
    
    This function sends a thought to a server. It receives the following arguments:
    - address: a tuple of consist of ip and port, i.e (ip, port), the ip of the server.
    - user: an integer that represents the sender's id
    - thought: a string that contains the thought
    
    Usage example:

    ```pycon
    >>> upload_thought((127.0.0.1, 10000), 1, "I'm hungry")
    done  # when sending is complete, this message is printed 
    ```
  
- `run_webserver`

    This function starts a http website, consists of list of thoughts for each user.
    It receives the following arguments:
    - address: a tuple of consist of ip and port, i.e (ip, port), to run the server on
    - data: a directory that contains thoughts to be displayed on the website
    
    Usage example:
    ```pycon
    >>> run_server((127.0.0.1, 8000), ./data)
    ```

The `bci` package also provides a command-line interface:

```sh
$ python -m bci
Brain Computer Interface, version 1.0.1
```

The CLI provides the `run_server`, `upload_thought` and `run_webserver`, with the same arguments as above:

```sh
$ python -m bci run_server 127.0.0.1:10000 ./data 
...
$ python -m bci upload_thought 127.0.0.1:10000 1 "I'm hungry"
done
$ python -m bci run_webserver
...
```