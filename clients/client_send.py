import os, requests
FOG = "http://fog:8000/ingest"
path = os.environ.get("FILE", "/app/sample.txt")
with open(path, "rb") as f:
    data = f.read()
r = requests.post(FOG, data=data, headers={"X-Filename": os.path.basename(path)}, timeout=10)
print("Status:", r.status_code); print("Body:", r.text)
