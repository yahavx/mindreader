# YahavFooBar

Yahav's final project for Advanced System Design course

## Installation

1. Clone the repository and enter it:

    ```sh
    $ git clone git@github.com:yahavx/YahavFooBar.git
    ...
    $ cd YahavFooBar/
    ```

2. Run the installation script and activate the virtual environment:

    ```sh
    $ ./scripts/install.sh
    ...
    $ source .env/bin/activate
    [YahavFB] $ # you're good to go!
    ```

3. To check that everything is working as expected, run the tests:


    ```sh
    $ pytest tests/
    ...
    ```

## Usage

The `bci` (aka Brain Computer Interface) package provides the `Thought` class. 
It also provides a `utils` sub-package, which provides a `Connection` and `Listener` classes.
  In addition, `bci` provides the following functions:  


- `run_server`

    This function starts a server that is going to receive thoughts.
    It receives the following arguments:
    - address: a tuple of consist of ip and port, i.e (ip, port), to run the server on
    - data: a directory to save received data
    
    Sending SIGINT ends the connection. 
    Usage example:

    ```pycon
    >>> run_server((127.0.0.1, 10000), ./data)
    # Waiting for data
    # When data is sent in the correct format, it will be appended to ./data
    # ^CServer terminated by user (KeyboardInterrupt)
    ```

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
    - address
    
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