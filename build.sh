#!/bin/bash

PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo -e "Прекращение работы прошлых докеров"
docker-compose -f "${PROJECT_DIR}/docker-compose.yml" down

echo -e "Построение докера"
docker-compose -f "${PROJECT_DIR}/docker-compose.yml" build

echo -e "Поднятие докера"
docker-compose -f "${PROJECT_DIR}/docker-compose.yml" up

echo -e "Сайт работает!!"