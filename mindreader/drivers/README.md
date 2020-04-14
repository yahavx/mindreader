## drivers
This package is a utility that provides drivers of different types: database, message queue, etc.

Each sub-package corresponds to a driver type. It consists of:
* A python file that is named after the package (for `encoders` it would be `encoder.py`), which contains a base class
that exposes the interface, and allows initializing the driver and using it.
* One or more implementations of the driver, built using the driver convention. 

You can add your own implementation, by following the instructions on the relevant base class.

Example usage of the `database` driver:

```pycon
>>> from mindreader.drivers import Database
>>> database = Database('mongodb://127.0.0.1:27017')  # database.py instructs to use 'mongodb' prefix
>>> print(database)
MongoDB(127.0.0.1:27017)
>>> user = ...
>>> database.insert_user(user)  # inserts user to the database
``` 
