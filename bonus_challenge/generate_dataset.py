import csv
import random

# Setting random seed so data is reproducible
random.seed(42)

# Joints tracked on the 6-axis robotic arm
joints = ["shoulder", "elbow", "wrist"]

rows = []

# Generate 40 normal readings (label = 0)
for i in range(1, 41):
    arm_id = f"Arm_{random.randint(1, 10)}"
    joint = random.choice(joints)
    
    # Normal ranges: low-to-moderate torque, cool temps, low vibration
    if joint == "shoulder":
        torque = round(random.uniform(40.0, 85.0), 1)
    elif joint == "elbow":
        torque = round(random.uniform(30.0, 65.0), 1)
    else: # wrist
        torque = round(random.uniform(15.0, 40.0), 1)
        
    temperature = round(random.uniform(32.0, 54.0), 1)
    vibration = round(random.uniform(0.5, 2.5), 2)
    label = 0  # 0 means healthy / normal
    
    rows.append([arm_id, joint, torque, temperature, vibration, label])

# Generate 35 wear/degraded readings (label = 1)
for i in range(1, 36):
    arm_id = f"Arm_{random.randint(1, 10)}"
    joint = random.choice(joints)
    
    # Degraded wear ranges: higher friction torque, elevated temps, increased vibration
    if joint == "shoulder":
        torque = round(random.uniform(90.0, 130.0), 1)
    elif joint == "elbow":
        torque = round(random.uniform(70.0, 105.0), 1)
    else: # wrist
        torque = round(random.uniform(45.0, 72.0), 1)
        
    temperature = round(random.uniform(58.0, 78.0), 1)
    vibration = round(random.uniform(3.0, 5.8), 2)
    label = 1  # 1 means early wear detected
    
    rows.append([arm_id, joint, torque, temperature, vibration, label])

# Shuffle dataset
random.shuffle(rows)

# Save to CSV file
filename = "historical_data.csv"
header = ["arm_id", "joint", "torque", "temperature", "vibration", "label"]

with open(filename, mode="w", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(header)
    writer.writerows(rows)

print(f"Dataset generated successfully! Total rows: {len(rows)} saved to {filename}")
