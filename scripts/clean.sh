#!/bin/bash

cd "$(dirname "${BASH_SOURCE[0]}")" || exit

function  main {
    mongo db --eval "db.dropDatabase()"
    docker-compose stop
    docker-compose rm --force

    rm -rf '/var/data/mindreader_data/*'
    echo "Data has been cleaned successfully."
}

main "$@"
