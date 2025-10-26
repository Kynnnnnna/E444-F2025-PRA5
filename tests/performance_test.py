import requests
import time
import pandas as pd
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
import seaborn as sns

BASE_URL = "http://ece444pra5-env.eba-kg8z6if5.us-east-2.elasticbeanstalk.com/"

test_cases = [
    ("This is a real news.", "REAL"),
    ("This is a fake news.", "FAKE"),
    ("The government has announced a new policy to improve education.", "REAL"),
    ("Celebrity endorses miracle cure that doctors don't want you to know about!", "FAKE"),
]

all_rows = []

for case_id, (text, expected) in enumerate(test_cases, start=1):
    print(f"Running performance test for case {case_id}...")

    for run_idx in range(100):  # 100 calls per test case
        start = time.perf_counter()

        resp = requests.post(BASE_URL, data={"text": text})
        end = time.perf_counter()

        latency_s = end - start  # seconds
        latency_ms = latency_s * 1000.0

        soup = BeautifulSoup(resp.text, "html.parser")
        result_div = soup.find("div", class_="result")
        if result_div:
            model_pred = result_div.get_text(strip=True).replace("Prediction:", "").strip()
        else:
            model_pred = "UNKNOWN"

        all_rows.append({
            "case_id": case_id,
            "input_text": text,
            "expected_label": expected,
            "predicted_label": model_pred,
            "run_number": run_idx + 1,
            "latency_ms": latency_ms
        })

df = pd.DataFrame(all_rows)
df.to_csv("performance_test_results.csv", index=False)

avg_by_case = df.groupby("case_id")["latency_ms"].mean().reset_index()
print("\nAverage Latency by Test Case:")
print(avg_by_case)


plt.figure()
sns.boxplot(data=df, x="case_id", y="latency_ms", hue="expected_label", palette="coolwarm")
plt.title("Latency Distribution by Test Case")
plt.suptitle("")
plt.xlabel("Test Case ID")
plt.ylabel("Latency (ms)")
plt.savefig("latency_boxplot.png", dpi=200)