import os, requests, time
FOG = os.environ.get("FOG_URL", "http://fog:8000/upload")
path = os.environ.get("FILE", "/app/sample.txt")
with open(path, "rb") as f:
    data = f.read()

while True:
    r = requests.post(FOG, data=data, headers={"X-Filename": os.path.basename(path)}, timeout=10)
    print("Status:", r.status_code); print("Body:", r.text)
    time.sleep(5)
