"""
Robotic Arm Joint Health Monitoring System
==========================================
Bonus Challenge Implementation
Author: S Tharun Bhalaaji (23R232)
Description:
    Monitors 6-axis robotic arms on an assembly line using:
    1. Deterministic immediate safety stops
    2. Machine learning for predictive wear detection
    3. Natural language keyword scanning on technician logs
    4. Cross-sensor consistency checks to catch spoofed torque readings
    5. Integrated decision engine producing SAFE, MONITOR, SCHEDULE_MAINTENANCE, or EMERGENCY_STOP
"""

import pandas as pd
from sklearn.tree import DecisionTreeClassifier

# =====================================================================
# 1. IMMEDIATE SAFETY THRESHOLDS (Deterministic rule, No ML)
# =====================================================================
# Hard limits based on manufacturer physical tolerances.
# Exceeding any of these triggers an immediate EMERGENCY_STOP.
SAFETY_LIMITS = {
    "shoulder": {"torque": 135.0, "temp": 82.0, "vibration": 7.0},
    "elbow":    {"torque": 110.0, "temp": 78.0, "vibration": 6.5},
    "wrist":    {"torque": 75.0,  "temp": 75.0, "vibration": 5.8}
}

def check_immediate_safety(joint_readings):
    """
    Requirement 1: Immediate Safety Stop
    Checks each joint against critical physical thresholds.
    Returns: (is_critical, reason_message)
    """
    for joint_name, data in joint_readings.items():
        limits = SAFETY_LIMITS.get(joint_name)
        if not limits:
            continue
            
        torque = data.get("torque", 0)
        temp = data.get("temp", 0)
        vib = data.get("vibration", 0)
        
        if torque >= limits["torque"]:
            return True, f"CRITICAL: {joint_name} torque ({torque} Nm) exceeded safety limit ({limits['torque']} Nm)"
        if temp >= limits["temp"]:
            return True, f"CRITICAL: {joint_name} temp ({temp} deg C) exceeded safety limit ({limits['temp']} deg C)"
        if vib >= limits["vibration"]:
            return True, f"CRITICAL: {joint_name} vibration ({vib} mm/s) exceeded safety limit ({limits['vibration']} mm/s)"
            
    return False, "All joints within physical safety limits."


# =====================================================================
# 2. PREDICTIVE WEAR DETECTION (Machine Learning Model)
# =====================================================================
# Mapping joints to simple numbers for the classifier
JOINT_MAP = {"shoulder": 0, "elbow": 1, "wrist": 2}
FEATURE_NAMES = ["joint_code", "torque", "temperature", "vibration"]

def train_wear_model(csv_file="historical_data.csv"):
    """
    Requirement 2: Predictive Wear Detection
    Trains a Decision Tree on historical labeled joint failure data.
    """
    df = pd.read_csv(csv_file)
    
    # Convert joint name into a numeric code
    df["joint_code"] = df["joint"].map(JOINT_MAP)
    
    X = df[FEATURE_NAMES]
    y = df["label"]
    
    # Simple, highly interpretable decision tree
    model = DecisionTreeClassifier(max_depth=4, random_state=42)
    model.fit(X, y)
    
    return model

def predict_joint_wear(model, joint_readings):
    """
    Uses the trained ML model to predict wear on each joint.
    Returns: (has_wear, list_of_worn_joints)
    """
    worn_joints = []
    for joint_name, data in joint_readings.items():
        joint_code = JOINT_MAP[joint_name]
        sample_df = pd.DataFrame(
            [[joint_code, data["torque"], data["temp"], data["vibration"]]],
            columns=FEATURE_NAMES
        )
        pred = model.predict(sample_df)[0]
        if pred == 1:
            worn_joints.append(joint_name)
            
    return len(worn_joints) > 0, worn_joints


# =====================================================================
# 3. MAINTENANCE LOG SCANNER (Technician Notes Signal)
# =====================================================================
def scan_maintenance_logs(arm_id, log_file="maintenance_logs.txt"):
    """
    Requirement 3: Maintenance notes as a second signal
    Parses unstructured text logs for technician notes mentioning the arm.
    """
    concern_keywords = [
        "squeak", "squeaking", "noise", "clicking", "grinding",
        "vibration", "leak", "warm", "hot", "loose", "jerking", "stiff"
    ]
    
    matched_notes = []
    has_concern = False
    
    try:
        with open(log_file, "r") as f:
            lines = f.readlines()
            
        for line in lines:
            line_clean = line.strip()
            # Check if this note is about this specific arm
            if arm_id.lower() in line_clean.lower():
                matched_notes.append(line_clean)
                lower_line = line_clean.lower()
                for word in concern_keywords:
                    if word in lower_line:
                        has_concern = True
                        break
    except FileNotFoundError:
        return False, ["Log file not found."]
        
    return has_concern, matched_notes


# =====================================================================
# 4. SPOOFED-SENSOR DEFENSE (Physics-Based Plausibility Check)
# =====================================================================
def detect_spoofed_sensor(joint_readings):
    """
    Requirement 4: Spoofed-sensor defense
    Catches attacks where torque sensor is forced to read low/zero
    to hide friction/mechanical binding under high heat and vibration.
    """
    for joint_name, data in joint_readings.items():
        torque = data.get("torque", 0)
        temp = data.get("temp", 0)
        vib = data.get("vibration", 0)
        
        # Physics rule:
        # High friction generates heat (> 65 deg C) and heavy vibration (> 4.5 mm/s).
        # In a real mechanical arm, high friction demands higher motor torque.
        # If torque is reported as near-zero (< 10 Nm) or zero while temp and vib
        # are abnormally elevated, the torque reading is physically impossible.
        if (temp > 65.0 and vib > 4.5) and (torque < 10.0):
            return True, (
                f"SPOOF ALERT: {joint_name} shows high heat ({temp} deg C) and vibration ({vib} mm/s) "
                f"but suspiciously low torque ({torque} Nm). Sensor is likely spoofed!"
            )
            
        # Complete zero or negative torque while actively vibrating heavily
        if vib > 4.0 and torque <= 0.0:
            return True, (
                f"SPOOF ALERT: {joint_name} shows active vibration ({vib} mm/s) but zero/negative torque ({torque} Nm)."
            )
            
    return False, "Sensors appear genuine and consistent with physics."


# =====================================================================
# 5. INTEGRATED DECISION ENGINE (One Decision Per Arm)
# =====================================================================
def evaluate_arm(arm_id, joint_readings, model, log_file="maintenance_logs.txt"):
    """
    Requirement 5: Produce one final decision per arm:
    - EMERGENCY_STOP
    - SCHEDULE_MAINTENANCE
    - MONITOR
    - SAFE
    """
    print(f"\n=======================================================")
    print(f" EVALUATING: {arm_id}")
    print(f"=======================================================")
    
    # Step 1: Immediate Safety Stop Check (Hard Rule - NEVER depends on ML)
    is_critical, crit_msg = check_immediate_safety(joint_readings)
    if is_critical:
        print(f" [!] HARD SAFETY CHECK FAILED: {crit_msg}")
        return "EMERGENCY_STOP", crit_msg

    # Step 2: Spoofed Sensor Check
    is_spoofed, spoof_msg = detect_spoofed_sensor(joint_readings)
    if is_spoofed:
        print(f" [!] SECURITY CHECK FAILED: {spoof_msg}")
        # A spoof attack trying to mask degradation requires immediate maintenance & inspection
        return "SCHEDULE_MAINTENANCE", spoof_msg

    # Step 3: ML Wear Prediction
    has_ml_wear, worn_joints = predict_joint_wear(model, joint_readings)
    if has_ml_wear:
        print(f" [*] ML Model: Early wear predicted on joints: {', '.join(worn_joints)}")
    else:
        print(f" [*] ML Model: Sensor trends look healthy.")

    # Step 4: Maintenance Log Signal
    has_log_concern, notes = scan_maintenance_logs(arm_id, log_file)
    if notes:
        print(f" [*] Technician Logs Found ({len(notes)}):")
        for n in notes:
            print(f"     - {n}")
    else:
        print(f" [*] Technician Logs: No entries found for this arm.")

    # Step 5: Combine Signals for Final Decision
    # Both signals agree that wear/concern exists -> SCHEDULE_MAINTENANCE
    if has_ml_wear and has_log_concern:
        reason = f"Corroborated wear: ML model detected wear on {worn_joints} AND technician logged warning signs."
        return "SCHEDULE_MAINTENANCE", reason

    # Only one signal flags wear/concern -> MONITOR
    if has_ml_wear or has_log_concern:
        if has_ml_wear:
            reason = f"ML model flagged potential wear on {worn_joints}, but no maintenance concerns logged yet."
        else:
            reason = "Technician logged warning notes, but sensor numbers are still within normal bounds."
        return "MONITOR", reason

    # Everything is clean -> SAFE
    return "SAFE", "All sensors normal, ML model predicts healthy, and logs confirm good condition."


# =====================================================================
# DEMO EXECUTION (Reaching all 4 decisions + spoof defense)
# =====================================================================
if __name__ == "__main__":
    print("Training predictive wear model from historical data...")
    model = train_wear_model("historical_data.csv")
    print("Model trained successfully!\n")
    
    # Define test scenarios to demonstrate every outcome:
    test_arms = [
        # Arm 1: Normal sensor readings + clean logs -> SAFE
        {
            "id": "Arm_2",
            "readings": {
                "shoulder": {"torque": 55.0, "temp": 42.0, "vibration": 1.2},
                "elbow":    {"torque": 40.0, "temp": 38.0, "vibration": 0.9},
                "wrist":    {"torque": 22.0, "temp": 36.0, "vibration": 0.8}
            }
        },
        # Arm 2: Sensor numbers trigger ML wear, but no technician issue logged -> MONITOR
        {
            "id": "Arm_5",
            "readings": {
                "shoulder": {"torque": 98.0, "temp": 64.0, "vibration": 3.6},
                "elbow":    {"torque": 45.0, "temp": 40.0, "vibration": 1.1},
                "wrist":    {"torque": 25.0, "temp": 38.0, "vibration": 0.9}
            }
        },
        # Arm 3: ML predicts wear AND technician note mentions grinding/warm -> SCHEDULE_MAINTENANCE
        {
            "id": "Arm_4",
            "readings": {
                "shoulder": {"torque": 60.0, "temp": 45.0, "vibration": 1.5},
                "elbow":    {"torque": 50.0, "temp": 42.0, "vibration": 1.2},
                "wrist":    {"torque": 52.0, "temp": 66.0, "vibration": 4.1}
            }
        },
        # Arm 4: Single reading exceeds safety threshold -> EMERGENCY_STOP
        {
            "id": "Arm_3",
            "readings": {
                "shoulder": {"torque": 65.0,  "temp": 48.0, "vibration": 1.8},
                "elbow":    {"torque": 122.0, "temp": 72.0, "vibration": 3.9}, # Elbow torque > 110 Nm limit!
                "wrist":    {"torque": 30.0,  "temp": 41.0, "vibration": 1.0}
            }
        },
        # Arm 5: Spoofed sensor attack (High heat & vibration, but fake low torque) -> Caught by Defense!
        {
            "id": "Arm_6",
            "readings": {
                "shoulder": {"torque": 2.0,  "temp": 74.0, "vibration": 5.4}, # Fake torque to hide binding!
                "elbow":    {"torque": 42.0, "temp": 40.0, "vibration": 1.2},
                "wrist":    {"torque": 20.0, "temp": 35.0, "vibration": 0.7}
            }
        }
    ]
    
    summary_results = []
    
    for arm in test_arms:
        decision, details = evaluate_arm(arm["id"], arm["readings"], model)
        print(f"\n >>> FINAL DECISION for {arm['id']}: [{decision}]")
        print(f"     Reason: {details}")
        summary_results.append((arm["id"], decision, details))
        
    print("\n" + "=" * 65)
    print(" PIPELINE EXECUTION SUMMARY")
    print("=" * 65)
    print(f"{'ARM ID':<10} | {'FINAL DECISION':<22} | {'DETAILS'}")
    print("-" * 65)
    for arm_id, decision, details in summary_results:
        print(f"{arm_id:<10} | {decision:<22} | {details[:45]}...")
    print("=" * 65)
