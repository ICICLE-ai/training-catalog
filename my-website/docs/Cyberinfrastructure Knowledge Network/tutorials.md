---
tags:
  - CI4AI
  - Software
  - PADI
---

# Tutorial

## Step 1  |  Set Up Your Environment

```bash
git clone https://github.com/Data-to-Insight-Center/cyberinfrastructure-knowledge-network.git
cd cyberinfrastructure-knowledge-network
make up  # launches Kafka, Neo4j, and supporting services
```

*Wait a few moments for all services to initialise.*

## Step 2  |  Create a Kafka Topic for Temperature Events

We will create a Kafka topic named `temperature-sensor-data` to store temperature events.

**Update `docker-compose.yml`** (root directory) and add the topic to the broker environment:

```yaml
services:
  broker:
    environment:
      KAFKA_CREATE_TOPICS: "temperature-sensor-data:1:1"
```

Apply the change:

```bash
make down
make up
```

*(Alternatively, create the topic with Kafka CLI, noting that it will disappear when the broker restarts.)*

## Step 3  |  Produce Temperature Events

### Install required libraries

```bash
python -m venv venv
source venv/bin/activate  # or .\venv\Scripts\activate on Windows
pip install confluent-kafka  # <https://pypi.org/project/confluent-kafka/>
```

### Create the producer script – `produce_temperature_events.py`

```python
from confluent_kafka import Producer
import json, time

kafka_conf = {"bootstrap.servers": "localhost:9092"}
producer = Producer(kafka_conf)

sensors = ["sensor_1", "sensor_2", "sensor_3"]

try:
    for i in range(10):
        for sensor_id in sensors:
            event = {
                "sensor_id": sensor_id,
                "temperature": round(20 + 10 * (0.5 - time.time() % 1), 2),
                "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
            }
            producer.produce("temperature-sensor-data", key=sensor_id, value=json.dumps(event))
        producer.flush()
        time.sleep(1)
    print("Produced 10 events successfully.")
except Exception as e:
    print(f"An error occurred: {e}")
```

Run the producer:

```bash
python produce_temperature_events.py
```

## Step 4  |  Consume and View Events

1. **Open a shell inside the Kafka container**

   ```bash
   docker exec -it broker bash  # replace "broker" with the container name if different
   ```

2. **Start a Kafka consumer**

   ```bash
   kafka-console-consumer --bootstrap-server localhost:9092 --topic temperature-sensor-data --from-beginning
   ```

   You should see JSON‑formatted temperature events.

Press **Ctrl +C** (or **Ctrl + Break** on Windows) to exit.

## Step 5  |  Connect Kafka to Neo4j

### Create connector configuration – `neo4jsink-temperature-connector.json`

```json
{
  "name": "Neo4jSinkConnectorTemperature",
  "config": {
    "topics": "temperature-sensor-data",
    "connector.class": "streams.kafka.connect.sink.Neo4jSinkConnector",
    "errors.retry.timeout": "-1",
    "errors.retry.delay.max.ms": "1000",
    "errors.tolerance": "all",
    "errors.log.enable": true,
    "errors.log.include.messages": true,
    "key.converter": "org.apache.kafka.connect.storage.StringConverter",
    "key.converter.schemas.enable": false,
    "value.converter": "org.apache.kafka.connect.json.JsonConverter",
    "value.converter.schemas.enable": false,
    "neo4j.server.uri": "bolt://neo4j:7687",
    "neo4j.authentication.basic.username": "neo4j",
    "neo4j.authentication.basic.password": "PWD_HERE",
    "neo4j.topic.cypher.temperature-sensor-data": "MERGE (sensor:Sensor {id: event.sensor_id}) MERGE (reading:TemperatureReading {timestamp: datetime(event.timestamp)}) SET reading.temperature = event.temperature MERGE (sensor)-[:REPORTED]->(reading)"
  }
}
```

Place the file in `ckn_broker/connectors/` (or your chosen directory).

### Register the connector – `setup_connector.sh`

```bash
curl -X POST -H "Content-Type: application/json" \
     --data @/app/neo4jsink-temperature-connector.json \
     http://localhost:8083/connectors
```

Restart CKN:

```bash
make down
make up
```

Run the temperature‑event producer again:

```bash
python produce_temperature_events.py
```

## Step 6  |  Visualise Data in Neo4j

1. **Open the Neo4j browser:** [http://localhost:7474/browser/](http://localhost:7474/browser/)

2. **Log in** – username `neo4j`, password `PWD_HERE`.

3. **Query the graph:**

   ```cypher
   MATCH (s:Sensor)-[:REPORTED]->(r:TemperatureReading)
   RETURN s, r;
   ```


4. **Explore** the graph using Neo4j visual tools.
