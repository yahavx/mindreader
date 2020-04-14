## saver

The saver is responsible to save parsed data, supplied by parsers, to a database.

It provides a `Saver` class, which is instantiated via a database url:
```pycon
>>> from mindreader.saver import Saver
>>> saver = Saver(database_url)
```

After that, the `saver` provide the following functions:
* `save`: saves data to the database. It receives the following arguments:
    * `topic`: the type of parsed data, usually the name of the parser which produces it
    * `data`: the data, as a dictionary
    
    Example usage:    
    ```pycon
    >>> from mindreader.parsers import parse
    >>> data = ... 
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