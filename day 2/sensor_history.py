import csv
import random

with open("sensor_log.csv", "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["temp", "pressure", "vibration", "rpm", "current", "state"])

    for i in range(250):
        temp = random.randint(50, 95)
        pressure = random.randint(1, 5)
        vibration = round(random.uniform(0.1, 2.0), 2)
        rpm = random.randint(500, 3000)
        current = random.randint(5, 20)

        if temp > 80 or vibration > 1.5:
            state = "error"
        elif rpm < 700:
            state = "idle"
        else:
            state = "running"

        w.writerow([temp, pressure, vibration, rpm, current, state])

print("Dataset created successfully!")
