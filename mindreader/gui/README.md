## GUI

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
    After that, visit http://127.0.0.1:8080/ (or your chosen url) to view the website.
