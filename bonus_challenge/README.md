# Robotic Arm Joint Health Monitoring System

Bonus Challenge project for automated joint health monitoring of 6-axis robotic arms.

## Project Structure
* `generate_dataset.py` — Generates the synthetic historical training dataset (`historical_data.csv`).
* `historical_data.csv` — Labeled historical sensor readings (75 rows: shoulder, elbow, wrist).
* `maintenance_logs.txt` — Technician inspection logs (10 entries mixing relevant arm notes and general plant notes).
* `monitor_system.py` — Main Python system implementing all 5 requirements.
* `written_explanation.md` — Half-page written explanation addressing thresholds, signal fusion, and spoof defense.

## How to Run

1. **(Optional) Re-generate the historical dataset:**
   ```bash
   python generate_dataset.py
   ```

2. **Run the monitoring system:**
   ```bash
   python monitor_system.py
   ```

## Requirements Addressed
1. **Immediate Safety Stop:** Instant deterministic check against hard physical limits per joint. Never depends on ML.
2. **Predictive Wear Detection:** Decision Tree model trained on historical failure data to detect early wear before failure.
3. **Maintenance Notes Signal:** Keyword scanner that extracts independent observations from technician logs.
4. **Spoofed-Sensor Defense:** Physics-based cross-sensor validation catching fake/suppressed torque readings during high heat and vibration.
5. **One Decision Per Arm:** Evaluates all arms and outputs `SAFE`, `MONITOR`, `SCHEDULE_MAINTENANCE`, or `EMERGENCY_STOP`.
