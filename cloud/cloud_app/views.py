import time, hashlib, gzip, io
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

def _sha256(b: bytes) -> str:
    h = hashlib.sha256(); h.update(b); return h.hexdigest()

def _gzip_size(b: bytes) -> int:
    buf = io.BytesIO()
    with gzip.GzipFile(fileobj=buf, mode="wb") as z:
        z.write(b)
    return len(buf.getvalue())


def health(request):
    return JsonResponse({"service":"cloud","status":"ok"})

@csrf_exempt
def process(request):
    data = request.body or b""
    size = len(data)
    # Simulate heavier work
    time.sleep(min(0.5, size / 100000.0))
    return JsonResponse({
        "processed_by": "cloud",
        "size": size,
        "sha256": _sha256(data),
        "gzip_size": _gzip_size(data)
    })
