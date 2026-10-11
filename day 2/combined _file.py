import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score

data = pd.read_csv(r"C:\Users\pl\Desktop\system-automation-psg-23r232\day 2\Data\day2_sample.csv")

X = data[["temperature", "pressure", "vibration", "current", "rpm"]]
y = data["state"]


X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.3, random_state=1, stratify=y
)


scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

ai = LogisticRegression(max_iter=2000)
ai.fit(X_train, y_train)

def rules(r):
    if r["temperature"] > 75:
        return "OVERHEATING"
    elif r["pressure"] < 3.5:
        return "LOW_PRESSURE"
    elif r["vibration"] > 5:
        return "HIGH_VIBRATION"
    elif r["current"] > 18:
        return "MOTOR_OVERLOAD"
    else:
        return "NORMAL"


X_test_original = pd.DataFrame(
    scaler.inverse_transform(X_test),
    columns=X.columns
)

rule_predictions = X_test_original.apply(rules, axis=1)
ai_predictions = ai.predict(X_test)


reading = pd.DataFrame([{
    "temperature": float(input("Temperature: ")),
    "pressure": float(input("Pressure: ")),
    "vibration": float(input("Vibration: ")),
    "current": float(input("Current: ")),
    "rpm": float(input("RPM: "))
}])


rule_result = rules(reading.iloc[0])
ai_result = ai.predict(scaler.transform(reading))[0]

print("\nRule result:", rule_result)
print("AI result:", ai_result)


if rule_result == ai_result == "NORMAL":
    print("Both models agree. Continue monitoring.")

elif rule_result == ai_result:
    print("Both models agree. Inspect the machine.")

else:
    print("Models disagree. Inspect the machine.")

