import requests
from bs4 import BeautifulSoup

BASE_URL = "http://ece444pra5-env.eba-kg8z6if5.us-east-2.elasticbeanstalk.com/"

test_cases = [
    ("This is a real news.", "REAL"),
    ("This is a fake news.", "FAKE"),
    ("The government has announced a new policy to improve education.", "REAL"),
    ("Celebrity endorses miracle cure that doctors don't want you to know about!", "FAKE"),
]

for i, (text, expected) in enumerate(test_cases, start=1):
    resp = requests.post(BASE_URL, data={"text": text})
    resp.raise_for_status()

    soup = BeautifulSoup(resp.text, "html.parser")
    result_div = soup.find("div", class_="result")

    if result_div:
        result_text = result_div.get_text(strip=True)
        predicted = result_text.replace("Prediction:", "").strip()
    else:
        predicted = "UNKNOWN"

    print(f"Test Case {i} ({'PASS' if predicted == expected else 'FAIL'})"
          f": Expected: {expected}, Predicted: {predicted}")
