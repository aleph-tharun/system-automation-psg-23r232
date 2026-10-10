import random
import time

LOG_FILE = "day1_log.txt"


# STEP 1: Generate sensor data
def generate_sensor_data():
    return {
        "temperature": random.randint(50, 95),
        "pressure": round(random.uniform(1, 5), 2),
        "vibration": round(random.uniform(0.1, 2.0), 2),
        "current": random.randint(5, 20)
    }


# STEP 2, 7 and 8: Define automation rules
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
        "condition": lambda r: r["pressure"] > 4.5,
        "action": "CHECK_PRESSURE"
    },
    {
        "name": "HIGH_VIBRATION",
        "priority": 3,
        "condition": lambda r: r["vibration"] > 1.5,
        "action": "CHECK_VIBRATION"
    },
    {
        "name": "HIGH_CURRENT",
        "priority": 4,
        "condition": lambda r: r["current"] > 17,
        "action": "REDUCE_LOAD"
    }
]


# STEP 3: Evaluate rules
def evaluate_rules(reading, rules):
    for rule in sorted(rules, key=lambda r: r["priority"]):
        if rule["condition"](reading):
            return rule["name"], rule["action"], rule["priority"]

    return "NO_RULE_FIRED", "CONTINUE_NORMAL", 99


# STEP 4: Take action
def take_action(action):
    if action == "STOP_MACHINE":
        return "Stop machine - high temperature!"
    elif action == "CHECK_PRESSURE":
        return "Check machine pressure!"
    elif action == "CHECK_VIBRATION":
        return "Inspect machine vibration!"
    elif action == "REDUCE_LOAD":
        return "Reduce electrical load!"
    else:
        return "Machine operating normally."


# STEP 5: Log decisions with machine ID and name
def log_decision(machine_id, machine_name, reading, rule_name, action):
    with open(LOG_FILE, "a", encoding="utf-8") as file:
        file.write(
            f"Machine ID: {machine_id} | "
            f"Machine Name: {machine_name} | "
            f"Readings: {reading} | "
            f"Rule: {rule_name} | "
            f"Action: {action}\n"
        )


# STEP 6: Monitor five machines
def main():
    machines = [
        {"id": "M1", "name": "Conveyor Belt"},
        {"id": "M2", "name": "Robotic Arm"},
        {"id": "M3", "name": "Hydraulic Press"},
        {"id": "M4", "name": "Cooling Pump"},
        {"id": "M5", "name": "CNC Machine"}
    ]

    results = []

    print("=" * 45)
    print("       FACTORY MONITORING SYSTEM")
    print("=" * 45)

    for machine in machines:
        machine_id = machine["id"]
        machine_name = machine["name"]

        reading = generate_sensor_data()

        rule_name, action, priority = evaluate_rules(
            reading, RULES
        )

        outcome = take_action(action)

        print(f"\nMachine ID: {machine_id}")
        print(f"Machine Name: {machine_name}")
        print(f"Sensor Readings: {reading}")
        print(f"Rule Triggered: {rule_name}")
        print(f"Action: {outcome}")

        log_decision(
            machine_id, machine_name,
            reading, rule_name, action
        )

        if rule_name != "NO_RULE_FIRED":
            results.append(
                (priority, machine_id, machine_name, rule_name, action)
            )

        time.sleep(0.2)

    # Factory attention report
    print("\n" + "=" * 45)
    print("         FACTORY ATTENTION REPORT")
    print("=" * 45)

    if results:
        results.sort(key=lambda x: x[0])

        print("\nMachines needing attention:")

        for priority, machine_id, machine_name, rule_name, action in results:
            print(f"\nMachine ID: {machine_id}")
            print(f"Machine Name: {machine_name}")
            print(f"Problem: {rule_name}")
            print(f"Action: {take_action(action)}")

        priority, machine_id, machine_name, rule_name, action = results[0]

        print("\n*** IMMEDIATE ATTENTION REQUIRED ***")
        print(f"Machine ID: {machine_id}")
        print(f"Machine Name: {machine_name}")
        print(f"Problem: {rule_name}")
        print(f"Action: {take_action(action)}")

    else:
        print("All five machines are operating normally.")

    print(f"\nFull log saved to: {LOG_FILE}")


if __name__ == "__main__":
    main()