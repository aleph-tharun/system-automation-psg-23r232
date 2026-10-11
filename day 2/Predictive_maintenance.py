import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
from sklearn.preprocessing import StandardScaler

data = pd.read_csv(
    r"C:\Users\pl\Desktop\system-automation-psg-23r232\day 2\Data\day2_sample.csv"
)

X = data[["temperature", "pressure", "vibration", "current", "rpm"]]
y = data["state"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.3, random_state=1, stratify=y
)

scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

model = LogisticRegression(max_iter=1000)
model.fit(X_train, y_train)

predictions = model.predict(X_test)

print("Accuracy:", round(accuracy_score(y_test, predictions) * 100, 2), "%")

print("\nConfusion Matrix:")
print(confusion_matrix(y_test, predictions, labels=model.classes_))

print("\nClassification Report:")
print(classification_report(y_test, predictions, zero_division=0))

print("\nActual states:")
print(y_test.head(10).tolist())

print("\nPredicted states:")
print(predictions[:10])