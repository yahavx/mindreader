## client
The client reads snapshots from a file and sends them to the server. 

It provides the following functions:
* `upload_sample`: reads a sample and uploads it to the server. Use CTRL+C to exit gracefully in the middle. It receives the following arguments:
    * `host`: server host
    * `port`: server port
    * `path`: relative or absolute path to the sample
    * `format`: the format of the sample supplied. Optional parameter, defaults to 'pb' (protobuf)

    Example usage:    
    ```pycon
    >>> from mindreader.client import upload_sample
    >>> upload_sample(host='127.0.0.1', port=8000, path='sample.mind.gz', format='protobuf')
    ...
    ^CSome of the snapshots were not sent due to a keyboard interrupt. Total sent: 27
    >>>
    ```
  
    It is also consumable by a CLI, where the host and port are optional (and default to the shown here):
    ```sh
    [mindreader] $ python -m mindreader.client -h/--host '127.0.0.1' -p/--port 8000 \
    -f/--file_format 'protobuf' snapshot.mind.gz'
    ...
    All the 1024 snapshots were sent successfully!  # We were patient this time
    [mindreader] $ 
    ```