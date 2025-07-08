---
tags:
  - CI4AI
  - Software
  - PADI
---

# Tutorial

#### 1. Create a CKN Topic

We will create a CKN topic named `temperature-sensor-data` to store temperature events. The CKN topics and their details are mentioned [here](https://github.com/Data-to-Insight-Center/cyberinfrastructure-knowledge-network/blob/main/docs/topics.md).

Update `docker-compose.yml` (root directory) and add the topic to the broker environment:

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


#### 2. Produce Events

Create a producer script `produce_temperature_events.py` and run it.

```python
from confluent_kafka import Producer
import json, time

producer = Producer({"bootstrap.servers": "localhost:9092"})

try:
    for i in range(10):
        for sensor_id in ["sensor_1", "sensor_2", "sensor_3"]:
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

Open a shell inside the broker container and start the consumer. You should see JSON‑formatted temperature events.

```bash
kafka-console-consumer --bootstrap-server localhost:9092 --topic temperature-sensor-data --from-beginning
```


#### 3. Connect to a Data Sink

Create the connector configuration `neo4jsink-temperature-connector.json` and place the file in `ckn_broker/connectors/` (or your chosen directory).

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

#### 4. Register the connector

```bash
curl -X POST -H "Content-Type: application/json" \
     --data @/app/neo4jsink-temperature-connector.json \
     http://localhost:8083/connectors
```

Restart CKN and run the `temperature‑event` producer again.

```bash
make down
make up

python produce_temperature_events.py
```

Open [neo4j browser](http://localhost:7474/browser/) and log in with the credentials mentioned in the docker-compose file to view the streamed data. 
You have successfully set up a temperature‑monitoring plugin with CKN!