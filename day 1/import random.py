import random
import time

LOG_FILE = "day1_log.txt"


# STEP 1 and STEP 6: Generate sensor data
def generate_sensor_data():
    return {
        "temperature": random.randint(50, 95),
        "pressure": random.randint(1, 5),
        "vibration": round(random.uniform(0.1, 2.0), 2),
        "current": random.randint(5, 20)
    }


# STEP 2, STEP 7 and STEP 8: Create rules
RULES = [
    {
        "name": "HIGH_TEMP",
        "priority": 1,
        "condition": lambda r: r["temperature"] > 80,
        "action": "STOP_MACHINE"
    },
    {
        "name": "HIGH_PRESSURE",
        "priority": 2,
        "condition": lambda r: r["pressure"] > 4,
        "action": "CHECK_PRESSURE"
    },
    {
        "name": "HIGH_VIBRATION",
        "priority": 3,
        "condition": lambda r: r["vibration"] > 1.5,
        "action": "STOP_MACHINE"
    },
    {
        "name": "HIGH_CURRENT",
        "priority": 4,
        "condition": lambda r: r["current"] > 17,
        "action": "REDUCE_LOAD"
    }
]


# STEP 3: Check the rules
def evaluate_rules(reading, rules):
    for rule in sorted(rules, key=lambda r: r["priority"]):
        if rule["condition"](reading):
            return rule["name"], rule["action"]

    return "NO_RULE_FIRED", "CONTINUE_NORMAL"


# STEP 4: Perform the action
def take_action(action):
    if action == "STOP_MACHINE":
        return "Machine stopped!"
    elif action == "CHECK_PRESSURE":
        return "Check the pressure!"
    elif action == "REDUCE_LOAD":
        return "Reducing electrical load!"
    else:
        return "Machine running normally."


# STEP 5: Save the results
def log_decision(reading, rule_name, action):
    with open(LOG_FILE, "a") as file:
        file.write(
            f"{reading} | {rule_name} | {action}\n"
        )


# MAIN PROGRAM
def main():
    for tick in range(1, 11):
        reading = generate_sensor_data()

        rule_name, action = evaluate_rules(reading, RULES)

        outcome = take_action(action)

        print(f"[Tick {tick:02d}] SENSE -> {reading}")
        print(f"           THINK -> {rule_name}")
        print(f"           ACT   -> {outcome}\n")

        log_decision(reading, rule_name, action)

        time.sleep(0.2)


if __name__ == "__main__":
    main()