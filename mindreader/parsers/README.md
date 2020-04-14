## parsers

The parsers sub-package is used to parse snapshots. Each parser can be used directly on a
snapshot, or be deployed to a message queue, where it listens and receives snapshots 
from the queue, and pass the results back to it.

The current parsers are color_image, depth_image, feelings, and pose. You can  
[add your own new parser](#adding-a-new-parser) in a few simple steps, and it will be automatically collected and
can be easily deployed.

The parsers (package) provides the following functions:
* `parse`: parses a snapshot, and returns the result in JSON format. It receives the following arguments:
    * `parser_name`: the name of the parser
    *  `raw_snapshot`: a snapshot, encoded in JSON format
    
    Example usage:    
    ```pycon
    >>> from mindreader.parsers import parse
    >>> raw_snapshot = ...  # a snapshot, in JSON format
    >>> result = parse('feelings' , raw_snapshot)
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
    This command receives only a url to a message queue. Example usage:
    ```sh
    [mindreader] $ python -m mindreader.parsers run-parsers 'rabbitmq://127.0.0.1:5672/'
    ...  # Each parser listens on the message queue
    ```
  
#### Adding a new parser
In order to add a new parser, create a `<parser_name>.py` inside this `parsers` sub-package.
Inside, add the parser as a function, which is named `parse_<parser_name>`.
It should receive a [snapshot](../objects/snapshot.py), and return the parsed data, in JSON format.
Finally, add to the function an attribute, named `field`, which is the name of the parser (a string).

You can also add a parser as an instance of a class (instead of a function), which 
implements `__call__(self, snapshot)`. The rules from above will follow to this instance, in exactly the same way. 

The parser will be automatically collected, to be used through the parsing functions (with the name
assigned under `field`).

Example:
```python
# parsers/example.py

def parse_example(snapshot):
    result = ...  # parse the snapshot
    return {'example': result, 'another': result.attr}

parse_example.field = 'example'
```

#### Scalability
It is possible to have as many workers as you like on a single parser. Simply call `run-parser` multiple times
with the same parser and it will be adjusted automatically to split the work evenly.