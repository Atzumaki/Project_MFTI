#!/bin/bash

DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
docker-compose -f "${DIR}/docker-compose.yml" down
docker-compose -f "${DIR}/docker-compose.yml" build
docker-compose -f "${DIR}/docker-compose.yml" up
echo -e "Сайт работает!"