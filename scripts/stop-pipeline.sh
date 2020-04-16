#!/bin/bash

cd "$(dirname "${BASH_SOURCE[0]}")" || exit

function  main {
    docker-compose stop
    echo "The pipeline is down."
  }


main "$@"