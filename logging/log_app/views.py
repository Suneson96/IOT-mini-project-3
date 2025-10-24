import json, time, os
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
LOGFILE = '/app/logs/central_logs.jsonl'

def health(request):
    return JsonResponse({"service":"logging","status":"ok"})

@csrf_exempt
def log_entry(request):
    try: j=json.loads(request.body.decode('utf-8'))
    except Exception: j={'raw':request.body.decode('utf-8','ignore')}
    j['received_ts']=time.time()
    os.makedirs(os.path.dirname(LOGFILE), exist_ok=True)
    with open(LOGFILE,'a') as f: f.write(json.dumps(j)+'\n')
    return JsonResponse({'status':'ok'}, status=201)
def get_logs(request):
    if os.path.exists(LOGFILE):
        with open(LOGFILE) as f: return HttpResponse(f.read(), content_type='text/plain')
    return HttpResponse('no logs', content_type='text/plain')
