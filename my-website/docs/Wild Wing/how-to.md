---
tags:
  - Animal-Ecology
  - AI4CI
  - Software
  - Docs
---
# How-To Guides

## Continuing Multi-Session Missions

**Problem:** You want to continue tracking without landing the drone between sessions.

**Solution:**
1. Comment out the takeoff line in `controller.py`:
```python
# drone.piloting.takeoff()
```
2. Save the file
3. Run `./launch.sh` to start the new mission segment

## Customizing Flight Behavior for Different Species

**Problem:** Different animals require different tracking approaches and flight patterns.

**Adjustments in `navigation.py`:**
- **Large, slow animals (elephants, giraffes):** Increase `x_dist_no_subject` for wider search patterns
- **Fast-moving herds (zebras, wildebeest):** Reduce `x_dist`, `y_dist` for tighter tracking
- **Species or group sensitive to noise:** Increase `z_dist` for higher altitude operation

**Weather Considerations:**
- **Windy conditions:** Reduce all distance parameters by 20-30%
- **Poor visibility:** Decrease `DURATION` for shorter, more manageable sessions

## Analyzing Mission Data

**Problem:** You have collected mission data and need to extract behavioral insights.

**Steps:**
1. Navigate to mission folder: `/missions/mission_record_YYYYMMDD_HHMMSS/`
2. Use the provided [data analysis notebook](data_analysis.ipynb) for telemetry analysis
3. For behavior labeling, process video files with [KABR tools](https://github.com/Imageomics/kabr-tools)
4. Cross-reference YOLO detection outputs with video timestamps

**Troubleshooting:**
- **No video stream:** Check VLC network URL and drone connection
- **Poor tracking:** Verify lighting conditions and adjust YOLO confidence thresholds
- **Connection issues:** Restart controller connection and check USB cables
