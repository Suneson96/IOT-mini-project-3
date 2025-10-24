import time, hashlib, gzip, io
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

def _sha256(b: bytes) -> str:
    h = hashlib.sha256(); h.update(b); return h.hexdigest()

def health(request):
    return JsonResponse({"service":"cloud","status":"ok"})

@csrf_exempt
def process(request):
    data = request.body or b""
    size = len(data)
    return JsonResponse({
        "processed_by": "cloud",
        "size": size,
        "sha256": _sha256(data)
    })
