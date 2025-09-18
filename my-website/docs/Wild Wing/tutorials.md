---
tags:
  - Animal-Ecology
  - AI4CI
  - Software
  - Docs
---
# Tutorials

## Getting Started with WildWing

### Prerequisites
- **Hardware:** [Parrot Anafi drone](https://www.parrot.com/en/drones/anafi) with controller
- **Operating System:** Ubuntu 22.04.4 OS on x86_64 architecture
- **Software:** [VLC media player](https://www.videolan.org/), text editor (nano, emacs, vi, or VSCode)
- **Optional:** Smartphone with [FreeFlight 6](https://apps.apple.com/us/app/freeflight-6/id1386165299) app

### Complete Setup and First Mission

**Step 1: Environment Setup**
```bash
# Create conda environment (one-time setup)
conda create --name wildwing --file requirements.txt
```

**Step 2: Hardware Connection**
1. Power on the Parrot Anafi drone and Skycontroller
2. Connect drone to controller using USB-A to USB-C cable
3. Wait for blue LED on controller, then disconnect cable
4. Connect controller to laptop via USB-C cable
5. Open VLC Media Player → Media → Open network stream
6. Enter network URL: `rtsp://192.168.53.1/live`

**Step 3: Configure Mission Parameters**
Edit the following files to customize your mission:
- `controller.py`: Set `DURATION` (number of tracking sections)
- `navigation.py`: Adjust movement distances (`x_dist`, `y_dist`, `z_dist`)

**Step 4: Launch Your First Mission**
```bash
./launch.sh
```

**Step 5: Monitor and Control**
- Watch drone's point-of-view via VLC livestream
- Monitor YOLO output in `/missions/mission_record_YYYYMMDD_HHMMSS/`
- Check logs in `/log/outputs_YYYYMMDD_HHMMSS.log`
- Use handheld controller for manual altitude adjustments if needed

**Expected Results:**
- Autonomous animal tracking with recorded video data
- Telemetry logs and YOLO detection outputs
- Mission data ready for behavioral analysis
