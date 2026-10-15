# Robotic Arm Joint Health Monitoring System — System Explanation

**Author:** Undergraduate Student  
**Course Module:** System Automation (Bonus Challenge)

---

### 1. Rationale for Immediate-Stop Safety Thresholds
The immediate safety check is designed as a strict, hard-coded rule engine that runs before and completely independently of any Machine Learning model. The thresholds were selected based on the physical mechanical limits of standard 6-axis industrial robotic arms:
* **Shoulder joint:** Limit set to **135.0 Nm torque**, **82.0 °C temperature**, and **7.0 mm/s vibration**. As the base pivot bearing a heavy cantilever load, high torque is normal, but anything above 135 Nm indicates extreme mechanical binding or motor overload.
* **Elbow joint:** Limit set to **110.0 Nm torque**, **78.0 °C temperature**, and **6.5 mm/s vibration**.
* **Wrist joint:** Limit set to **75.0 Nm torque**, **75.0 °C temperature**, and **5.8 mm/s vibration**. Wrist gearboxes are smaller and far more sensitive to thermal and shock damage.

Any single sensor reading exceeding these limits indicates an imminent mechanical failure, motor burnout, or human collision hazard. Because safety in an automated factory cannot tolerate model inference lag or false negatives, this check halts the arm immediately with `EMERGENCY_STOP`.

---

### 2. Signal Fusion: Combining Predictive ML and Maintenance Logs
To prevent premature or delayed interventions, the system combines quantitative sensor intelligence with qualitative human observation:
1. **Predictive ML Signal:** A Decision Tree model trained on historical failure data monitors joint degradation trends (e.g., subtle increases in friction torque, running temperature, and vibration) before critical limits are breached.
2. **Technician Log Signal:** A text scanner extracts notes for each arm and checks for physical warning signs logged by line technicians (such as *"squeaking"*, *"grinding"*, *"unusually warm"*, or *"clicking"*).

**Combination Logic for Final Decisions:**
* **Corroborated Wear (`SCHEDULE_MAINTENANCE`):** When the ML model predicts wear **AND** the technician log notes abnormal physical signs, both independent signals confirm that the joint is actively deteriorating. The arm is scheduled for prompt maintenance before line downtime occurs.
* **Single Warning / Ambiguous Evidence (`MONITOR`):** If only one signal flags an anomaly (e.g., sensor numbers are slightly high but no physical symptoms are seen, or a technician noted a minor squeak but sensor readings remain nominal), the arm is placed on `MONITOR` status to increase observation frequency without needlessly halting production.
* **All Clear (`SAFE`):** When sensor metrics are healthy, the ML model predicts normal operation, and technician inspection notes report smooth running.

---

### 3. Spoofed-Sensor Defense Mechanism
* **How It Works:** An attacker or malfunctioning transmitter might inject a fake low or zero torque reading (e.g., reporting 2.0 Nm) to trick the system into believing the arm is operating under nominal load. The defense employs a **cross-sensor physical plausibility check**:
  $$\text{If } (\text{Temperature} > 65.0\ ^\circ\text{C} \text{ and } \text{Vibration} > 4.5\text{ mm/s}) \implies \text{Torque cannot physically be } < 10.0\text{ Nm}$$
  In mechanical machinery, elevated heat and severe vibration cannot occur without mechanical friction and heavy motor current. Detecting low/zero torque under severe heat and vibration flags a sensor spoofing attack and triggers `SCHEDULE_MAINTENANCE` with an alert.
* **What Attacks It Catches:**
  * **Suppression Attacks:** Attackers forcing torque readings to zero or baseline nominal levels while a joint is overheating or seizing up.
  * **Sensor Freeze / Disconnect Attacks:** A severed or grounded torque sensor reporting 0.0 Nm while the joint is actively running and vibrating.
* **What Attacks It Wouldn't Catch:**
  * **Coordinated Multi-Sensor Spoofing:** If an attacker simultaneously hacks and spoofs **all three** sensors (torque, temperature, and vibration) to report perfectly plausible normal numbers, single-point cross-validation cannot catch it without hardware cryptographic authentication or motor current bus verification.
  * **Subtle In-Range Bias:** Small manipulations (e.g., lowering torque by 5 Nm within normal operating bounds) that do not break the physical temperature-vibration-torque correlation.
