---
tags:
  - Software
  - Animal-Ecology
---

# How-To Guides

## How to Configure Camera-Trap Detection Thresholds

### Problem Description
Adjusting detection sensitivity to balance false positives against missed detections in varying field conditions.

### Steps

1. Access the camera-trap configuration in [ct-config/cameratrap-config.py](https://github.com/ICICLE-ai/Smartfield-Backpack/blob/master/ct-config/cameratrap-config.py)

2. Modify the `detection_thresholds` parameter:
   ```python
   "detection_thresholds": "{\"animal\": \"0.4\", \"image_store_save_threshold\": \"0\", \"image_store_reduce_save_threshold\": \"0\"}"
   ```

3. Threshold values range from 0.0 to 1.0:
   - **0.3-0.4**: High sensitivity (more detections, more false positives)
   - **0.5-0.6**: Balanced (recommended for most scenarios)
   - **0.7-0.8**: High precision (fewer false positives, may miss detections)

4. Apply changes:
   ```bash
   python3 cameratrap-config.py
   ```

### Advanced Tips
- Test different thresholds during daytime before field deployment
- Monitor detection logs in `./logs/` to tune sensitivity
- Use higher thresholds in high-traffic areas to reduce false positives

### Troubleshooting
- **Too many false positives**: Increase threshold to 0.6+
- **Missing obvious animals**: Decrease threshold to 0.3-0.4
- **Camera not responding**: Check network connectivity with `ping icicle-ct1.local`

## How to View Real-Time System Logs

### Problem Description
Monitoring system operations and debugging issues during field deployment.

### Steps

1. **View all service logs**:
   ```bash
   docker-compose logs -f
   ```

2. **View specific service logs**:
   ```bash
   docker-compose logs -f wildwings
   docker-compose logs -f smartfield
   docker-compose logs -f openpasslite
   ```

3. **Filter logs by time**:
   ```bash
   docker-compose logs --since 30m smartfield
   ```

4. **Export logs for analysis**:
   ```bash
   docker-compose logs > system-logs-$(date +%Y%m%d).txt
   ```

### Code Examples

**Python log reader**:
```python
import subprocess

def tail_logs(service_name, lines=50):
    cmd = f"docker-compose logs --tail {lines} {service_name}"
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    return result.stdout
```

### Troubleshooting
- **Logs not appearing**: Check if service is running with `docker-compose ps`
- **Permission denied**: Run with `sudo` or add user to docker group
- **Disk space issues**: Use the provided [log-cleaner.sh](https://github.com/ICICLE-ai/Smartfield-Backpack/blob/master/log-cleaner.sh) script

## How to Manually Trigger a Drone Mission

### Problem Description
Testing drone deployment without waiting for camera-trap detections.

### Steps

1. Ensure drone is connected and WildWings service is running:
   ```bash
   docker-compose ps wildwings
   ```

2. Access the SmartField API to publish a test detection:
   ```bash
   curl -X POST http://localhost:2188/test-detection \
     -H "Content-Type: application/json" \
     -d '{"location": {"lat": 40.0, "lon": -83.0}, "confidence": 0.95}'
   ```

3. Monitor mission execution in logs:
   ```bash
   docker-compose logs -f openpasslite wildwings
   ```

4. Check mission status via OpenPassLite:
   ```bash
   curl http://localhost:2177/mission/status
   ```

### Relevant Configuration

Edit [config.toml](https://github.com/ICICLE-ai/Smartfield-Backpack/blob/master/config.toml) to adjust mission parameters:
```toml
[drone]
mission_duration = 45  # seconds
altitude = 10  # meters
video_quality = "high"
```

### Troubleshooting
- **Drone not connecting**: Check USB connection with `lsusb | grep Parrot`
- **Mission fails to start**: Verify GPS lock and battery level
- **Video not recording**: Check storage space in `./AnafiMedia`

## How to Add Custom MQTT Event Handlers

### Problem Description
Extending the system to respond to custom detection events or external triggers.

### Steps

1. Create a new subscriber in [services/mqtt_subscriber/](https://github.com/ICICLE-ai/Smartfield-Backpack/blob/master/services/mqtt_subscriber)

2. Add your handler function:
   ```python
   def on_custom_event(client, userdata, message):
       payload = json.loads(message.payload)
       # Your custom logic here
       print(f"Custom event: {payload}")
   ```

3. Subscribe to your topic:
   ```python
   client.subscribe("smartfield/custom/events")
   client.message_callback_add("smartfield/custom/events", on_custom_event)
   ```

4. Rebuild and restart:
   ```bash
   docker-compose up -d --build mqtt_subscriber
   ```

### Potential Variations
- Filter events by confidence threshold
- Forward events to external systems
- Aggregate multiple detections before triggering actions

### Troubleshooting
- **Messages not received**: Verify topic name matches publisher
- **Connection refused**: Check MQTT broker is running on port 1883
- **Callback not firing**: Ensure proper topic subscription syntax
