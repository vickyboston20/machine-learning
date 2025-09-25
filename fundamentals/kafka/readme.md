# Run Docker
docker compose -f fundamentals/kafka/docker-compose.yaml up -d

#### Check log
docker compose -f fundamentals/kafka/docker-compose.yaml logs kafka

# install package
uv add kafka-python

# Kafka commands
1. docker exec kafka-kafka-1 kafka-topics --list --bootstrap-server localhost:9092
2. docker exec kafka-kafka-1 kafka-topics --create --topic sample-topic --bootstrap-server localhost:9092 --partitions 1 --replication-factor 1
3. docker exec kafka-kafka-1 kafka-topics --describe --topic sample-topic --bootstrap-server localhost:9092