---
tags:
  - CI4AI
  - Software
  - PADI
---
# Tutorials

### Create a Custom CKN Plug-in

#### 1. Create a CKN Topic

We will create a CKN topic named `temperature-sensor-data` to store temperature events. The CKN topics and their details are mentioned [here](https://github.com/ICICLE-ai/cyberinfrastructure-knowledge-network/blob/main/docs/topics.md).

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

Create the connector configuration `pgsink-temperature-connector.json` and place it in `ckn_broker/`,
following the existing `pgsink-*.json` configs (Postgres is the supported sink for new pipelines —
see `ckn_broker/setup_connector.sh`).

```json
{
  "name": "PgSinkConnectorTemperature",
  "config": {
    "connector.class": "io.confluent.connect.jdbc.JdbcSinkConnector",
    "topics": "temperature-sensor-data",
    "connection.url": "jdbc:postgresql://postgres:5432/d2i",
    "connection.user": "d2i",
    "connection.password": "d2i",
    "value.converter": "org.apache.kafka.connect.json.JsonConverter",
    "table.name.format": "temperature_sensor_data",
    "value.converter.schemas.enable": true,
    "delete.enabled": false,
    "auto.create": true,
    "auto.evolve": false,
    "errors.tolerance": "all",
    "errors.log.enable": true
  }
}
```

#### 4. Register the connector

Add the `curl` registration call to `ckn_broker/setup_connector.sh` alongside the other JDBC sinks:

```bash
curl -X POST -H "Content-Type: application/json" \
     --data @/app/pgsink-temperature-connector.json \
     http://localhost:8083/connectors
```

Restart CKN and run the `temperature‑event` producer again.

```bash
make down
make up

python produce_temperature_events.py
```

Query the `temperature_sensor_data` table in Postgres to view the streamed data.
You have successfully set up a temperature‑monitoring plugin with CKN!
