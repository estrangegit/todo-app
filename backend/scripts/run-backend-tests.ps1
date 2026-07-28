try {
    docker compose -f docker-compose.test.yml up -d db
    docker compose -f docker-compose.test.yml run --rm backend
}
finally {
    docker compose -f docker-compose.test.yml down
}