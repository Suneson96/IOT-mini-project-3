import os, time, hashlib
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import requests

SIZE_THRESHOLD = int(os.environ.get("SIZE_THRESHOLD", "51200"))
LOG_SERVICE_URL = os.environ.get("LOG_SERVICE_URL", "http://logging:8000/log")
CLOUD_URL = os.environ.get("CLOUD_URL", "http://cloud:8000/process")

RATE_LIMIT_WINDOW = 10
RATE_LIMIT_MAX_REQ = 50
_ip_requests = {}

def _log_event(obj):
    try:
        requests.post(LOG_SERVICE_URL, json=obj, timeout=1)
    except Exception:
        pass

def _check_rate_limit(ip):
    now = time.time()
    arr = [t for t in _ip_requests.get(ip, []) if now - t < RATE_LIMIT_WINDOW]
    arr.append(now)
    _ip_requests[ip] = arr
    return len(arr) <= RATE_LIMIT_MAX_REQ

def health(request): 
    return JsonResponse({"service":"fog","status":"ok"})

def _sha256(b: bytes) -> str:
    h = hashlib.sha256(); h.update(b); return h.hexdigest()

@csrf_exempt
def upload(request):
    ip = request.META.get('REMOTE_ADDR', 'unknown')

    # Accept both JSON and multipart/form-data
    if request.FILES:
        f = next(iter(request.FILES.values()))
        data = f.read()
        filename = f.name
        content_type = f.content_type
    else:
        data = request.body or b""
        filename = request.headers.get("X-Filename", "payload.bin")
        content_type = request.headers.get("Content-Type", "application/octet-stream")

    size = len(data); ts = time.time()
    _log_event({"source":"fog","ip":ip,"size":size,"ts":ts,"endpoint":"/upload","filename":filename,"ctype":content_type})

    if not _check_rate_limit(ip):
        _log_event({"source":"fog","event":"rate_limit_exceeded","ip":ip,"ts":ts})
        return JsonResponse({"error":"rate limit exceeded"}, status=429)

    # Decision
    if size <= SIZE_THRESHOLD:
        # process locally (whole bytes)
        local = {
            "processed_by": "fog",
            "size": size,
            "sha256": _sha256(data)
        }
        # forward whole file to cloud
        try:
            r = requests.post(CLOUD_URL, data=data, headers={"X-Filename": filename}, timeout=10)
            cloud = r.json()
        except Exception as e:
            cloud = {"error":"cloud unreachable","detail":str(e)}
        return JsonResponse({"status":"ok","mode":"small","local":local,"cloud":cloud})
    else:
        # split workload: fog first half, cloud second half
        half = size // 2
        part1, part2 = data[:half], data[half:]
        local = {
            "processed_by": "fog",
            "size": len(part1),
            "sha256": _sha256(part1)
        }
        try:
            r = requests.post(CLOUD_URL, data=part2, headers={"X-Filename": filename}, timeout=15)
            cloud = r.json()
        except Exception as e:
            cloud = {"error":"cloud unreachable","detail":str(e)}
        return JsonResponse({"status":"ok","mode":"split","local":local,"cloud":cloud})
