---
tags:
  - Software
  - Animal-Ecology
---
# Tutorials

## Getting Started with Smart Backpack Deployment

### Overview
This tutorial guides you through deploying the complete Smart Backpack system from camera-trap configuration to autonomous drone operations.

### Prerequisites

#### Hardware Requirements
- **Raspberry Pi 4B**: 64GB Storage, 4GB RAM minimum
- **Webcam**: USB-compatible camera for animal detection
- **WiFi Router**: Local network infrastructure
- **Power Station**: Portable power supply for field deployment
- **Parrot ANAFI Drone** (optional): For full autonomous pipeline

#### Software Requirements
- Docker Engine (v20.10+)
- Docker Compose (v2.0+)
- Python 3.9+
- Linux-based OS (tested on Ubuntu 20.04+)

### Step-by-Step Deployment

#### Step 1: Camera-Trap Configuration

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd smartfield
   ```

2. Navigate to the camera-trap configuration directory:
   ```bash
   cd ct-config
   ```

3. Edit `cameratrap-config.py` to set your controller IP:
   ```python
   controller_ip = 'http://icicle-ct1.local:8080'
   ```

4. Configure the camera-trap by running each section sequentially:

   **Health Check**:
   ```python
   response = requests.get(f'{controller_ip}/health')
   print(response.json())
   ```

   **System Startup**:
   ```python
   response = requests.post(f'{controller_ip}/startup', json={},
                           headers={'Content-Type': 'application/json'})
   ```

   **Configure Detection Parameters**:
   ```python
   payload = {
       "gpu": "false",
       "ckn_mqtt_broker": "192.168.0.122",  # Your MQTT broker IP
       "ct_version": "test",
       "mode": "demo",
       "min_seconds_between_images": "5",
       "model": "yolov5nu_ep120_bs32_lr0.001_0cfb1c03.pt",
       "inference_server": "false",
       "detection_thresholds": "{\"animal\": \"0.4\", \"image_store_save_threshold\": \"0\", \"image_store_reduce_save_threshold\": \"0\"}"
   }
   response = requests.post(f'{controller_ip}/configure', json=payload)
   ```

   **Start Detection**:
   Note: Run the file everytime when you comment and uncomment the piece of code. Dont run the entire file. Run every section of code one by one.
   ```python
   response = requests.post(f'{controller_ip}/run')
   ```

5. Run the configuration:
   ```bash
   python3 cameratrap-config.py
   ```

#### Step 2: System Installation

1. Create required directories:
   ```bash
   mkdir -p logs mission AnafiMedia
   ```

2. Configure system settings in `config.toml`:
   ```bash
   nano config.toml
   ```

   **IMPORTANT**: Update the camera-trap location coordinates precisely. The drone uses these coordinates to navigate to detection sites. Incorrect values will cause the drone to fly to the wrong location.

   ```toml
   # MQTT topic mapping for each Pi
   [mqtt_topics."cameratrap/events"]
   lat = 40.008278960212      # Replace with your camera-trap's exact latitude
   lon = -83.0175149068236    # Replace with your camera-trap's exact longitude
   camid = "pi-001"           # Unique identifier for this camera-trap
   ```

   Also update MQTT broker addresses, network settings, and service endpoints as needed.

3. Build and start services:
   ```bash
   docker-compose up -d
   ```

4. Verify deployment:
   ```bash
   docker-compose ps
   ```

#### Step 3: Verification

Check each service endpoint:
```bash
# OpenPassLite (Mission Planning)
curl http://localhost:2177/

# SmartField (Event Coordination)
curl http://localhost:2188/

# WildWings (Drone Control)
curl http://localhost:2199/
```

#### Step 4: Monitoring Dashboard

Access Grafana at `http://localhost:3000`:
- **Username**: admin
- **Password**: admin


### End Result
Upon successful deployment, you will have:
- ✓ Autonomous camera-trap detecting animals in real-time
- ✓ MQTT-based event communication system
- ✓ Drone coordination ready for autonomous missions
- ✓ Real-time monitoring dashboard
- ✓ Centralized logging infrastructure
