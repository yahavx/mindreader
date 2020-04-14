## CLI

The CLI consumes the [API](../api/README.md). It provides a command for each API endpoint (except the last one - data).
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
     the [API](../api/README.md)).

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